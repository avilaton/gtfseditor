define([
  'OpenLayers',
  'backbone',
  'config',
  'views/map/styles'
  ],
  function (OpenLayers, Backbone, Config, Styles) {
    'use strict';

    var View = Backbone.View.extend({

        initialize: function (options) {
          var self = this;
          this.map = options.map;

          var refreshStrategy = new OpenLayers.Strategy.Refresh({
            // interval: 1000,
            force: true
          });

          OpenLayers.Format.GTFS = OpenLayers.Class(OpenLayers.Format, {
            read: function(body) {
              var obj = JSON.parse(body);

              var stops = obj.stops, stop,
              x, y, point,
              feature, features = [];

              for(var i=0,l=stops.length; i<l; i++) {
                stop = stops[i];
                x = stop.stop_lon;
                y = stop.stop_lat;
                point = new OpenLayers.Geometry.Point(x, y);
                feature = new OpenLayers.Feature.Vector(point, stop);
                features.push(feature);
              }
              return features;
              }
          });

          this.layer = new OpenLayers.Layer.Vector('Existing stops', {
            projection: new OpenLayers.Projection('EPSG:4326'),
            styleMap: Styles.bboxStyleMap,
            visibility: true,
            strategies: [
              new OpenLayers.Strategy.BBOX({resFactor: 1.2}),
              refreshStrategy
              ],
            protocol: new OpenLayers.Protocol.HTTP({
              format: new OpenLayers.Format.GTFS(),
              url: Config.server + 'api/stops.json',
              params: {
                filter: '',
                limit: 300
              }
            })
          });
          this.layer.id = 'bbox';

          refreshStrategy.activate();

          this.map.addLayer(this.layer);
        }

    });

    return View;
});