define([
  "OpenLayers",
  "backbone",
  "views/map/styles"
  ],
  function (OpenLayers, Backbone, Styles) {
    'use strict';

    var View;

    View = Backbone.View.extend({

        initialize: function (options) {
            var self = this;
            this.map = options.map;
            this.format = options.format;

            this.layer = new OpenLayers.Layer.Vector('Draw stops', {
              projection: new OpenLayers.Projection('EPSG:4326'),
              styleMap: Styles.drawStopsStyleMap
            });
            this.layer.id = 'drawStops';

            this.map.addLayer(self.layer);
            this.bindEvents();
        },

        bindEvents: function () {
            var self = this;
            this.layer.events.register('featureselected', self,
                self.handleStopSelect);
            this.layer.events.register('featureunselected', self,
                self.handleStopSelect);
            this.layer.events.register('featuremodified', self,
                self.onFeatureModified);

            this.layer.events.register('featureadded', self.layer, function (event) {
                this.features.forEach(function (item) {
                    if (item.id !== event.feature.id) {
                        item.layer.removeFeatures([item]);
                    }
                });
                self.onFeatureModified(event);
            });
        },

        onFeatureModified: function (event) {
            var feature = event.feature;
            var geoJSON = this.format.write(feature);
            var featureObject = JSON.parse(geoJSON);
            var coords = feature.geometry.getBounds().getCenterLonLat();

            this.model.feature = feature;
            this.model.set('stop_lon', featureObject.geometry.coordinates[0]);
            this.model.set('stop_lat', featureObject.geometry.coordinates[1]);
        },

        handleStopSelect: function (event) {
            var feature = event.feature;
            var geoJSON = this.format.write(feature);
            var featureObject = JSON.parse(geoJSON);

            if (event.type == "featureselected") {
                this.model.feature = feature;
                this.model.set(feature.attributes);
            } else if (event.type == "featureunselected") {
                console.log
                this.model.clear();
            };
        },

    });

    return View;
});