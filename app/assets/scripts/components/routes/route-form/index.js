var templateUrl = require('./route-form.html');

function Controller(Route, RouteTrips, $routeParams, Agencies) {
    var ctrl = this;
    ctrl.route = Route.get({routeId: $routeParams.routeId});
    ctrl.trips = RouteTrips.get({routeId: $routeParams.routeId});
    Agencies.get(function (agencies) {
        ctrl.agencies = _.keyBy(agencies, 'agency_id');
    });
}

module.exports = function(ngModule) {
    ngModule.component('routeForm', {
        templateUrl: templateUrl,
        controller: Controller
    });
};