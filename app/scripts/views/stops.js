define([
  'underscore',
  'backbone',
  'handlebars',
  'JST',
  'views/stopData',
  'views/filter',
  'views/stopMap',
  'views/stopToolbar',
  'models/stop',
  'models/shape',
  'collections/stops'
  ], function (_, Backbone, Handlebars, JST, StopDataView, FilterView, StopMapView,
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

        var stopMapView = new StopMapView({
          el: '.map-view',
          stop: this.stopModel,
          model: this.stopModel
        });
        var filterView = new FilterView({
          el: this.$('.filter-view')
        });
        filterView.on('change', function (value) {
          stopMapView.bboxLayer.protocol.params.filter = value;
          stopMapView.bboxLayer.refresh({force:true});
        });

        var stopDataView = new StopDataView({
          model: this.stopModel,
          el: this.$('.stop-data-view')
        });
        var stopToolbarView = new StopToolbarView({
          el: '.stop-toolbar-view',
          model: this.stopModel,
          controls: stopMapView.controls,
          stopDataView: stopDataView
        });
      }

    });

    return View;
  })