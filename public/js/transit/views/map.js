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
        self.stops = options.stops;
        self.stop = options.stop;

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

        self.stops.on("trip_stop_selected", self.selectTripStop, self);
      },

      updateShapesLayer: function () {
        var self = this;
        var ft = this.format.read(self.shape.toJSON());
        this.shapesLayer.removeAllFeatures();
        this.shapesLayer.addFeatures(ft);
        self.shapesLayer.refresh();
      },

      updateStopsLayer: function () {
        var self = this;
        var ft = this.format.read(self.stops.geoJSON);
        this.stopsLayer.removeAllFeatures();
        this.stopsLayer.addFeatures(ft);
        this.stopsLayer.refresh();
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
          projection: new OpenLayers.Projection('EPSG:4326'),
          styleMap: Styles.stopsStyleMap
        });
        this.stopsLayer.id = 'stops';
        
        this.map.addLayer(self.stopsLayer);
      },

      addBboxLayer: function () {
        var self = this;

        var refreshStrategy = new OpenLayers.Strategy.Refresh({
          // interval: 1000, 
          force: true
        });

        this.bboxLayer = new OpenLayers.Layer.Vector('Existing stops', {
          projection: new OpenLayers.Projection('EPSG:4326'),
          visibility: true,
          strategies: [
            new OpenLayers.Strategy.BBOX({resFactor: 2.0}),
            refreshStrategy
            ],
          protocol: new OpenLayers.Protocol.HTTP({
            format: new OpenLayers.Format.GeoJSON(),
            url: 'api/bbox',
            params: {filter:''}
          })
        });
        this.bboxLayer.id = 'bbox';

        refreshStrategy.activate();

        this.map.addLayer(self.bboxLayer);
      },

      selectTripStop: function (selectedModel) {
        var stop_id = selectedModel.get("id");

        var newSelection = this.stopsLayer.getFeaturesByAttribute("stop_id", stop_id)[0];

        if (newSelection) {
          this.controls.selectStops.unselectAll();
          this.controls.selectStops.select(newSelection);
          // console.log(newSelection.geometry.getBounds().getCenterLonLat());
        };
      },

      onTripFeatureSelected: function (event) {
        var feature = event.feature;

        // this.format.extract.feature(feature) fails, check issue at openlayers
        var geoJSON = this.format.write(feature);
        this.stop.set(JSON.parse(geoJSON));

        this.stops.select(feature.fid);

        if (event.type == "featureselected") {
          this.stop.set(JSON.parse(geoJSON));
        } else if (event.type == "featureunselected") {
          this.stop.clear();
        };
      },

      onBboxFeatureSelected: function (event) {
        var feature = event.feature;

        var geoJSON = this.format.write(feature);
        if (event.type == "featureselected") {
          this.stop.set(JSON.parse(geoJSON));
        } else if (event.type == "featureunselected") {
          this.stop.clear();
        };
      },

      onMultipleFeatureSelected: function (event) {
        console.log(event);
      },

      attachEventHandlers: function () {
        var self = this;
        this.stopsLayer.events.register('featureselected', self,
          self.onTripFeatureSelected);
        // this.stopsLayer.events.register('featureunselected', self,
        //   self.onTripFeatureSelected);

        this.bboxLayer.events.register('featureselected', self,
          self.onBboxFeatureSelected);
        this.bboxLayer.events.register('featureunselected', self,
          self.onBboxFeatureSelected);

        // this.bboxLayer.events.on({
        //   'featureselected': self.onMultipleFeatureSelected,
        //   'featureunselected': self.onMultipleFeatureSelected,
        //   scope: self.bboxLayer
        // });

        // this.shapesLayer.events.register('loadend',
        // {
        //   'routesLayer':self.routesLayer,
        //   'notesLayer':self.notesLayer
        // },
        // utils.endsRenderer);
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

      addOldControls: function () {
        var self = this;
        var controls = {};

        this.controls = controls;

        controls.selectStops = new OpenLayers.Control.SelectFeature(
          [self.stopsLayer,self.bboxLayer],
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
          self.stopsLayer,{id: 'modifyStops'});
        self.map.addControl(controls.modifyStops);

        controls.modifyBbox = new OpenLayers.Control.ModifyFeature(
          self.bboxLayer,{id: 'modifyBbox'});
        self.map.addControl(controls.modifyBbox);

        controls.modifyShape = new OpenLayers.Control.ModifyFeature(
          self.shapesLayer,{
            id: 'modifyShape',
            vertexRenderIntent: 'vertex'
          });
        this.map.addControl(controls.modifyShape);
        
        controls.drawStops = new OpenLayers.Control.DrawFeature(self.stopsLayer,
          OpenLayers.Handler.Point);
        this.map.addControl(controls.drawStops);
        
        controls.selectStops.activate();
      },

      addGeolocationControl: function () {
        var firstGeolocation;

        controls.geolocate = new OpenLayers.Control.Geolocate({
          bind: false,
          geolocationOptions: {
            enableHighAccuracy: false,
            maximumAge: 0,
            timeout: 7000
          }
        });
        map.addControl(controls.geolocate);
        
        controls.geolocate.events.register("locationupdated",controls.geolocate,function(e) {
          console.log('location updated');
          var cross = notesLayer.getFeatureById('userCross');
          var circle = notesLayer.getFeatureById('userAccuracy');
          if (cross) {
            notesLayer.removeFeatures(cross);
          }
          if (circle) {
            notesLayer.removeFeatures(circle);
          }
          
          circle = new OpenLayers.Feature.Vector(
            OpenLayers.Geometry.Polygon.createRegularPolygon(
              new OpenLayers.Geometry.Point(e.point.x, e.point.y),
              e.position.coords.accuracy/2,
              40,
              0
              ),
            {},
            {
              fillColor: '#000',
              fillOpacity: 0.1,
              strokeWidth: 0
            }
            );
          circle.id = 'userAccuracy';
          
          cross = new OpenLayers.Feature.Vector(
            e.point,
            {},
            {
              graphicName: 'cross',
              strokeColor: '#f00',
              strokeWidth: 2,
              fillOpacity: 0,
              pointRadius: 10
            }
            );
          cross.id = 'userCross';
          
          notesLayer.addFeatures([cross,circle]);
          
          if (firstGeolocation) {
            firstGeolocation = false;
            // the following will center the map to the user's location
            //~ this.bind = true; 
          }
        });

        controls.geolocate.events.register("locationfailed", this, function() {
          console.log('Location detection failed');
        });
        controls.geolocate.watch = true;
        firstGeolocation = true;
        controls.geolocate.activate();

        controls.selectStops.activate();

        maps.controls = controls;
      },

      skip: function () {
        var selectedFeature = this.stopsLayer.selectedFeatures[0];
        var ordinal = selectedFeature.data.stop_seq;
        console.log(selectedFeatures);
        var nextSelected = stopsLayer.getFeaturesByAttribute('stop_seq',ordinal+i)[0];

        var current;
        if (controls.selectStops.active) {
          current = controls.selectStops;
        } else if (controls.modifyStops.active) {
          current = controls.modifyStops.selectControl;
        };
        if (nextSelected) {
          current.unselectAll();
          current.select(nextSelected);
          map.setCenter(
            new OpenLayers.LonLat(nextSelected.geometry.x,
              nextSelected.geometry.y));
        };
        return false;
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
