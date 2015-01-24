define([
  'OpenLayers',
  'backbone',
  'config',
  'views/map/drawStops',
  'views/map/stopsLayer',
  'views/map/styles'
  ],
  function (OpenLayers, Backbone, Config, DrawStopsView, StopsLayerView, Styles) {
    'use strict';

    var MapView = Backbone.View.extend({
      initialize: function(options){
        var self = this;

        self.stop = options.stop;

        this.map = new OpenLayers.Map(this.el, {
          controls : [
          new OpenLayers.Control.Navigation(),
          new OpenLayers.Control.PanZoomBar(),
          new OpenLayers.Control.LayerSwitcher({'ascending':false}),
          new OpenLayers.Control.ScaleLine(),
          new OpenLayers.Control.MousePosition({
            displayProjection: new OpenLayers.Projection("EPSG:4326")
          }),
          new OpenLayers.Control.Attribution()
          ]
        });

        this.baselayer = new OpenLayers.Layer.OSM('OSM Map');

        this.map.addLayer(this.baselayer);

        this.format = new OpenLayers.Format.GeoJSON({
          'internalProjection': this.map.baseLayer.projection,
          'externalProjection': new OpenLayers.Projection("EPSG:4326")
        });

        this.layers = {};

        this.panAndZoom();

        this.initializeChildViews();
        this.addControls();
        this.attachEventHandlers();
      },

      initializeChildViews: function () {
        var self = this;

        this.layers.stopsBboxLayer = new StopsLayerView({
          map: this.map
        });
        this.layers.drawStops = new DrawStopsView({
          format: this.format,
          map: this.map,
          model: self.stop
        });
        if (typeof (google) === 'object') {
          require(["views/map/googleLayer"], function (GoogleLayerView) {
            self.layers.google = new GoogleLayerView({
              map: self.map
            });
          })
        }
      },

      handleStopSelect: function (event) {
        var feature = event.feature;
        var geoJSON = this.format.write(feature);
        var featureObject = JSON.parse(geoJSON);

        if (event.type == "featureselected") {
          this.stop.feature = feature;
          this.stop.set(feature.attributes);
        } else if (event.type == "featureunselected") {
          this.stop.clear();
        };
      },

      attachEventHandlers: function () {
        var self = this;

        this.layers.stopsBboxLayer.layer.events.register('featureselected', self,
          self.handleStopSelect);
        this.layers.stopsBboxLayer.layer.events.register('featureunselected', self,
          self.handleStopSelect);
      },

      addControls: function () {
        var self = this;
        var controls = {};

        this.controls = controls;

        controls.selectStops = new OpenLayers.Control.SelectFeature(
          [self.layers.stopsBboxLayer.layer, self.layers.drawStops.layer],
          {
            id: 'selectStops',
            clickout: true, toggle: false,
            multiple: false, hover: false
          });
        this.map.addControl(controls.selectStops);

        controls.modifyStops = new OpenLayers.Control.ModifyFeature(
          self.layers.drawStops.layer,
          {
            id: 'modifyStops',
            allowSelection: true
          });
        this.map.addControl(controls.modifyStops);

        controls.drawStops = new OpenLayers.Control.DrawFeature(self.layers.drawStops.layer,
          OpenLayers.Handler.Point);
        this.map.addControl(controls.drawStops);

        controls.selectStops.activate();

        controls.getSelectedFeature = function () {
            var layers = self.controls.selectStops.layers;
            var feature = null;
            for (var i = 0; i < layers.length; i++) {
              console.log(layers[i].selectedFeatures);
              if (layers[i].selectedFeatures) {
                feature = layers[i].selectedFeatures[0];
              };
            };
            return feature;
        };

        controls.copyFeature = function (feature, toLayer) {
          self.layers[toLayer].layer.addFeatures([feature]);
        }

        controls.clearEdits = function () {
          self.layers.drawStops.layer.removeAllFeatures();
        }
      },

      activateControl: function (controlId) {
        this.controls.drawStops.deactivate();
        this.controls.modifyStops.deactivate();
        this.controls.selectStops.deactivate();

        if (this.controls.hasOwnProperty(controlId)) {
          this.controls[controlId].activate();
        };
      },

      panAndZoom: function (lon, lat, zoom) {
        var lon = lon || -64.1857371;
        var lat = lat || -31.4128832;
        var zoom = zoom || 4;

        this.map.setCenter(
          new OpenLayers.LonLat(lon, lat).transform(
            new OpenLayers.Projection("EPSG:4326"),
            this.map.getProjectionObject()
            ), zoom
          );
      }

    }); 

return MapView;
});
