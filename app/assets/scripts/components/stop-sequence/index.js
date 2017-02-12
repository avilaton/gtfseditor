var templateUrl = require('./stop-sequence.html');

function Controller(Route, RouteTrips, $routeParams, TripStopsService) {
    var ctrl = this;

    console.log(ctrl.stops);

    ctrl.saveTripStops = function () {
      TripStopsService.get(1);
    };
}

module.exports = function(ngModule) {
    ngModule.component('stopSequence', {
        templateUrl: templateUrl,
        controller: Controller,
        bindings: {
          stops: '='
        }
    });
};