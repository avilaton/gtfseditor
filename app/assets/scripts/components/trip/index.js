var templateUrl = require('./trip.html');

function Controller(Route, Trip, TripShape, TripStops, $routeParams, $timeout) {
    var ctrl = this;
    ctrl.route = Route.get({routeId: $routeParams.routeId});
    ctrl.trip = Trip.get({tripId: $routeParams.tripId}, function (trip) {
      // console.log(trip);
    });
    ctrl.shape = TripShape.get({tripId: $routeParams.tripId}, function (shape) {
      // console.log(shape);
    });
    ctrl.stops = TripStops.get({tripId: $routeParams.tripId}, function (stops) {
      // console.log(stops);
    });

    ctrl.$onInit = function () {
        ctrl.map = new ol.Map({
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
        // Cause a repaint because something funky prevents the first paint (has to do with the
        // ui-tab component)
        $timeout(function () {ctrl.map.updateSize();});
    };
}

module.exports = function(ngModule) {
    ngModule.component('trip', {
        templateUrl: templateUrl,
        controller: Controller
    });
};