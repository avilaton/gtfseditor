define([
  'jquery',
  "models/shape",
	"models/stop",
  "collections/routes",
  "collections/trips",
  "collections/stops",
  "collections/kml",
  "views/filter",
  "views/kmlSelect",
  "views/routesSelect",
  "views/tripsSelect",
  "views/shapesToolbox",
  "views/sequenceToolbox",
  "views/stopData",
  "views/stopToolbar",
  "views/map",
  'views/navbarRight',
  'views/sequence'
	], 
  function ($, ShapeModel, StopModel, RoutesCollection, TripsCollection, 
    StopsCollection, KmlCollection, FilterView, KmlSelectView, RoutesSelectView, 
    TripsSelectView, ShapesToolboxView, SequenceToolboxView, 
    StopDataView, StopToolbarView, MapView, NavbarRightView, SequenceView) {

    require(["bootstrap"]);

		function init () {
			var routesCollection,
      kmlCollection,
      tripsCollection,
      stopsCollection,
      shapeModel,
      stopModel;
			
      var navbarRight = new NavbarRightView();

      routesCollection = new RoutesCollection();
      kmlCollection = new KmlCollection();
      tripsCollection = new TripsCollection();
      stopsCollection = new StopsCollection();
      shapeModel = new ShapeModel();
      stopModel = new StopModel();

			routesCollection.fetch();


      var routeSelector = new RoutesSelectView({
        collection: routesCollection
      });
      var tripsSelector = new TripsSelectView({
        routesCollection: routesCollection,
        collection: tripsCollection
      });
      var sequenceView = new SequenceView({
        collection: stopsCollection
      });

      var kmlSelector = new KmlSelectView({
        el: $("#kmlSelect"),
        collection: kmlCollection
      })

      var myMap = new MapView({
        shape: shapeModel,
        stops: stopsCollection,
        stop: stopModel,
        kml: kmlCollection
      });
      // myMap.bboxLayer.refresh({force: true});

      var filterBox = new FilterView({
        bboxLayer: myMap.bboxLayer
      });

      var myShapesToolbox = new ShapesToolboxView({
        model: shapeModel,
        controls: myMap.controls,
        map: myMap
      });

      var mySequenceToolbox = new SequenceToolboxView({
        collection: stopsCollection,
        model: stopModel,
        controls: myMap.controls
      });

      var myStopDataView = new StopDataView({
        model: stopModel,
        controls: myMap.controls
      });

      var myStopToolbarView = new StopToolbarView({
        model: stopModel,
        controls: myMap.controls,
        stopDataView: myStopDataView
      });

      /** 
       * this should be inside map.js
       */
      tripsCollection.on("trip_selected", function (selectedModel) {
        var trip_id = selectedModel.get("trip_id");
        var shape_id = selectedModel.get("shape_id");

        shapeModel.set("shape_id", shape_id);
        shapeModel.fetch({reset: true}).done(function () {
          myMap.updateShapesLayer();
        });

        stopsCollection.trip_id = trip_id;
        stopsCollection.fetch({reset: true});
      });

		};

		return {
			init: init
		};
	});