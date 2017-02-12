var templateUrl = require('./route.html');

function Controller(Route, RouteTrips, $routeParams) {
    var ctrl = this;
    ctrl.route = Route.get({routeId: $routeParams.routeId});
    ctrl.trips = RouteTrips.get({routeId: $routeParams.routeId});
}

module.exports = function(ngModule) {
    ngModule.component('route', {
        templateUrl: templateUrl,
        controller: Controller
    });
};