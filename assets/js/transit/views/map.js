define([
  "OpenLayers",
  "backbone",
  "transit/views/mapStyles"
  ],
  function (OpenLayers, Backbone, Styles) {
    'use strict';

    var MapView = Backbone.View.extend({
      // el: $("#mapBox"),

      initialize: function(options){
        var self = this;

        self.shape = options.shape;

        this.map = new OpenLayers.Map('map', {
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

        this.addGoogleMapsLayers();

        this.baselayer = new OpenLayers.Layer.OSM('OSM Map');

        this.map.addLayer(this.baselayer);

        this.format = new OpenLayers.Format.GeoJSON({
          'internalProjection': this.map.baseLayer.projection,
          'externalProjection': new OpenLayers.Projection("EPSG:4326")
        });

      },

      updateShapesLayer: function () {
        var self = this;
        var ft = this.format.read(self.shape.toJSON());
        this.shapesLayer.removeAllFeatures();
        this.shapesLayer.addFeatures(ft);
        self.shapesLayer.refresh();
      },

      addGoogleMapsLayers: function () {
        var gmap, gsat;

        if (typeof (google) === 'object') {
          gmap = new OpenLayers.Layer.Google('Google Streets', {
            numZoomLevels: 22,
            animationEnabled: false
          });
          this.map.addLayer(gmap);
          gsat = new OpenLayers.Layer.Google('Google Satellite', {
            type: google.maps.MapTypeId.SATELLITE,
            numZoomLevels: 22,
            animationEnabled: false
          });
          this.map.addLayer(gsat);
          gsat.mapObject.setTilt(0);
        };
      },

      addNotesLayer: function () {
        notesLayer = new OpenLayers.Layer.Vector('Notas', {
          styleMap: Styles.notesStyleMap
        });
        notesLayer.id = 'notes';

        map.addLayer(notesLayer);

        return maps;
      },

      addShapesLayer: function () {
        this.shapesLayer = new OpenLayers.Layer.Vector('Route shape', {
          styleMap: Styles.routesStyleMap
        });
        this.shapesLayer.id = 'shapes';

        this.map.addLayer(this.shapesLayer);
      },

      addGpxLayer: function () {
        gpxLayer = new OpenLayers.Layer.Vector('Gpx', {
          strategies: [new OpenLayers.Strategy.Fixed()],
          protocol: new OpenLayers.Protocol.HTTP({
            url: "",
            format: new OpenLayers.Format.GPX()
          }),
          styleMap: Styles.gpxStyleMap,
          projection: new OpenLayers.Projection("EPSG:4326")
        });
        gpxLayer.id = 'gpx';
        map.addLayer(gpxLayer);

        return maps;
      },

      addRoutesLayer: function () {
        routesLayer = new OpenLayers.Layer.Vector('Recorrido', {
          styleMap: Styles.routesStyleMap,
          projection: new OpenLayers.Projection('EPSG:4326'),
          strategies: [new OpenLayers.Strategy.Fixed()],
          protocol: new OpenLayers.Protocol.HTTP({
            format: new OpenLayers.Format.GeoJSON(),
            url: config.vectorLayerUrl
          })
        });

        routesLayer.id = 'routes';

        map.addLayer(routesLayer);

        return maps;
      },

      addStopsLayer: function () {
        var self = this;
        this.stopsLayer = new OpenLayers.Layer.Vector('Selected route stops', {
          styleMap: Styles.stopsStyleMap,
          projection: new OpenLayers.Projection('EPSG:4326'),
          strategies: [new OpenLayers.Strategy.Fixed()],
          protocol: new OpenLayers.Protocol.HTTP({
            format: new OpenLayers.Format.GeoJSON(),
            url: config.vectorLayerUrl
          })
        });
        this.stopsLayer.id = 'stops';
        
        this.map.addLayer(self.stopsLayer);
      },

      addBboxLayer: function () {
        var self = this;
        this.bboxLayer = new OpenLayers.Layer.Vector('Existing stops', {
          projection: new OpenLayers.Projection('EPSG:4326'),
          visibility: true,
          strategies: [new OpenLayers.Strategy.BBOX({resFactor: 2.0})],
          protocol: new OpenLayers.Protocol.HTTP({
            format: new OpenLayers.Format.GeoJSON(),
            url: 'api/bbox'
          })
        });
        this.bboxLayer.id = 'bbox';

        this.map.addLayer(self.bboxLayer);
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

      addLayer: function (spec) {
        var layer;

        layer = new OpenLayers.Layer.GML(spec.filename, "./data/" + spec.filename, {
          format: OpenLayers.Format.GeoJSON,
          styleMap: Styles["select"],
          visibility: false
        });
        layer.id = spec.filename;

        this.map.addLayer(layer);
      },

      setVisibility: function (layerId,visibility) {
        this.map.getLayer(layerId).setVisibility(visibility);
      },

      setSelectable: function (layerId) {
        var layer = this.map.getLayer(layerId),
        control = this.map.getControl("selectControl");

        control.setLayer(layer);
      },

      setCurrent: function (layerId) {
        var self = this;

        _.each(self.layers.models, function (model) {
          self.mapView.setVisibility(model.attributes.filename, false)
        });

        this.mapView.setVisibility(layerId, true);
      },

      toJSON: function (features) {
        var result = this.format.write(features);
        console.log("feature to json", result);
        $('#result').text(result);
        // this.trigger("featureselected");
      },

      selectedFeature: function (event) {
        App.vent.trigger("featureselected", event);
      }

    }); 

return MapView;
});
