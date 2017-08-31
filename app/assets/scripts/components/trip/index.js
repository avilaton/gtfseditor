import Map from 'ol/map';
import Feature from 'ol/feature';
import Collection from 'ol/collection';
import Select from 'ol/interaction/select';
import Point from 'ol/geom/point';
import LineString from 'ol/geom/linestring';
import Vector from 'ol/source/vector';
import OSM from 'ol/source/osm';
import Style from 'ol/style/style';
import Circle from 'ol/style/circle';
import Fill from 'ol/style/fill';
import Stroke from 'ol/style/stroke';
import proj from 'ol/proj';
import VectorLayer from 'ol/layer/vector';
import TileLayer from 'ol/layer/tile';
import View from 'ol/view';
import olExtent from 'ol/extent';
import condition from 'ol/events/condition';
console.log(condition);

var templateUrl = require('./trip.html');

function Controller(Route, Trip, TripShape, TripStops, TripStopsService, $routeParams, $timeout, _) {
    var ctrl = this;

    ctrl.route = Route.get({routeId: $routeParams.routeId});

    ctrl.trip = Trip.get({tripId: $routeParams.tripId}, function (trip) {
      // console.log(trip);
    });

    ctrl.shape = TripShape.get({tripId: $routeParams.tripId}, function (shape) {
        var coordinates = _.map(shape.coordinates, function (point) {
            return proj.transform([point[0], point[1]], 'EPSG:4326', 'EPSG:3857')
        });
        var shapeFeature = new Feature({
            geometry: new LineString(coordinates),
        });
        ctrl.tripShapeFeatures.push(shapeFeature);
    });

    ctrl.stops = TripStops.get({tripId: $routeParams.tripId, embed: 'true'}, function (stops) {
        _.each(stops, function (trip_stop) {
            var stop = trip_stop._stop;

            var stopFeature = new Feature(trip_stop);
            stopFeature.setGeometry(new Point(proj.transform([stop.stop_lon,stop.stop_lat],
                'EPSG:4326', 'EPSG:3857')));

            ctrl.tripStopFeatures.push(stopFeature);
        });
    });

    ctrl.tripStopFeatures = new Collection();
    ctrl.tripShapeFeatures = new Collection();

    var stopStyle = new Style({
        image: new Circle({
            fill: new Fill({
                color: '#FFF'
            }),
            stroke: new Stroke({
                color: '#000',
                width: 2
            }),
            radius: 5
        })
    });

    var selectedStopStyle = new Style({
        image: new Circle({
            fill: new Fill({
                color: '#F00'
            }),
            stroke: new Stroke({
                color: '#000',
                width: 2
            }),
            radius: 6
        })
    });

    var shapeStyle = new Style({
        stroke: new Stroke({
            color: 'blue',
            width: 4
        })
    });

    ctrl.$onInit = function () {
        var tripStopsLayer = new VectorLayer({
            source: new Vector({features: ctrl.tripStopFeatures}),
            style: stopStyle
        });

        var tripShapeLayer = new VectorLayer({
            source: new Vector({features: ctrl.tripShapeFeatures}),
            style: shapeStyle
        });

        var selectStop = new Select({
            condition: condition.click,
            style: selectedStopStyle,
            layers: [tripStopsLayer]
        });

        ctrl.map = new Map({
            layers: [
                new TileLayer({
                    source: new OSM()
                }),
                tripShapeLayer,
                tripStopsLayer,
            ],
            view: new View({
                center: proj.fromLonLat([-64, -31.5]),
                zoom: 9
            })
        });
        ctrl.map.addInteraction(selectStop);
        selectStop.on('select', function(evt) {
            var feature = evt.selected[0];
            $timeout(function () {
                ctrl.selectedStop = feature ? feature.getProperties(): undefined;
            });
        });

        // Cause a repaint because something funky prevents the first paint (has to do with the
        // ui-tab component)
        $timeout(function () {ctrl.map.updateSize();});
    };

    ctrl.saveTripStops = function () {
        var payload = _.map(ctrl.stop_times, function (stop_time) {
            var stop_time = _.clone(stop_time);
            delete stop_time._stop;
            return stop_time;
        });
        TripStopsService.update($routeParams.tripId, payload);
    };

    TripStopsService.get($routeParams.tripId).then(function (res) {
        ctrl.stop_times = res.data;
    });
}

module.exports = function(ngModule) {
    ngModule.component('trip', {
        templateUrl: templateUrl,
        controller: Controller
    });
};
