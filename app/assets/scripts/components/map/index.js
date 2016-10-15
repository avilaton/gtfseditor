var templateUrl = require('./map.html');
var ol = require('openlayers');

function Controller(Route, Trip, TripShape, TripStops, $routeParams) {
    var ctrl = this;

}

module.exports = function(ngModule) {
    ngModule.directive('map', function () {
      return {
        restrict: 'E',
        scope: {},
        templateUrl: templateUrl,
        controller: Controller,
        controllerAs: '$ctrl',
        bindToController: true,
        link: function (scope, element, attrs) {
          var map = new ol.Map({
            target: 'map',
            layers: [
              new ol.layer.Tile({
                source: new ol.source.OSM()
              })
            ],
            view: new ol.View({
              center: ol.proj.fromLonLat([-64, -32]),
              zoom: 6
            })
          });
        }
      };
    });
};