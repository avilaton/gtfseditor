define([
  'underscore',
  'backbone',
  'handlebars',
  'JST',
  'views/map',
  'views/sequenceToolbox',
  'views/shapesToolbox',
  'views/sequence',
  'views/startTimes',
  'views/calendarsSelect',
  'views/calendarsTools',
  'views/kmlSelect',
  'views/tripToolbox',
  'models/route',
  'models/stop',
  'models/shape',
  'models/trip',
  'collections/stop_seq',
  'collections/tripStartTimes'
  ], function (_, Backbone, Handlebars, JST, MapView, SequenceToolboxView,
      ShapesToolboxView, SequenceView,
      StartTimesView, CalendarsSelectView, CalendarsToolsView, KmlSelectView,
      TripToolbox, RouteModel,
      StopModel, ShapeModel, TripModel, StopsSeqCollection, TripStartTimesCol) {
    var View;

    View = Backbone.View.extend({
      el: $('.main-view'),

      template: JST['routeTrip'],

      events: {},

      initialize: function(options){
        var self = this;

        this.tripModel = new TripModel({trip_id: options.trip_id})
        this.tripModel.fetch();
        this.routeModel = new RouteModel({route_id: options.route_id})
        this.routeModel.fetch();
        $.when(this.tripModel.fetch(), this.routeModel.fetch()).then(function(trip, route) {
          self.render();
        });
      },

      render: function () {
        this.$el.html(this.template({
          trip: this.tripModel.toJSON(),
          route: this.routeModel.toJSON()
        }));
        this.stopModel = new StopModel();
        this.stopsSeqCollection = new StopsSeqCollection();
        this.shapeModel = new ShapeModel();
        this.tripStartTimesCol = new TripStartTimesCol();

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

        var trip_id = this.tripModel.get('trip_id');
        var shape_id = this.tripModel.get('shape_id');
        this.shapeModel.trip_id = trip_id;

        this.shapeModel.set('trip_id', trip_id, {silent: true});
        if (shape_id) {
          this.shapeModel.fetch({reset: true}).done(function () {
            mapView.updateShapesLayer();
          });
        } else {
          this.shapeModel.unset('coordinates');
          mapView.updateShapesLayer();
        }
        shapesToolbox.render();

        this.stopsSeqCollection.trip_id = trip_id;
        this.stopsSeqCollection.fetch({reset: true});

        if (trip_id !== '') {
          this.tripStartTimesCol.trip_id = trip_id;
          this.tripStartTimesCol.fetch({reset: true});
        } else {
          this.tripStartTimesCol.reset();
        }

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

      }

    });

    return View;
  })