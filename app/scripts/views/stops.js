define([
  'underscore',
  'backbone',
  'handlebars',
  'JST',
  'views/stopData',
  'views/filter',
  'views/map',
  'views/stopToolbar',
  'models/stop',
  'models/shape',
  'collections/stops'
  ], function (_, Backbone, Handlebars, JST, StopDataView, FilterView, MapView,
      StopToolbarView, StopModel, ShapeModel, StopsCollection) {
    var View;

    View = Backbone.View.extend({
      el: $('.main-view'),

      template: JST['stops'],

      events: {},

      initialize: function(){
        this.render();
      },

      render: function () {
        this.$el.html(this.template());
        this.stopModel = new StopModel();
        this.stopsCollection = new StopsCollection();
        this.shapeModel = new ShapeModel();

        var stopDataView = new StopDataView({
          model: this.stopModel,
          el: this.$('.stop-data-view')
        });
        var mapView = new MapView({
          el: '.map-view',
          shape: this.shapeModel,
          stops: this.stopsCollection,
          stop: this.stopModel
        });
        var filterView = new FilterView({
          el: this.$('.filter-view')
        });
        filterView.on('change', function (value) {
          mapView.bboxLayer.protocol.params.filter = value;
          mapView.bboxLayer.refresh({force:true});
        });
        var stopToolbarView = new StopToolbarView({
          el: '.stop-toolbar-view',
          model: this.stopModel,
          controls: mapView.controls,
          stopDataView: stopDataView
        });
      }

    });

    return View;
  })