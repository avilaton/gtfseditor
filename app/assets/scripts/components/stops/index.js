var templateUrl = require('./stops.html');

function Controller(_, $http) {
    var ctrl = this;

    ctrl.$onInit = function () {

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
            if (ol.extent.containsExtent(lastScaledExtent, extent)) {
              return [extent];
            } else {
              lastScaledExtent = extent.slice();
              scaleFromCenter(lastScaledExtent, ratio);
              return [lastScaledExtent];
            }
          };
        };

        var source = new ol.source.Vector({

            loader: function(extent, resolution, projection) {
                extent = ol.extent.applyTransform(extent, ol.proj.getTransform("EPSG:3857", "EPSG:4326"));
                var url = '/api/stops.json?bbox=' + extent.join(',');
                console.log(url);
                $http.get(url).then(function (res) {
                    var features = _.map(res.data, function (stop) {
                        var stopFeature = new ol.Feature(stop);
                        stopFeature.setGeometry(new ol.geom.Point(ol.proj.transform([stop.stop_lon,stop.stop_lat],
                            'EPSG:4326', 'EPSG:3857')));
                        return stopFeature;
                    });
                    source.addFeatures(features);
                });
            },
            projection: 'EPSG:4326',
            // strategy: ol.loadingstrategy.bbox,
            strategy: bboxWithRatio(1.1),
            url: function (extent, resolution, projection) {
                extent = ol.extent.applyTransform(extent, ol.proj.getTransform("EPSG:3857", "EPSG:4326"));
                var url = '/api/stops.json?bbox=' + extent.join(',');
                return url
            }
        });

        var view = new ol.View({
                center: ol.proj.fromLonLat([-64, -31.5]),
                zoom: 9
            });
        var vectorLayer = new ol.layer.Vector({
                    title: 'Nodes',
                    source : source,
                });
        ctrl.map = new ol.Map({
            layers: [
                new ol.layer.Tile({
                    source: new ol.source.OSM()
                }),
                vectorLayer
            ],
            view: view
        });
        ctrl.map.on('moveend', function (e) {
            source.clear();
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