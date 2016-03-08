define([
  'underscore',
  'backbone',
  'handlebars',
  'JST',
  'views/map',
  'views/routesSelect',
  'views/tripsSelect',
  'views/sequenceToolbox',
  'views/shapesToolbox',
  'views/sequence',
  'views/startTimes',
  'views/calendarsSelect',
  'views/calendarsTools',
  'views/kmlSelect',
  'views/tripToolbox',
  'models/stop',
  'models/shape',
  'collections/stop_seq',
  'collections/tripStartTimes'
  ], function (_, Backbone, Handlebars, JST, MapView, RoutesSelectView,
      TripsSelectView, SequenceToolboxView, ShapesToolboxView, SequenceView,
      StartTimesView, CalendarsSelectView, CalendarsToolsView, KmlSelectView,
      TripToolbox,
      StopModel, ShapeModel, StopsSeqCollection, TripStartTimesCol) {
    var View;

    View = Backbone.View.extend({
      el: $('.main-view'),

      template: JST['routes'],

      events: {},

      initialize: function(){
        this.render();
      },

      render: function () {
        this.$el.html(this.template());
        this.stopModel = new StopModel();
        this.stopsSeqCollection = new StopsSeqCollection();
        this.shapeModel = new ShapeModel();
        this.tripStartTimesCol = new TripStartTimesCol();

        var routeSelector = new RoutesSelectView({
          el: this.$('.routes-select')
        });

        var tripsSelector = new TripsSelectView({
          el: this.$('.trips-select')
        });

        routeSelector.on('select', function (route_id) {
          tripsSelector.collection.route_id = route_id;
          tripsSelector.collection.fetch();
        });

        var mapView = new MapView({
          el: this.$('.map-view'),
          shape: this.shapeModel,
          collection: this.stopsSeqCollection,
          stop: this.stopModel,
          model: this.stopModel
        });

        var kmlSelectView = new KmlSelectView({
          el: this.$('.kml-select-view')
        });
        kmlSelectView.on('select', function (content) {
          mapView.layers.fileLayer.read(content);
        });

        var shapesToolbox = new ShapesToolboxView({
          el: this.$('.shapes-toolbox'),
          model: this.shapeModel,
          controls: mapView.controls,
          map: mapView
        });

        var tripToolbox = new TripToolbox({
          el: this.$('.trip-toolbox'),
          collection: this.stopsSeqCollection,
          model: this.stopModel
        });

        var sequenceToolbox = new SequenceToolboxView({
          el: this.$('.sequence-toolbox'),
          collection: this.stopsSeqCollection,
          model: this.stopModel
        });

        var sequenceView = new SequenceView({
          el: this.$('.sequence-view'),
          collection: this.stopsSeqCollection
        });

        tripsSelector.on('select', function (value) {
          var selectedTrip = tripsSelector.collection.get(value);
          var trip_id = selectedTrip.get('trip_id');
          var shape_id = selectedTrip.get('shape_id');

          this.shapeModel.clear();
          this.shapeModel.set('trip_id', trip_id, {silent: true});
          if (shape_id) {
            this.shapeModel.fetch({reset: true}).done(function () {
              mapView.updateShapesLayer();
            });
          } else {
            this.shapeModel.unset('coordinates');
            mapView.updateShapesLayer();
          }

          this.stopsSeqCollection.trip_id = trip_id;
          this.stopsSeqCollection.fetch({reset: true});
        }, this);

        this.shapeModel.on('created', function () {
          tripsSelector.collection.fetch();
        });

        var calendarsSelectView = new CalendarsSelectView({
          el: this.$('.calendars-select-view')
        });

        var calendarsToolsView = new CalendarsToolsView({
          el: this.$('.calendars-tools-view'),
          collection: this.tripStartTimesCol
        });

        calendarsSelectView.on('select', function (service_id) {
          this.tripStartTimesCol.service_id = service_id;
          if (service_id !== '') {
            this.tripStartTimesCol.fetch({reset: true});
          } else {
            this.tripStartTimesCol.reset();
          }
        }, this);

        var startTimesView = new StartTimesView({
          el: this.$('.start-times-view'),
          collection: this.tripStartTimesCol
        });

        tripsSelector.on('select', function (value) {
          var selectedTrip = tripsSelector.collection.get(value);
          var trip_id = selectedTrip.get('trip_id');

          if (trip_id !== '') {
            this.tripStartTimesCol.trip_id = trip_id;
            this.tripStartTimesCol.fetch({reset: true});
          } else {
            this.tripStartTimesCol.reset();
          }
        }, this);
      }

    });

    return View;
  })