var templateUrl = require('./home.html');

function Controller(Stats) {
    var ctrl = this;
    ctrl.stats = Stats.get();
}

module.exports = function(ngModule) {
    ngModule.component('home', {
        templateUrl: templateUrl,
        controller: Controller
    });
};