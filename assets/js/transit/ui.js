define(["jquery",
    "transit/model",
    "transit/templates",
    "transit/api",
    "transit/maps",
    "transit/config",
    "transit/utils"],
    function ($, model, templates, api, maps, config, utils) {

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
    populateSelect(config.ui.routesDiv, model.routes, 
      function text(d) {return 'Ruta '+d.route_id;},
      function value(d) {return d.route_id;});
  };

  function populateTrips () {
    populateSelect(config.ui.tripsDiv, model.trips, 
      function text(data) {return 'Viaje hacia '+data.trip_headsign;},
      function value(d) {return d.trip_id;});
  };

  function setupTabs() {
    $('a[data-toggle="tab"]').on('shown', function (e) {
      if (e.target.hash == '#stopsTab') {
        maps.toggleLayer('bbox',true);
        maps.controls.selectStops.deactivate();
        maps.controls.selectMultiple.activate();
      } else if (e.target.hash == '#tripsTab') {
        maps.controls.selectMultiple.deactivate();
        maps.controls.selectStops.activate();
      };
    });
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
    
    function saveStops() {
      var readStops = maps.readStops();
      // TODO trip_id <> shape_id in general
      api.put({
        route: 'trip/'+model.selected.trip_id+'/stops',
        params: readStops.stops
      }).done(maps.update());
    };

    $('#prevStop').click(maps.skipHandler(-1));
    $('#nextStop').click(maps.skipHandler(1));

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
        var readShape = maps.readShape();
        api.saveShape(readShape.shape, function(response) {
          console.log(response);
        });
      }
    );

    $('#revShape').click(function (e){
      var selected = $('#tripsSelect').find(':selected')[0],
        trip_id;
      trip_id = $(selected).val();
      e.preventDefault();
      api.revShape(trip_id, function(response) {
        maps.update();
      });
    });

    $('#sortStops').click(function (e){
      var selected = $('#tripsSelect').find(':selected')[0],
        trip_id;
      trip_id = $(selected).val();
      e.preventDefault();
      api.sortStops(trip_id, function(response) {
        maps.update();
      });
    });

    $('#offsetStops').click(function (e){
      var selected = $('#tripsSelect').find(':selected')[0],
        trip_id;
      trip_id = $(selected).val();
      e.preventDefault();
      api.offsetStops(trip_id, function(response) {
        maps.update();
      });
    });

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
        saveStops();
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
        saveStops();
      }
    );
    
    $('#removeStop').click(function (e) {
      e.preventDefault();
      maps.destroySelected();
      saveStops();
    });

    $('#toggleTimepoint').click(function (e) {
      e.preventDefault();
      var tripsSelected = $('#trips').find(':selected')[0],
        trip_id = $(tripsSelected).val(),
        stopFeature = maps.getSelectedStop(),
        is_timepoint = stopFeature.data['is_timepoint'] ? 0 : 1;

      api.put({
        route: 'trip/'+trip_id+'/stop/'+stopFeature['fid']+'/timepoint',
        params: {is_timepoint: is_timepoint},
        success: function(response) {
          console.log(response);
        }
      });

      //maps.update();
    });

    $('#appendStop').click(function (e){
      e.preventDefault();
      maps.appendSelected();
      saveStops();
    });

    // buttons on the Stops tab
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
        //saveStops();
      }
    );

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
    var selectedFeature;
    if (evt && (evt.type == 'featureselected')) {
      selectedFeature = evt.feature;
    } else {
      selectedFeature = null;
    };
    var stopInfoDiv = $('#stopData');
    stopInfoDiv.empty();
    if (selectedFeature) {
      stopInfoDiv.append(templates.stop(selectedFeature));
    };
  };
  
  function renderMultipleStops(evt) {
    var selected,
      multipleDiv;
    selected = maps.bboxGetSelected();
    multipleDiv = $('#multipleStops');
    multipleDiv.empty();
    if (selected.length == 1) {
      multipleDiv.append(templates.stop(selected[0]));
    } else {
      multipleDiv.append(templates.multiple({features:selected}));
    };
    $('#multipleStops table tr button').on('click',function(e){
      var merge = [],
        keep = e.currentTarget.id;

      for (var i = 0; i < selected.length; i++) {
        merge.push(selected[i]['fid']);
      };
      handleMerger({
        keep: keep,
        merge: merge
      });
      maps.update();
    });
  };


  ui.init = function (spec) {

    maps.init({
        layers:['bbox','notes','routes','gpx','stops'],
        controls: 'editor'
    })
    .setCenter(config.initCenter);

    maps.setEventHandlers({
      renderStopInfo: renderStopInfo,
      renderMultipleStops: renderMultipleStops
    });

    model.fetchRoutes().done(populateRoutes);

    setupButtons();
    setupTabs();

  };
  
  return ui;
});
