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
  'models/stop',
  'models/shape',
  'collections/stop_seq'
  ], function (_, Backbone, Handlebars, JST, MapView, RoutesSelectView,
      TripsSelectView, SequenceToolboxView, ShapesToolboxView, SequenceView,
      StopModel, ShapeModel, StopsSeqCollection) {
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

        var mapView = new MapView({
          el: '.map-view',
          shape: this.shapeModel,
          collection: this.stopsSeqCollection,
          stop: this.stopModel
        });

        // var kmlSelectView = new KmlSelectView({
        //   el: $("#kmlSelect")
        // });
        // kmlSelectView.on('select', function (value) {
        //   mapView.layers.kml.refresh(value);
        // });

        var shapesToolbox = new ShapesToolboxView({
          el: '.shapes-toolbox',
          model: this.shapeModel,
          controls: mapView.controls,
          map: mapView
        });

        var sequenceToolbox = new SequenceToolboxView({
          el: '.sequence-toolbox',
          collection: this.stopsSeqCollection,
          model: this.stopModel,
          controls: mapView.controls
        });

        var sequenceView = new SequenceView({
          el: '.sequence-view',
          collection: this.stopsSeqCollection
        });

        tripsSelector.on('select', function (value) {
          var selectedTrip = tripsSelector.collection.get(value);
          var trip_id = selectedTrip.get('trip_id');
          var shape_id = selectedTrip.get('shape_id');

          this.shapeModel.set("shape_id", shape_id);
          this.shapeModel.fetch({reset: true}).done(function () {
            mapView.updateShapesLayer();
          });

          this.stopsSeqCollection.trip_id = trip_id;
          this.stopsSeqCollection.fetch({reset: true});
        }, this);
      }

    });

    return View;
  })