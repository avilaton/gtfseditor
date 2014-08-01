define([
  'jquery',
  "models/shape",
	"models/stop",
  "collections/routes",
  "collections/trips",
  "collections/stops",
  "collections/kml",
  "views/filter",
  "views/kmlSelect",
  "views/routesSelect",
  "views/tripsSelect",
  "views/shapesToolbox",
  "views/sequenceToolbox",
  "views/stopData",
  "views/stopToolbar",
  "views/map"
	], 
  function ($, ShapeModel, StopModel, RoutesCollection, TripsCollection, 
    StopsCollection, KmlCollection, FilterView, KmlSelectView, RoutesSelectView, 
    TripsSelectView, ShapesToolboxView, SequenceToolboxView, 
    StopDataView, StopToolbarView, MapView) {

    require(["bootstrap"]);

		function createControls () {
			var state = window.app.state;
			
			// console.log("create controls");

      state.routes = new RoutesCollection();
      state.kml = new KmlCollection();
      state.trips = new TripsCollection();
      state.stops = new StopsCollection();
      state.shape = new ShapeModel();
      state.stop = new StopModel();

			state.routes.fetch();


      var routeSelector = new RoutesSelectView({
        collection: state.routes
      });
      var tripsSelector = new TripsSelectView({
        routesCollection: state.routes,
        collection: state.trips
      });

      var kmlSelector = new KmlSelectView({
        el: $("#kmlSelect"),
        collection: state.kml
      })

      var myMap = new MapView({
        shape: state.shape,
        stops: state.stops,
        stop: state.stop,
        kml: state.kml
      });
      // myMap.bboxLayer.refresh({force: true});

      var filterBox = new FilterView({
        bboxLayer: myMap.bboxLayer
      });

      var myShapesToolbox = new ShapesToolboxView({
        model: state.shape,
        controls: myMap.controls,
        map: myMap
      });

      var mySequenceToolbox = new SequenceToolboxView({
        collection: state.stops,
        model: state.stop,
        controls: myMap.controls
      });

      var myStopDataView = new StopDataView({
        model: state.stop,
        controls: myMap.controls
      });

      var myStopToolbarView = new StopToolbarView({
        model: state.stop,
        controls: myMap.controls,
        stopDataView: myStopDataView
      });

      /** 
       * this should be inside map.js
       */
      state.trips.on("trip_selected", function (selectedModel) {
        var trip_id = selectedModel.get("trip_id");
        var shape_id = selectedModel.get("shape_id");

        state.shape.set("shape_id", shape_id);
        state.shape.fetch({reset: true}).done(function () {
          myMap.updateShapesLayer();
        });

        state.stops.trip_id = trip_id;
        state.stops.fetch({reset: true});
      });

		};

		return {
			createControls: createControls
		};
	});