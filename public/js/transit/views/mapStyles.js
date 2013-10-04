define([
  "OpenLayers"
  ], function (OpenLayers) {
   var Styles = {};

   Styles.notesStyleMap = new OpenLayers.StyleMap({
    'default': new OpenLayers.Style({strokeColor: 'blue',
      strokeWidth: 10, strokeOpacity: 1, pointRadius: 6,
      fillOpacity: 1,
      fontColor: "black", fontSize: "16px",
      fontFamily: "Courier New, monospace", fontWeight: "bold",
      labelAlign: "left", labelXOffset: "8", labelYOffset: "8",
      labelOutlineColor: "white", labelOutlineWidth: 3
    }),
    'select': new OpenLayers.Style({strokeColor: "red",
      strokeWidth: 3, pointRadius: 5
    })
  });
   Styles.notesStyleMap.addUniqueValueRules("default", "type", {
    "Start": {label : "${type}", fillColor: 'white',
    strokeWidth: 3, strokeColor: 'black'},
    "End": {label : "${type}", fillColor: 'white',
    strokeWidth: 3, strokeColor: 'black'},
    "Line": {strokeWidth: 10, strokeOpacity: 0.5}
  });

   Styles.gpxStyleMap = new OpenLayers.StyleMap({
    'default': new OpenLayers.Style({
      strokeColor: 'black',
      strokeWidth: 2, strokeOpacity: 1, pointRadius: 6,
      fillOpacity: 0.8,
      fontColor: "black", fontSize: "16px",
      fontFamily: "Courier New, monospace", fontWeight: "bold",
      labelAlign: "left", labelXOffset: "8", labelYOffset: "8",
      labelOutlineColor: "white", labelOutlineWidth: 3
    })
  });


   Styles.gpxStyleMap.addUniqueValueRules("default", "name", 
   {
     "Bus stop": {label : "s", fillColor: 'white',
     strokeWidth: 3, strokeColor: 'black'},
     "Parada de autobús": {label : "s", fillColor: 'white',
     strokeWidth: 3, strokeColor: 'black'},
     "Tracked with OSMTracker for Android™": {fillColor: 'white',
     strokeWidth: 3, strokeColor: 'green'},
     "Trazado con OSMTracker para Android™": {fillColor: 'white',
     strokeWidth: 3, strokeColor: 'green'}
   });


   Styles.routesStyleMap = new OpenLayers.StyleMap({
    'default': new OpenLayers.Style({
      strokeColor: "blue",
      strokeWidth: 8,
      strokeOpacity: 0.6
    }),
    'select': new OpenLayers.Style({
      strokeColor: "red",
      strokeWidth: 8,
      strokeOpacity: 0.8
    }),
    'vertex': new OpenLayers.Style({
      strokeColor: "black",
      strokeWidth: 2,
      strokeOpacity: 0.9,
      pointRadius: 8,
      fill: true,
      fillColor: 'white',
      fillOpacity: 0.6
    })
  });

   Styles.stopsStyleMap = new OpenLayers.StyleMap({
    'default': new OpenLayers.Style({
      strokeColor: 'black', strokeWidth: 2, strokeOpacity: 1, 
      pointRadius: 6, fillColor: 'white', fill: true, 
      fillOpacity: 1
    })
    ,
    'select': new OpenLayers.Style({
      strokeColor: 'black', strokeWidth: 2, strokeOpacity: 1, 
      pointRadius: 8, fillColor: 'red', fill: true, fillOpacity: .6,
      label: '${stop_id}',
      fontColor: "black", fontSize: "16px", 
      fontFamily: "Courier New, monospace", fontWeight: "bold",
      labelAlign: "left", labelXOffset: "8", labelYOffset: "12",
      labelOutlineColor: "white", labelOutlineWidth: 3
    })          
  });

   Styles.bboxStyleMap = new OpenLayers.StyleMap({
    'default': new OpenLayers.Style({
      strokeColor: 'black', strokeWidth: 1, strokeOpacity: 1, 
      stroke: true,
      pointRadius: 4, fillColor: 'yellow', fill: true, 
      fillOpacity: 1
    })
    ,
    'select': new OpenLayers.Style({
      strokeColor: 'black', strokeWidth: 2, strokeOpacity: 1, 
      pointRadius: 8, fillColor: 'red', fill: true, fillOpacity: .6,
      label: '${stop_id}',
      fontColor: "black", fontSize: "16px", 
      fontFamily: "Courier New, monospace", fontWeight: "bold",
      labelAlign: "left", labelXOffset: "8", labelYOffset: "12",
      labelOutlineColor: "white", labelOutlineWidth: 3
    })          
  });

   return Styles;

 });