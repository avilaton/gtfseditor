var templateUrl = require('./routes.html');

function Controller(Routes, Agencies, _) {
    var ctrl = this;
    ctrl.routes = Routes.get();
    Agencies.get(function (agencies) {
      ctrl.agencies = _.keyBy(agencies, 'agency_id');
    });
}

module.exports = function(ngModule) {
    ngModule.component('routes', {
        templateUrl: templateUrl,
        controller: Controller
    });
};