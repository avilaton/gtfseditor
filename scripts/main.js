define([
  'jquery',
  "models/shape",
	"models/stop",
  "collections/stops",
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
  'views/sequence',
  'collections/stop_seq'
	], 
  function ($, ShapeModel, StopModel, 
    StopsCollection, FilterView, KmlSelectView, RoutesSelectView, 
    TripsSelectView, ShapesToolboxView, SequenceToolboxView, 
    StopDataView, StopToolbarView, MapView, NavbarRightView, SequenceView,
    StopsSeqCollection) {

    require(["bootstrap"]);

		function init () {
			var stopsCollection,
      shapeModel,
      stopModel;
			
      var navbarRight = new NavbarRightView();

      stopsCollection = new StopsCollection();
      stopsSeqCollection = new StopsSeqCollection();
      shapeModel = new ShapeModel();
      stopModel = new StopModel();

      var routeSelector = new RoutesSelectView();

      var tripsSelector = new TripsSelectView();

      routeSelector.on('select', function (route_id) {
        tripsSelector.collection.route_id = route_id;
        tripsSelector.collection.fetch();
      });

      var sequenceView = new SequenceView({
        collection: stopsSeqCollection
      });

      var kmlSelectView = new KmlSelectView({
        el: $("#kmlSelect")
      });
      kmlSelectView.on('select', function (value) {
        mapView.layers.kml.refresh(value);
      });

      var mapView = new MapView({
        el: '.map-view',
        shape: shapeModel,
        stops: stopsCollection,
        stop: stopModel
      });

      // var filterView = new FilterView();

      // filterView.on('change', function (value) {
      //   mapView.bboxLayer.protocol.params.filter = value;
      //   mapView.bboxLayer.refresh({force:true});
      // });

      var myShapesToolbox = new ShapesToolboxView({
        model: shapeModel,
        controls: mapView.controls,
        map: mapView
      });

      var mySequenceToolbox = new SequenceToolboxView({
        collection: stopsCollection,
        model: stopModel,
        controls: mapView.controls
      });

      var myStopDataView = new StopDataView({
        model: stopModel,
        controls: mapView.controls
      });

      var myStopToolbarView = new StopToolbarView({
        model: stopModel,
        controls: mapView.controls,
        stopDataView: myStopDataView
      });

      /** 
       * this should be inside map.js
       */
      tripsSelector.on('select', function (value) {
        var selectedTrip = tripsSelector.collection.get(value);
        var trip_id = selectedTrip.get('trip_id');
        var shape_id = selectedTrip.get('shape_id');

        shapeModel.set("shape_id", shape_id);
        shapeModel.fetch({reset: true}).done(function () {
          mapView.updateShapesLayer();
        });

        stopsCollection.trip_id = trip_id;
        stopsCollection.fetch({reset: true});

        stopsSeqCollection.trip_id = trip_id;
        stopsSeqCollection.fetch({reset: true}).done(function () {
          console.log(stopsSeqCollection);
        });
      });

		};

		return {
			init: init
		};
	});