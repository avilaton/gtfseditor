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

            this.layer = new OpenLayers.Layer.Vector('Gpx', {
              strategies: [new OpenLayers.Strategy.Fixed()],
              protocol: new OpenLayers.Protocol.HTTP({
                url: "",
                format: new OpenLayers.Format.GPX()
              }),
              styleMap: Styles.gpxStyleMap,
              projection: new OpenLayers.Projection("EPSG:4326")
            });
            this.layer.id = 'gpx';
            this.map.addLayer(this.layer);
        }

    });

    return View;
});