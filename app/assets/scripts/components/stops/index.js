var templateUrl = require('./stops.html');

function Controller() {
    var ctrl = this;

    ctrl.$onInit = function () {
        ctrl.map = new ol.Map({
            layers: [
                new ol.layer.Tile({
                    source: new ol.source.OSM()
                }),
            ],
            view: new ol.View({
                center: ol.proj.fromLonLat([-64, -31.5]),
                zoom: 9
            })
        });
    }
}

module.exports = function(ngModule) {
    ngModule.component('stops', {
        templateUrl: templateUrl,
        controller: Controller,
    });
};