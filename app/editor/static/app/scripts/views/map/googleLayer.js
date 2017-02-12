define([
  "OpenLayers",
  "backbone",
  'async!http://maps.google.com/maps/api/js?sensor=false'
  ],
  function (OpenLayers, Backbone) {
    'use strict';

    var View;

    View = Backbone.View.extend({

        initialize: function (options) {
            var self = this;
            this.map = options.map;

            if (typeof (google) === 'object') {
              this.googleMapsLayer = new OpenLayers.Layer.Google('Google Streets', {
                numZoomLevels: 22,
                animationEnabled: false
              });
              this.map.addLayer(this.googleMapsLayer);

              this.googleSatelliteLayer = new OpenLayers.Layer.Google('Google Satellite', {
                type: google.maps.MapTypeId.SATELLITE,
                numZoomLevels: 22,
                animationEnabled: false
              });
              this.map.addLayer(this.googleSatelliteLayer);
              this.googleSatelliteLayer.mapObject.setTilt(0);
            };

        }

    });

    return View;
});