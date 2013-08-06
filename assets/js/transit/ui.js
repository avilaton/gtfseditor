define(["jquery",
    "transit/model",
    "transit/templates",
    "transit/api",
    "transit/maps",
    "transit/config",
    "transit/utils",
    "transit/views/routebar"],
    function ($, model, templates, api, maps, config, utils, RouteBarView) {

  'use strict';

  var ui = {};

  function populateTracks() {
    var options = $('select#' + config.ui.tracksDiv);
    function fillValues(values) {
      options
        .empty()
        .append($('<option />').val('').text('Select an option'));
      $.each(values, function () {
        options.append($('<option />')
          .val(this.filename)
          .text(this.name));
      });
    };
    api.get({
      route: 'tracks/',
      success: fillValues
    });

    return this;
  };

  function populateSelect(div, values, textSetter, valSetter) {
    var options = $('select#' + div);
    options
      .empty()
      .append($('<option />').val(null).text(' -- '));
    $.each(values, function() {
      options.append(
        $('<option />')
        .val(valSetter(this))
        .text(textSetter(this))
      );
    });
  };

  function populateRoutes () {
    var routeBar;

    populateSelect(config.ui.routesDiv, model.routes, 
      function text(d) {return 'Ruta '+d.route_id;},
      function value(d) {return d.route_id;});
    
    routeBar = new RouteBarView({model: {routes: model.routes} });
  };

  function populateTrips () {
    populateSelect(config.ui.tripsDiv, model.trips, 
      function text(data) {return 'Viaje hacia '+data.trip_headsign;},
      function value(d) {return d.trip_id;});
  };

  function setupButtons() {
    $('select#' + config.ui.routesDiv).change(function () {
      var route_id = $(this).find(':selected')[0].value;
      model.selected.route_id = route_id;
      model.selected.trip_id = null;
      model.selected.shape_id = null;
      model.fetchTrips().done(populateTrips);
      maps.update();
      renderServices(route_id);
      renderStopInfo(null);
    });

    $('select#' + config.ui.tripsDiv).change(function () {
      var trip_id = $(this).find(':selected')[0].value;
      model.selected.trip_id = trip_id;
      model.getTripShape(trip_id);
      maps.update();
      renderStopInfo(null);
    });

    $('select#' + config.ui.tracksDiv).change(function () {
      var selected = $(this).find(':selected')[0];
      var track = $(selected).val();
      maps.update({track:track});
    });

    /*
    Both of these should be moved to the model when the data is 
    hosted there.
     */
    function saveStops() {
      var stops = maps.readStops().stops;
      model.saveStops(stops).done(maps.update());
    };
    function saveShape() {
      var shape = maps.readShape().shape;
      model.saveShape(shape).done(maps.update());
    };

    $('#prevStop').click(maps.skipHandler(-1));
    $('#nextStop').click(maps.skipHandler(1));

    $('#routesPane').on('click', function() {
      $('#leftbar, #leftbarStops').toggle();
    });

    $('#editShape').toggle(
      function () {
        $(this).addClass('btn-primary');
        maps.controls.selectStops.deactivate();
        maps.controls.modifyShape.activate();
      },
      function () {
        $(this).removeClass('btn-primary');
        maps.controls.modifyShape.deactivate();
        maps.controls.selectStops.activate();
      }
    );

    $('#multipleSelect').toggle(
      function () {
        $(this).addClass('btn-primary');
        maps.controls.selectStops.deactivate();
        maps.controls.selectMultiple.activate();
      },
      function () {
        $(this).removeClass('btn-primary');
        maps.controls.selectMultiple.deactivate();
        maps.controls.selectStops.activate();
      }
    );

    $('#editStops').toggle(
      function () {
        $(this).addClass('btn-primary');
        maps.controls.selectStops.deactivate();
        maps.controls.modifyStops.activate();
      }, 
      function () {
        $(this).removeClass('btn-primary');
        maps.controls.modifyStops.deactivate();
        maps.controls.selectStops.activate();
      }
    );

    $('#moveStops').toggle(
      function () {
        $(this).addClass('btn-primary');
        maps.controls.selectMultiple.deactivate();
        maps.controls.modifyBbox.activate();
      }, 
      function () {
        $(this).removeClass('btn-primary');
        maps.controls.modifyBbox.deactivate();
        maps.controls.selectMultiple.activate();
      }
    );

    $('#drawStops').toggle(
      function () {
        $(this).addClass('btn-primary');
        maps.controls.selectStops.deactivate();
        maps.controls.drawStops.activate();
      },
      function () {
        $(this).removeClass('btn-primary');
        maps.controls.drawStops.deactivate();
        maps.controls.selectStops.activate();
      }
    );
    
    $('#saveShape').click(function (e){
      e.preventDefault();
      saveShape()
    });

    $('#saveStops').click(function (e){
      e.preventDefault();
      saveStops()
    });

    $('#revShape').click(function (e){
      e.preventDefault();
      /* Should be model.reverseShape when all has been moved */
      maps.reverseShape()
      saveShape();
    });

    $('#sortStops').click(function (e){
      e.preventDefault();
      model.sortTripStops().done(maps.update());
    });

    $('#offsetStops').click(function (e){
      e.preventDefault();
      model.alignTripStops().done(maps.update());
    });

    $('#removeStop').click(function (e) {
      e.preventDefault();
      maps.destroySelected();
    });

    $('#toggleTimepoint').click(function (e) {
      e.preventDefault();
      var trip_id = model.selected.trip_id,
        stopFeature = maps.getSelectedStop(),
        is_timepoint = stopFeature.data['is_timepoint'] ? 0 : 1;

      api.put({
        route: 'trip/'+trip_id+'/stop/'+stopFeature['fid']+'/timepoint',
        params: {is_timepoint: is_timepoint},
        success: function(response) {
          console.log(response);
        }
      }).done(maps.update());
    });

    $('#appendStop').click(function (e){
      e.preventDefault();
      maps.appendSelected();
    });

    $('#findStop').on('click', function (event){
      var stop_id = $('#stop_id').val();
      api.get({route: 'stop/'+stop_id}).done(function (response) {
        if (response.hasOwnProperty('features')) {
          var coord = response.features[0].geometry.coordinates;
          maps.setCenter({
            lon: coord[0], lat: coord[1], zoom: 18
          });
        }
      });

    });
    $("#stop_id").keyup(function(event){
      if(event.keyCode == 13){
        $("#findStop").click();
      }
    });

    return this;
  };

  function renderServices(route_id) {
    var fillSchedule = function (data) {
      var scheduleDiv = $('#schedule');
      scheduleDiv.empty();
      scheduleDiv.append(templates.schedule(data));
    };
    api.getServices(route_id, fillSchedule);
  };

  function handleMerger(spec) {
    var merge;
    merge = JSON.stringify(spec.merge);
    api.mergeStops(spec.keep,merge,
      function (response) {
        console.log(response);
    });
  };

  function renderStopInfo(evt) {
    var stopAttrDiv = $(config.ui.stopAttr);
    var stopListDiv = $(config.ui.stopList);
    var selectedFeatures = evt.object.selectedFeatures;
    stopAttrDiv.empty();
    stopListDiv.empty();
    if (evt && (evt.type == 'featureselected')) {
      if (selectedFeatures.length == 1) {
        stopAttrDiv.append(templates.stop(selectedFeatures[0]));
        $('#saveStopData').on('click', function(){
          var stop_calle = $('#stop_calle').val();
          model.stop.properties['stop_calle'] = stop_calle;
          console.log(stop_calle);
          console.log('save clicked', model.stop);
          model.updateStop();
        });
      } else {
        stopListDiv.append(templates.multiple({features: selectedFeatures}));
        $('#stopList table tr button').on('click',function(e){
          var merge = [],
            keep = e.currentTarget.id;

          for (var i = 0; i < selectedFeatures.length; i++) {
            merge.push(selectedFeatures[i]['fid']);
          };
          handleMerger({
            keep: keep,
            merge: merge
          });
          maps.update();
        });
      };
    } else {
      selectedFeatures = null;
    };
  };

  ui.init = function (spec) {

    maps.init({
        layers:['bbox','notes','routes','gpx','stops'],
        controls: 'editor'
    })
    .setCenter(config.initCenter);

    maps.setEventHandlers({
      renderStopInfo: renderStopInfo,
    });

    model.fetchRoutes().done(populateRoutes);

    setupButtons();

  };
  
  return ui;
});
