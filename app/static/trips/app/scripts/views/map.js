define([
  'OpenLayers',
  'backbone',
  'config',
  'views/map/drawStops',
  'views/map/kmlLayer',
  'views/map/stopsLayer',
  'views/map/styles',
  'views/map/shapesLayer',
  'views/map/fileLayer'
  ],
  function (OpenLayers, Backbone, Config, DrawStopsView, KmlLayerView,
    StopsLayerView, Styles, ShapesLayerView, FileLayerView) {
    'use strict';

    var MapView = Backbone.View.extend({
      initialize: function(options){
        var self = this;

        self.shape = options.shape;
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

        this.bindEvents();


        this.panAndZoom();

        this.initializeChildViews();

        this.addControls();
        this.attachEventHandlers();
      },

      initializeChildViews: function () {
        var self = this;
        this.layers = {};

        this.layers.fileLayer = new FileLayerView({
          map: this.map
        });

        this.layers.shapesLayer = new ShapesLayerView({
          map: this.map,
          model: this.shape
        });

        this.shapesLayer = this.layers.shapesLayer.layer;

        this.layers.stopsBboxLayer = new StopsLayerView({
          map: this.map
        });

        this.addNotesLayer();
        this.addStopsLayer();

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

      bindEvents: function () {
        var self = this;
        self.shape.on("reset destroy", self.updateShapesLayer, self);
        this.listenTo(this.shape, 'change:coordinates', this.updateShapesLayer, this);

        this.collection.on("change reset add remove", self.updateStopsLayer, self);
        self.collection.on("trip_stop_selected", self.selectTripStop, self);
      },

      updateShapesLayer: function () {

        var self = this;
        var ft = this.format.read(self.shape.toGeoJSON());
        this.shapesLayer.removeAllFeatures();
        if (ft) {
          this.shapesLayer.addFeatures(ft);
        }
        self.shapesLayer.refresh();
        this.updateNotesLayer();
      },

      updateShapeModel: function () {
        var self = this;
        var shapeJSON = this.format.write(self.shapesLayer.features, true);
        var shapeObj = JSON.parse(shapeJSON);
        this.shape.set('coordinates', shapeObj.features[0].geometry.coordinates);
        return;
      },

      updateStopsLayer: function () {
        var self = this;
        var ft = this.format.read(JSON.stringify(self.collection.toGeoJSON()));
        this.stopsLayer.removeAllFeatures();
        this.stopsLayer.addFeatures(ft);
        this.stopsLayer.refresh();
        this.map.zoomToExtent(this.stopsLayer.getDataExtent());
      },

      updateNotesLayer: function () {
        var startFeature = this.notesLayer.getFeatureById('routeStart'),
          endFeature = this.notesLayer.getFeatureById('routeEnd'),
          route = this.shapesLayer.features[0],
          startPoint, endPoint;

        if (startFeature) {
          this.notesLayer.removeFeatures(startFeature);
        }
        if (endFeature) {
          this.notesLayer.removeFeatures(endFeature);
        }

        if (!route) return;
        startPoint = route.geometry.components[0];
        endPoint = route.geometry.components[route.geometry.components.length - 1];

        startFeature = new OpenLayers.Feature.Vector(startPoint);
        startFeature.id = 'routeStart';
        startFeature.attributes.type = 'Start';

        endFeature = new OpenLayers.Feature.Vector(endPoint);
        endFeature.id = 'routeEnd';
        endFeature.attributes.type = 'End';

        this.notesLayer.addFeatures([startFeature, endFeature]);
      },

      addNotesLayer: function () {
        this.notesLayer = new OpenLayers.Layer.Vector('Notes', {
          styleMap: Styles.notesStyleMap
        });
        this.notesLayer.id = 'notes';

        this.map.addLayer(this.notesLayer);
      },

      addStopsLayer: function () {
        var self = this;
        this.stopsLayer = new OpenLayers.Layer.Vector('Trip stops', {
          projection: new OpenLayers.Projection('EPSG:4326'),
          styleMap: Styles.stopsStyleMap
        });
        this.stopsLayer.id = 'stops';

        this.map.addLayer(self.stopsLayer);
      },

      selectTripStop: function () {
        var stop_id = this.stop.get("stop_id");

        var newSelection = this.stopsLayer.getFeaturesByAttribute("stop_id", stop_id)[0];

        if (newSelection) {
          this.controls.selectStops.unselectAll();
          this.controls.selectStops.select(newSelection);
          // console.log(newSelection.geometry.getBounds().getCenterLonLat());
        };
      },

      onTripFeatureSelected: function (event) {
        this.handleStopSelect(event);
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

      attachEventHandlers: function () {
        var self = this;
        this.stopsLayer.events.register('featureselected', self,
          self.onTripFeatureSelected);
        this.stopsLayer.events.register('featureunselected', self,
          self.onTripFeatureSelected);

        this.layers.stopsBboxLayer.layer.events.register('featureselected', self,
          self.onBboxFeatureSelected);
        this.layers.stopsBboxLayer.layer.events.register('featureunselected', self,
          self.onBboxFeatureSelected);
        this.layers.shapesLayer.layer.events.register('featureadded', self, function (shape) {
          self.updateShapeModel();
          self.controls.drawShape.deactivate();
        })
      },

      addControls: function () {
        var self = this;
        var controls = {};

        this.controls = controls;

        controls.selectStops = new OpenLayers.Control.SelectFeature(
          [self.stopsLayer, self.layers.stopsBboxLayer.layer, self.layers.drawStops.layer, self.layers.kml.layer],
          {
            id: 'selectStops',
            clickout: true, toggle: false,
            multiple: false, hover: false
          });
        this.map.addControl(controls.selectStops);

        controls.selectMultiple = new OpenLayers.Control.SelectFeature(
          self.layers.stopsBboxLayer.layer,
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

        controls.modifyShape = new OpenLayers.Control.ModifyFeature(
          self.shapesLayer,
          {
            id: 'modifyShape',
            vertexRenderIntent: 'vertex'
          });
        this.map.addControl(controls.modifyShape);

        controls.drawShape = new OpenLayers.Control.DrawFeature(
          self.shapesLayer, OpenLayers.Handler.Path);
        this.map.addControl(controls.drawShape);

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
        this.controls.modifyShape.deactivate();
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
