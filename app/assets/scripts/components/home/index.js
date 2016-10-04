var templateUrl = require('./home.html');
var angular = require('angular');

function Controller() {
    var ctrl = this;
}

module.exports = function(ngModule) {
    ngModule.component('home', {
        templateUrl: templateUrl,
        controller: Controller
    });
};