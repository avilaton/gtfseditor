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
  'models/stop',
  'models/shape',
  'collections/stops',
  'collections/stop_seq',
  'collections/tripStartTimes'
  ], function (_, Backbone, Handlebars, JST, MapView, RoutesSelectView,
      TripsSelectView, SequenceToolboxView, ShapesToolboxView, SequenceView,
      StartTimesView, StopModel, ShapeModel, StopsCollection, StopsSeqCollection,
      TripStartTimesCol) {
    var View;

    View = Backbone.View.extend({
      el: $('.main-view'),

      template: JST['times'],

      events: {},

      initialize: function(){
        this.render();
      },

      render: function () {
        this.$el.html(this.template());
        this.stopModel = new StopModel();
        this.stopsCollection = new StopsCollection();
        this.stopsSeqCollection = new StopsSeqCollection();
        this.tripStartTimesCol = new TripStartTimesCol();

        var routeSelector = new RoutesSelectView({
          el: '.routes-select'
        });

        var tripsSelector = new TripsSelectView({
          el: '.trips-select'
        });

        routeSelector.on('select', function (route_id) {
          tripsSelector.collection.route_id = route_id;
          tripsSelector.collection.fetch();
        });

        var startTimesView = new StartTimesView({
          el: '.start-times-view',
          collection: this.tripStartTimesCol
        });

        tripsSelector.on('select', function (value) {
          var selectedTrip = tripsSelector.collection.get(value);
          var trip_id = selectedTrip.get('trip_id');
      
          this.tripStartTimesCol.trip_id = trip_id;
          this.tripStartTimesCol.fetch({reset: true});

        }, this);
      }

    });

    return View;
  })