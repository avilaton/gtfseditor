define([
  "transit/models/shape",
	"transit/models/stop",
  "transit/collections/routes",
  "transit/collections/trips",
  "transit/collections/stops",
  "transit/views/filter",
  "transit/views/routesSelect",
  "transit/views/tripsSelect",
  "transit/views/shapesToolbox",
  "transit/views/sequenceToolbox",
  "transit/views/stopData",
  "transit/views/map"
	], 
  function (ShapeModel, StopModel, RoutesCollection, TripsCollection, 
    StopsCollection, FilterView, RoutesSelectView, TripsSelectView, 
    ShapesToolboxView, SequenceToolboxView, StopDataView, MapView) {

		function createControls () {
			var state = window.app.state;
			
			// console.log("create controls");

      state.routes = new RoutesCollection();
      state.trips = new TripsCollection();
      state.shape = new ShapeModel();
      state.stops = new StopsCollection();
      state.stop = new StopModel();

			state.routes.fetch();


      var routeSelector = new RoutesSelectView({
        collection: state.routes
      });

      var tripsSelector = new TripsSelectView({
        routesCollection: state.routes,
        collection: state.trips
      });

      var myShapesToolbox = new ShapesToolboxView({
        model: state.shape
      });

      var mySequenceToolbox = new SequenceToolboxView({
        collection: state.stops
      });

      var myStopData = new StopDataView({
        model: state.stop
      });

      var myMap = new MapView({
        shape: state.shape,
        stops: state.stops,
        stop: state.stop
      });


      myMap.panAndZoom();

      myMap.addBboxLayer();
      myMap.addShapesLayer();
      myMap.addStopsLayer();
      myMap.addOldControls();
      myMap.attachEventHandlers();

      var filterBox = new FilterView({
        bboxLayer: myMap.bboxLayer
      });
      
      state.trips.on("trip_selected", function (selectedModel) {
        var trip_id = selectedModel.get("trip_id");
        var shape_id = selectedModel.get("shape_id");

        state.shape.set("shape_id", shape_id);
        state.shape.fetch().done(function () {
          myMap.updateShapesLayer();
        });

        state.stops.trip_id = trip_id;
        state.stops.fetch().done(function () {
          myMap.updateStopsLayer();
        });
      });

		};

		return {
			createControls: createControls
		};
	});