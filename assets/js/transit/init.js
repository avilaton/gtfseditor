define([
	"transit/collections/routes",
	"transit/views/routesSelect",
	"transit/collections/trips",
	"transit/views/tripsSelect",
	"transit/views/shapesToolbox",
	"transit/models/shape",
	"transit/model",
	"transit/maps",
	"transit/models/state"
	], function (RoutesCollection, RoutesSelectView, TripsCollection, 
		TripsSelectView, ShapesToolboxView, ShapeModel,
		oldModel, Maps, StateModel) {

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

			state.routes.on("route_selected", function (selectedModel) {
				oldModel.selected.route_id = selectedModel.get("route_id");
				oldModel.selected.trip_id = '';
				oldModel.selected.shape_id = '';
				Maps.update();
			});

			state.trips.on("trip_selected", function (selectedModel) {
				var shape_id = selectedModel.get("shape_id");
				oldModel.selected.trip_id = selectedModel.get("trip_id");
				oldModel.selected.shape_id = selectedModel.get("shape_id");
				state.shape.set("shape_id", shape_id);
				state.shape.fetch().done(function () {
          Maps.update();
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