define([
  'OpenLayers',
  'backbone',
  'views/map/styles'
  ],
  function (OpenLayers, Backbone, Styles) {
    'use strict';

    var View;

    View = Backbone.View.extend({

        initialize: function (options) {
          this.map = options.map;

          this.layer = new OpenLayers.Layer.Vector('External File');
          this.layer.id = 'file';

          this.kmlFormat = new OpenLayers.Format.KML({
            internalProjection: this.map.baseLayer.projection,
            externalProjection: new OpenLayers.Projection('EPSG:4326'),
            extractStyles: true,
            extractAttributes: true,
            maxDepth: 2
          });
          this.map.addLayer(this.layer);
        },

        read: function (content) {
          var features = this.kmlFormat.read(content);
          this.layer.removeAllFeatures();
          this.layer.addFeatures(features);
        }

    });

    return View;
});