var templateUrl = require('./routes.html');

function Controller(Routes) {
    var ctrl = this;
    ctrl.routes = Routes.get();
}

module.exports = function(ngModule) {
    ngModule.component('routes', {
        templateUrl: templateUrl,
        controller: Controller
    });
};