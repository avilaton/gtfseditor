define([
  "OpenLayers",
  "backbone",
  'config',
  "views/map/drawStops",
  "views/map/kmlLayer",
  "views/map/styles"
  ],
  function (OpenLayers, Backbone, Config, DrawStopsView, KmlLayerView, Styles) {
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
        this.addBboxLayer();

        this.initializeChildViews();
        
        this.addControls();
        this.attachEventHandlers();
      },

      initializeChildViews: function () {
        var self = this;
        this.layers.drawStops = new DrawStopsView({
          format: this.format,
          map: this.map,
          model: self.stop
        });
        this.layers.kml = new KmlLayerView({
          map: this.map
        });
        if (typeof (google) === 'object') {
          require(["views/map/googleLayer"], function (GoogleLayerView) {
            self.layers.google = new GoogleLayerView({
              map: self.map
            });
          })
        }
      },

      addBboxLayer: function () {
        var self = this;

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

        this.bboxLayer = new OpenLayers.Layer.Vector('Existing stops', {
          projection: new OpenLayers.Projection('EPSG:4326'),
          styleMap: Styles.bboxStyleMap,
          visibility: true,
          strategies: [
            new OpenLayers.Strategy.BBOX({resFactor: 2.0}),
            refreshStrategy
            ],
          protocol: new OpenLayers.Protocol.HTTP({
            format: new OpenLayers.Format.GTFS(),
            url: Config.server + 'api/bbox.json',
            params: {filter:''}
          })
        });
        this.bboxLayer.id = 'bbox';

        refreshStrategy.activate();

        this.map.addLayer(self.bboxLayer);
      },

      onBboxFeatureSelected: function (event) {
        this.handleStopSelect(event);
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

      onMultipleFeatureSelected: function (event) {
        console.log(event);
      },

      attachEventHandlers: function () {
        var self = this;

        this.bboxLayer.events.register('featureselected', self,
          self.onBboxFeatureSelected);
        this.bboxLayer.events.register('featureunselected', self,
          self.onBboxFeatureSelected);

        // this.bboxLayer.events.on({
        //   'featureselected': self.onMultipleFeatureSelected,
        //   'featureunselected': self.onMultipleFeatureSelected,
        //   scope: self.bboxLayer
        // });
      },

      addSelectControl: function (layerIds) {
        var self = this,
        layers = [],
        control;

        _.each(self.collection.models, function (layerModel) {
          var layer = self.map.getLayer(layerModel.attributes.filename);
          layers.push(layer);
          layer.events.on({
            "featureselected": self.selectedFeature,
            "featureunselected": self.selectedFeature, 
            scope: self
          });
          layer.events.fallThrough = true;
        });

        control = new OpenLayers.Control.SelectFeature(
          layers,
          {
            clickout: true, toggle: true,
            multiple: false, hover: false
          }
          );
        control.id = "selectControl";

        control.handlers['feature'].stopDown = false;
        control.handlers['feature'].stopUp = false;

        self.map.addControl(control);
        control.activate();
      },

      addControls: function () {
        var self = this;
        var controls = {};

        this.controls = controls;

        controls.selectStops = new OpenLayers.Control.SelectFeature(
          [self.bboxLayer, self.layers.drawStops.layer, self.layers.kml.layer],
          {
            id: 'selectStops',
            clickout: true, toggle: false,
            multiple: false, hover: false
          });
        this.map.addControl(controls.selectStops);

        controls.selectMultiple = new OpenLayers.Control.SelectFeature(
          self.bboxLayer,
          {
            id: 'selectMultiple',
            multiple: true, multipleKey: 'shiftKey', 
            box: true,
            clickout: true, toggle: true,
            hover: false
          });
        this.map.addControl(controls.selectMultiple);

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
        // this.controls.modifyBbox.deactivate();
        this.controls.modifyStops.deactivate();
        this.controls.selectMultiple.deactivate();
        this.controls.selectStops.deactivate();

        if (this.controls.hasOwnProperty(controlId)) {
          this.controls[controlId].activate();
        };
      },

      panAndZoom: function (lon, lat, zoom) {
        var lon = lon || -64.1857371;
        var lat = lat || -31.4128832;
        var zoom = zoom || 12;

        this.map.setCenter(
          new OpenLayers.LonLat(lon, lat).transform(
            new OpenLayers.Projection("EPSG:4326"),
            this.map.getProjectionObject()
            ), zoom
          );
      },

      toJSON: function (features) {
        var result = this.format.write(features);
        console.log("feature to json", result);
      }

    }); 

return MapView;
});
