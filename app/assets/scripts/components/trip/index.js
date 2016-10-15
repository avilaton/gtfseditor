var templateUrl = require('./trip.html');

function Controller(Route, Trip, TripShape, TripStops, $routeParams) {
    var ctrl = this;
    ctrl.route = Route.get({routeId: $routeParams.routeId});
    ctrl.trip = Trip.get({tripId: $routeParams.tripId}, function (trip) {
      // console.log(trip);
    });
    ctrl.shape = TripShape.get({tripId: $routeParams.tripId}, function (shape) {
      // console.log(shape);
    });
    ctrl.stops = TripStops.get({tripId: $routeParams.tripId}, function (stops) {
      // console.log(stops);
    });

}

module.exports = function(ngModule) {
    ngModule.component('trip', {
        templateUrl: templateUrl,
        controller: Controller
    });
};