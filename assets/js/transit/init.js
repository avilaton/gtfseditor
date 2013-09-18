define([
	"transit/models/shape",
  "transit/collections/routes",
  "transit/collections/trips",
  "transit/collections/stops",
  "transit/views/routesSelect",
  "transit/views/tripsSelect",
  "transit/views/shapesToolbox",
  "transit/views/map"
	], 
  function (ShapeModel, RoutesCollection, TripsCollection, StopsCollection,
    RoutesSelectView, TripsSelectView, ShapesToolboxView, MapView) {

		function createControls () {
			var state = window.app.state;
			
			console.log("create controls");

      state.routes = new RoutesCollection();
			state.stops = new StopsCollection();

      state.trips = new TripsCollection();
      state.shape = new ShapeModel();

			state.routes.fetch();

			var routeSelector = new RoutesSelectView({
				collection: state.routes
			});

			var tripsSelector = new TripsSelectView({
				routesCollection: state.routes,
				collection: state.trips
			});

      var myMap = new MapView({
        shape: state.shape,
        stops: state.stops
      });

      myMap.panAndZoom();

      myMap.addBboxLayer();
      myMap.addShapesLayer();
      myMap.addStopsLayer();
      myMap.addOldControls();

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

      var myShapesToolbox = new ShapesToolboxView({
        model: state.shape
      });

		};

		return {
			createControls: createControls
		};
	});