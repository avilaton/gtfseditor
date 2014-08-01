define(["jquery",
  "transit/model",
  "transit/templates",
  "transit/api",
  "transit/maps",
  "transit/config",
  "transit/utils"
  ],
  function ($, model, templates, api, maps, config, utils) {

    'use strict';

    var ui = {};

    function setupButtons() {
    /*
    Both of these should be moved to the model when the data is 
    hosted there.
    */
    function saveStops() {
      var stops = maps.readStops().stops;
      model.saveStops(stops).done(maps.update());
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

    $('#saveStops').click(function (e){
      e.preventDefault();
      saveStops()
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

  ui.init = function () {

    // maps.init({
    //   layers:['bbox','notes','routes','gpx','stops', 'shapes'],
    //   controls: 'editor'
    // })
    // .setCenter(config.initCenter);

    // maps.setEventHandlers({
    //   renderStopInfo: renderStopInfo,
    // });

    setupButtons();

  };
  
  return ui;
});
