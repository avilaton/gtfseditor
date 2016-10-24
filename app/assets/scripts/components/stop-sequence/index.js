var templateUrl = require('./stop-sequence.html');

function Controller(Route, RouteTrips, $routeParams) {
    var ctrl = this;

    console.log(ctrl.stops);

    ctrl.saveTripStops = function () {
      ctrl.stops.$save();
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