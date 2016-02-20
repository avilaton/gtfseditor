'use strict';

define([
  'underscore',
  'backbone',
  'JST',
  'models/route',
  'collections/trips',
  'views/modals/trip'
  ], function (_, Backbone, JST, RouteModel, TripsCollection, TripModal) {
    var View;

    View = Backbone.View.extend({
      tagName: 'div',

      events: {
        'click button.btn-create': 'onCreate',
        'click button.btn-edit': 'onEdit',
        'click button.btn-rm': 'onRemove'
      },

      template: JST.tripsList,

      initialize: function(options){
        var self = this;
        this.routeModel = new RouteModel({route_id: options.route_id});

        this.collection = new TripsCollection();
        this.collection.route_id = options.route_id;
        this.collection.on('add change remove reset', this.render, this);
        $.when(this.collection.fetch(), this.routeModel.fetch()).then(function(trips, route) {
          self.render();
        });
      },

      render: function () {
        this.$el.html(this.template({
          models: this.collection.toJSON(),
          route: this.routeModel.toJSON()
        }));
        $('.main-view').empty().append(this.el);
        this.delegateEvents(this.events);
      },

      onRemove: function (e) {
        var $target = $(e.currentTarget),
          index = $target.closest('tr').data('index'),
          model = this.collection.at(index);

        e.preventDefault();
        model.destroy();
      },

      onCreate: function (e) {
        e.preventDefault();
        var model = this.collection.create();
        var modal = new TripModal({
          model: model,
          el: $('#routeDataEditor')
        });
        modal.$el.modal('show');
      },

      onEdit: function (e) {
        var $target = $(e.currentTarget),
          index = $target.closest('tr').data('index'),
          model = this.collection.at(index),
          modal = new TripModal({
            model: model,
            el: $('#routeDataEditor')
        });
        modal.$el.modal('show');
      }
    });

    return View;
  });