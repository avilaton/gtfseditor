define([
	"transit/collections/routes",
	"transit/views/routesSelect",
	"transit/collections/trips",
	"transit/views/tripsSelect",
	"transit/model",
	"transit/maps"
	], function (RoutesCollection, RoutesSelectView, TripsCollection, TripsSelectView, StateModel, Maps) {

		function createControls () {
			console.log("create controls");

	    // porting to backbone
	    var myRoutes = new RoutesCollection();
	    myRoutes.fetch();
	    
	    var myTrips = new TripsCollection();
 
	    var routeSelector = new RoutesSelectView({
	    	collection: myRoutes
	    });

	    var tripsSelector = new TripsSelectView({
	    	routesCollection: myRoutes,
	    	collection: myTrips
	    });
	    
	    myRoutes.on("route_selected", function (selectedModel) {
	    	StateModel.selected.route_id = selectedModel.get("route_id");
	    	StateModel.selected.trip_id = '';
	    	StateModel.selected.shape_id = '';
	    	Maps.update();
	    });

	    myTrips.on("trip_selected", function (selectedModel) {
	    	StateModel.selected.trip_id = selectedModel.get("trip_id");
	    	StateModel.selected.shape_id = selectedModel.get("shape_id");
	    	Maps.update();
	    });

	    // var topBar = new TopBarView();
	};

	return {
		createControls: createControls
	};
});