var templateUrl = require('./trip.html');

function Controller(Route, Trip, TripShape, TripStops, TripStopsService, $routeParams, $timeout, _) {
    var ctrl = this;

    ctrl.route = Route.get({routeId: $routeParams.routeId});

    ctrl.trip = Trip.get({tripId: $routeParams.tripId}, function (trip) {
      // console.log(trip);
    });

    ctrl.shape = TripShape.get({tripId: $routeParams.tripId}, function (shape) {
        var coordinates = _.map(shape.coordinates, function (point) {
            return ol.proj.transform([point[0], point[1]], 'EPSG:4326', 'EPSG:3857')
        });
        var shapeFeature = new ol.Feature({
            geometry: new ol.geom.LineString(coordinates),
        });
        ctrl.tripShapeFeatures.push(shapeFeature);
    });

    ctrl.stops = TripStops.get({tripId: $routeParams.tripId, embed: 'true'}, function (stops) {
        _.each(stops, function (trip_stop) {
            var stop = trip_stop._stop;

            var stopFeature = new ol.Feature(trip_stop);
            stopFeature.setGeometry(new ol.geom.Point(ol.proj.transform([stop.stop_lon,stop.stop_lat],
                'EPSG:4326', 'EPSG:3857')));

            ctrl.tripStopFeatures.push(stopFeature);
        });
    });

    ctrl.tripStopFeatures = new ol.Collection();
    ctrl.tripShapeFeatures = new ol.Collection();

    var stopStyle = new ol.style.Style({
        image: new ol.style.Circle({
            fill: new ol.style.Fill({
                color: '#FFF'
            }),
            stroke: new ol.style.Stroke({
                color: '#000',
                width: 2
            }),
            radius: 5
        })
    });

    var selectedStopStyle = new ol.style.Style({
        image: new ol.style.Circle({
            fill: new ol.style.Fill({
                color: '#F00'
            }),
            stroke: new ol.style.Stroke({
                color: '#000',
                width: 2
            }),
            radius: 6
        })
    });

    var shapeStyle = new ol.style.Style({
        stroke: new ol.style.Stroke({
            color: 'blue',
            width: 4
        })
    });

    ctrl.$onInit = function () {
        var tripStopsLayer = new ol.layer.Vector({
            source: new ol.source.Vector({features: ctrl.tripStopFeatures}),
            style: stopStyle
        });

        var tripShapeLayer = new ol.layer.Vector({
            source: new ol.source.Vector({features: ctrl.tripShapeFeatures}),
            style: shapeStyle
        });

        var selectStop = new ol.interaction.Select({
            condition: ol.events.condition.click,
            style: selectedStopStyle,
            layers: [tripStopsLayer]
        });

        ctrl.map = new ol.Map({
            layers: [
                new ol.layer.Tile({
                    source: new ol.source.OSM()
                }),
                tripShapeLayer,
                tripStopsLayer,
            ],
            view: new ol.View({
                center: ol.proj.fromLonLat([-64, -31.5]),
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