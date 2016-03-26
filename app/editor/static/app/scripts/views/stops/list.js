'use strict';

define([
  'underscore',
  'backbone',
  'handlebars',
  'JST',
  'views/stopData',
  'views/filter',
  'views/stops/map',
  'views/stopToolbar',
  'models/stop'
  ], function (_, Backbone, Handlebars, JST, StopDataView, FilterView, StopMapView,
      StopToolbarView, StopModel) {
    var View;

    View = Backbone.View.extend({
      el: $('.main-view'),

      template: JST['stops/list'],

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
        this.stopMapView = stopMapView;

        var filterView = new FilterView({
          el: this.$('.filter-view')
        });
        filterView.on('change', function (value) {
          stopMapView.layers.stopsBboxLayer.layer.protocol.params.filter = value;
          stopMapView.layers.stopsBboxLayer.layer.refresh({force:true});
        });

        this.stopDataView = new StopDataView({
          model: this.model,
          el: this.$('.stop-data-view')
        });

        this.model.on('sync', function () {
          this.refreshStops();
        }, this);
      },

      refreshStops: function () {
        this.stopMapView.layers.stopsBboxLayer.layer.refresh({force:true});
      }

    });

    return View;
  });