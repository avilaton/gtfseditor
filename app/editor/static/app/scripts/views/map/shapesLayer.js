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
            var self = this;
            this.map = options.map;
            this.format = options.format;

            this.layer = new OpenLayers.Layer.Vector('Route shape', {
              styleMap: Styles.routesStyleMap
            });
            this.layer.id = 'shapes';

            this.map.addLayer(self.layer);
            this.listenTo(this.model, 'change:coordinates', this.onShapeChange, this);
        },

        onShapeChange: function () {
            console.log('shape coordinates changed');
        }

    });

    return View;
});