import Map from 'ol/map';
import Feature from 'ol/feature';
import Point from 'ol/geom/point';
import Vector from 'ol/source/vector';
import OSM from 'ol/source/osm';
import proj from 'ol/proj';
import VectorLayer from 'ol/layer/vector';
import TileLayer from 'ol/layer/tile';
import View from 'ol/view';
import olExtent from 'ol/extent';

var templateUrl = require('./stops.html');

function Controller(_, $http) {
    var ctrl = this;

    ctrl.$onInit = function () {
1
        var scaleFromCenter = function(extent, value) {
          var deltaX = ((extent[2] - extent[0]) / 2) * (value - 1);
          var deltaY = ((extent[3] - extent[1]) / 2) * (value - 1);
          extent[0] -= deltaX;
          extent[2] += deltaX;
          extent[1] -= deltaY;
          extent[3] += deltaY;
        };
        var bboxWithRatio = function(ratio) {
          var lastScaledExtent = [0, 0, 0, 0];
          return function(extent, resolution) {
            if (olExtent.containsExtent(lastScaledExtent, extent)) {
              return [extent];
            } else {
              lastScaledExtent = extent.slice();
              scaleFromCenter(lastScaledExtent, ratio);
              return [lastScaledExtent];
            }
          };
        };

        var source = new Vector({

            loader: function(extent, resolution, projection) {
                extent = olExtent.applyTransform(extent, proj.getTransform("EPSG:3857", "EPSG:4326"));
                var url = '/api/stops.json?bbox=' + extent.join(',');
                console.log(url);
                $http.get(url).then(function (res) {
                    var features = _.map(res.data, function (stop) {
                        var stopFeature = new Feature(stop);
                        stopFeature.setGeometry(new Point(proj.transform([stop.stop_lon,stop.stop_lat],
                            'EPSG:4326', 'EPSG:3857')));
                        // Setting the id allows the source to only add the missing features from the collection.
                        // http://stackoverflow.com/questions/40324406/migrating-openlayers-2-bbox-strategy-to-openlayers-3
                        stopFeature.setId(stop.stop_id);
                        return stopFeature;
                    });
                    source.addFeatures(features);
                });
            },
            projection: 'EPSG:4326',
            strategy: ol.loadingstrategy.bbox,
            // strategy: bboxWithRatio(2),
            // url: function (extent, resolution, projection) {
            //     extent = ol.extent.applyTransform(extent, ol.proj.getTransform("EPSG:3857", "EPSG:4326"));
            //     var url = '/api/stops.json?bbox=' + extent.join(',');
            //     return url
            // }
        });

        var view = new View({
                center: proj.fromLonLat([-64, -31.5]),
                zoom: 12
            });
        var vectorLayer = new VectorLayer({
                    title: 'Nodes',
                    source : source,
                });
        ctrl.map = new Map({
            layers: [
                new TileLayer({
                    source: new OSM()
                }),
                vectorLayer
            ],
            view: view
        });
        ctrl.map.on('moveend', function (e) {
            //source.clear();
            // source.refresh();
        });
    }
}

module.exports = function(ngModule) {
    ngModule.component('stops', {
        templateUrl: templateUrl,
        controller: Controller,
    });
};
