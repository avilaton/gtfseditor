define([
  'underscore',
  'backbone',
  'handlebars',
  'JST',
  'views/stopData',
  'views/filter',
  'views/stopMap',
  'views/stopToolbar',
  'models/stop'
  ], function (_, Backbone, Handlebars, JST, StopDataView, FilterView, StopMapView,
      StopToolbarView, StopModel) {
    var View;

    View = Backbone.View.extend({
      el: $('.main-view'),

      template: JST['stops'],

      events: {},

      initialize: function(){
        this.model = new StopModel();
        this.render();
      },

      render: function () {
        this.$el.html(this.template());

        var stopMapView = new StopMapView({
          el: '.map-view',
          model: this.model
        });
        var filterView = new FilterView({
          el: this.$('.filter-view')
        });
        filterView.on('change', function (value) {
          stopMapView.bboxLayer.protocol.params.filter = value;
          stopMapView.bboxLayer.refresh({force:true});
        });

        var stopDataView = new StopDataView({
          model: this.model,
          el: this.$('.stop-data-view')
        });
        var stopToolbarView = new StopToolbarView({
          el: '.stop-toolbar-view',
          model: this.model,
          controls: stopMapView.controls
        });
      }

    });

    return View;
  })