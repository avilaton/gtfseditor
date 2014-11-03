define([
  'underscore',
  'backbone',
  'handlebars',
  'text!templates/stops.handlebars',
  'views/stopData',
  'views/filter',
  'views/map',
  'models/stop',
  'models/shape',
  'collections/stops'
  ], function (_, Backbone, Handlebars, tmpl, StopDataView, FilterView, MapView,
      StopModel, ShapeModel, StopsCollection) {
    var View;

    View = Backbone.View.extend({
      el: $('.main-view'),

      template: Handlebars.compile(tmpl),

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
        var filterView = new FilterView({
          el: this.$('.filter-view')
        });
        var mapView = new MapView({
          el: '.map-view',
          shape: this.shapeModel,
          stops: this.stopsCollection,
          stop: this.stopModel
        });
      }

    });

    return View;
  })