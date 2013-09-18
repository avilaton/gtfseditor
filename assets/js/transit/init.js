define([
	"transit/collections/routes",
	"transit/views/routesSelect",
	"transit/collections/trips",
	"transit/views/tripsSelect",
	"transit/views/shapesToolbox",
	"transit/models/shape",
	"transit/model",
	"transit/maps",
  "transit/views/map",
	"transit/models/state"
	], function (RoutesCollection, RoutesSelectView, TripsCollection, 
		TripsSelectView, ShapesToolboxView, ShapeModel,
		oldModel, Maps, MapView, StateModel) {

		function createControls () {
			var state = window.app.state;
			
			console.log("create controls");

			state.routes = new RoutesCollection();
			state.routes.fetch();
			state.trips = new TripsCollection();
		  state.shape = new ShapeModel();

			var routeSelector = new RoutesSelectView({
				collection: state.routes
			});

			var tripsSelector = new TripsSelectView({
				routesCollection: state.routes,
				collection: state.trips
			});

      var myMap = new MapView({
        shape: state.shape
      });

      myMap.panAndZoom();

      myMap.addShapesLayer();
      myMap.addBboxLayer();

      state.trips.on("trip_selected", function (selectedModel) {
        var shape_id = selectedModel.get("shape_id");

        state.shape.set("shape_id", shape_id);
        state.shape.fetch().done(function () {
          // Maps.update();
          myMap.updateShapesLayer();
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