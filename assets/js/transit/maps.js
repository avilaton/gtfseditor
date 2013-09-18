define(["OpenLayers",
  "jquery",
  "transit/model",
  "transit/styles",
  "transit/utils",
  "transit/config",
  "transit/models/state"
  ], function (OpenLayers, $, model, styles, utils, config, StateModel) {

    'use strict';

    var maps = {},
    map = {},
    vectorFormat = {},
    layerAdder = {},
    routesLayer,
    shapesLayer,
    stopsLayer,
    bboxLayer,
    notesLayer,
    gpxLayer,
    controls = {};

    maps.init = function (spec) {
      var layers = spec.layers, l,
      baselayer, gmap, gsat, osmLayer;

      map = new OpenLayers.Map(config.ui.mapDiv, {
        controls: [
        new OpenLayers.Control.LayerSwitcher(),
        new OpenLayers.Control.Navigation(),
        new OpenLayers.Control.PanZoomBar()
        ]
      });

      maps.map = map;

      if (config.localOsm) {
        baselayer = new OpenLayers.Layer.OSM('Mosaico Local',
          'http://localhost:8005/${z}/${x}/${y}.png',
          {numZoomLevels: 22, alpha: true, isBaseLayer: true});
        map.addLayer(baselayer);
        osmLayer = new OpenLayers.Layer.OSM('OSM Map');
        map.addLayer(osmLayer);
      } else {
        baselayer = new OpenLayers.Layer.OSM('OSM Map');
        map.addLayer(baselayer);
      }

      if (typeof (google) === 'object') {
        gmap = new OpenLayers.Layer.Google('Google Streets', {
          numZoomLevels: 22,
          animationEnabled: false
        });
        map.addLayer(gmap);
        gsat = new OpenLayers.Layer.Google('Google Satellite', {
          type: google.maps.MapTypeId.SATELLITE,
          numZoomLevels: 22,
          animationEnabled: false
        });
        map.addLayer(gsat);
        gsat.mapObject.setTilt(0);
      };

      vectorFormat = new OpenLayers.Format.GeoJSON({
        'internalProjection': map.baseLayer.projection,
        'externalProjection': new OpenLayers.Projection("EPSG:4326")
      });


    // Add Layers
    l = layers.length;
    for (var i = 0; i < l; i++) {
      layerAdder[layers[i]]();
    }

    // Initialize Map Controls
    initControls();

    return maps;
  };


  maps.setCenter = function (spec) {
    map.setCenter(
      new OpenLayers.LonLat(spec.lon, spec.lat)
      .transform(
        new OpenLayers.Projection('EPSG:4326'),
        map.getProjectionObject()
        ),
      spec.zoom
      );
  };

  layerAdder.notes = function () {
    notesLayer = new OpenLayers.Layer.Vector('Notas', {
      styleMap: styles.notesStyleMap
    });
    notesLayer.id = 'notes';

    map.addLayer(notesLayer);

    return maps;
  };

  layerAdder.shapes = function () {
    shapesLayer = new OpenLayers.Layer.Vector('Shapes', {
      styleMap: styles.routesStyleMap
    });
    notesLayer.id = 'shapes';

    map.addLayer(shapesLayer);

    return maps;
  };

  layerAdder.gpx = function () {
    gpxLayer = new OpenLayers.Layer.Vector('Gpx', {
      strategies: [new OpenLayers.Strategy.Fixed()],
      protocol: new OpenLayers.Protocol.HTTP({
        url: "",
        format: new OpenLayers.Format.GPX()
      }),
      styleMap: styles.gpxStyleMap,
      projection: new OpenLayers.Projection("EPSG:4326")
    });
    gpxLayer.id = 'gpx';
    map.addLayer(gpxLayer);

    return maps;
  };

  layerAdder.routes = function () {
    routesLayer = new OpenLayers.Layer.Vector('Recorrido', {
      styleMap: styles.routesStyleMap,
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
  };

  layerAdder.stops = function () {
    stopsLayer = new OpenLayers.Layer.Vector('Paradas', {
      styleMap: styles.stopsStyleMap,
      projection: new OpenLayers.Projection('EPSG:4326'),
      strategies: [new OpenLayers.Strategy.Fixed()],
      protocol: new OpenLayers.Protocol.HTTP({
        format: new OpenLayers.Format.GeoJSON(),
        url: config.vectorLayerUrl
      })
    });
    stopsLayer.id = 'stops';
    
    map.addLayer(stopsLayer);
    return maps;
  };

  layerAdder.bbox = function () {
    bboxLayer = new OpenLayers.Layer.Vector('Bbox Existing', {
      projection: new OpenLayers.Projection('EPSG:4326'),
      visibility: true,
      strategies: [new OpenLayers.Strategy.BBOX({resFactor: 2.0})],
      protocol: new OpenLayers.Protocol.HTTP({
        format: new OpenLayers.Format.GeoJSON(),
        url: config.vectorLayerUrl+'bbox'
      })
    });
    bboxLayer.id = 'bbox';

    map.addLayer(bboxLayer);


    return maps;
  };

  function initControls() {
    var firstGeolocation;

    controls.selectStops = new OpenLayers.Control.SelectFeature(
      [stopsLayer,bboxLayer],
      {
        id: 'selectStops',
        clickout: true, toggle: false,
        multiple: false, hover: false
      });
    map.addControl(controls.selectStops);

    controls.selectMultiple = new OpenLayers.Control.SelectFeature(
      bboxLayer,
      {
        id: 'selectMultiple',
        multiple: true, multipleKey: 'shiftKey', 
        box: true,
        clickout: true, toggle: true,
        hover: false
      });
    map.addControl(controls.selectMultiple);

    controls.modifyStops = new OpenLayers.Control.ModifyFeature(
      stopsLayer,{id: 'modifyStops'});
    map.addControl(controls.modifyStops);

    controls.modifyBbox = new OpenLayers.Control.ModifyFeature(
      bboxLayer,{id: 'modifyBbox'});
    map.addControl(controls.modifyBbox);

    controls.modifyShape = new OpenLayers.Control.ModifyFeature(
      routesLayer,{
        id: 'modifyShape',
        vertexRenderIntent: 'vertex'
      });
    map.addControl(controls.modifyShape);
    
    controls.drawStops = new OpenLayers.Control.DrawFeature(stopsLayer,
      OpenLayers.Handler.Point);
    map.addControl(controls.drawStops);
    
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
return maps;
};

function selectFeatures (context) {
  var selectedFeatures = context.object.selectedFeatures;
  var formatedFeatures = vectorFormat.write(selectedFeatures);
  model.select(formatedFeatures);
};

maps.setEventHandlers = function (handlers) {
  stopsLayer.events.register('featureselected', stopsLayer,
    handlers.renderStopInfo);
  stopsLayer.events.register('featureunselected',stopsLayer,
    handlers.renderStopInfo);
  bboxLayer.events.register('featureselected',bboxLayer,
    handlers.renderStopInfo);
  bboxLayer.events.register('featureunselected',bboxLayer,
    handlers.renderStopInfo);
  bboxLayer.events.on({
    'featureselected': selectFeatures,
    'featureunselected': selectFeatures,
    scope: bboxLayer
  });
  routesLayer.events.register('loadend',
  {
    'routesLayer':routesLayer,
    'notesLayer':notesLayer
  },
  utils.endsRenderer);
};

maps.bboxGetSelected = function () {
  return bboxLayer.selectedFeatures
};

maps.update = function () {
  console.log(app.state.shape);
  var ft = vectorFormat.read(app.state.shape.toJSON());
  shapesLayer.removeAllFeatures();
  shapesLayer.addFeatures(ft);
  shapesLayer.refresh();
  routesLayer.refresh({url: routesLayer.protocol.url+'shape/'+model.selected.shape_id})
  controls.selectStops.deactivate();
  stopsLayer.refresh({url: stopsLayer.protocol.url+'trip/'+model.selected.trip_id+'/stops'});
  controls.selectStops.activate();
  notesLayer.refresh();
    //gpxLayer.refresh({url:'gpx/'+spec.track});
  };

  maps.readShape = function () {
    var shape = vectorFormat.write(routesLayer.features, true);
    return {shape: shape};
  };
  
  maps.readStops = function () {
    var trip_id = stopsLayer.protocol.params.trip_id;
    var stops = vectorFormat.write(stopsLayer.features, true);
    return {trip_id: trip_id,
      stops: stops};
    };

    maps.readBbox = function () {
      var stops = vectorFormat.write(bboxLayer.features);
      console.log(stops);
      return {stops: stops};
    };

    maps.destroySelected = function () {
      stopsLayer.selectedFeatures[0].destroy();
      return;
    };

    maps.getSelectedStop = function () {
      return stopsLayer.selectedFeatures[0];
    };

    maps.appendSelected = function () {
      stopsLayer.addFeatures(bboxLayer.selectedFeatures);
      return;
    };

    maps.reverseShape = function () {
      var shape = routesLayer.features[0];
      shape.geometry.components.reverse();
    };

    maps.skipHandler = function (i) {
      function skipper() {
        var selectedFeature = stopsLayer.selectedFeatures[0];
        var ordinal = selectedFeature.data.stop_seq;    
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
      };

      return skipper;
    };

    maps.showUserLocation = function (position) {

    };

    maps.center = function () {
      transit.maps.utils.logmap(map);
    }
    return maps;

  });