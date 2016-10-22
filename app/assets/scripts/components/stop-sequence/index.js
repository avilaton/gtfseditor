var templateUrl = require('./stop-sequence.html');

function Controller(Route, RouteTrips, $routeParams) {
    var ctrl = this;
    console.log(ctrl);
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