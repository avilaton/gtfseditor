'use strict';

define([
  'underscore',
  'backbone',
  'JST',
  'models/route',
  'collections/routes',
  'collections/agencies',
  'views/modals/route'
  ], function (_, Backbone, JST, RouteModel, RoutesCollection, AgenciesCollection, RouteModal) {
    var View;

    View = Backbone.View.extend({
      tagName: 'div',

      events: {
        'click button.btn-create': 'onCreate',
        'click button.btn-edit': 'onEdit',
        'click button.btn-rm': 'onRemove'
      },

      template: JST.routesList,

      initialize: function(){
        var self = this;
        this.collection = new RoutesCollection();
        this.agencies = new AgenciesCollection();

        var agenciesPromise = this.agencies.fetch().then(function (agencies) {
          self.agencies = agencies;
        });
        var routesPromise = this.collection.fetch({reset: true});
        $.when(agenciesPromise, routesPromise).then(function() {
          self.render()
        })
        this.collection.on('add change remove', this.render, this);
      },

      render: function () {
        var self = this;
        var models = this.collection.toJSON();
        models = _.map(models, function (model) {
          model.agency = _.find(self.agencies, function(agency) {
            return agency.agency_id == model.agency_id;
          });
          return model;
        });

        this.$el.html(this.template({models: models}));
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
        var model = new RouteModel();
        var modal = new RouteModal({
          model: model,
          collection: this.collection,
          el: $('#routeDataEditor')
        });
        modal.$el.modal('show');
      },

      onEdit: function (e) {
        var $target = $(e.currentTarget),
          index = $target.closest('tr').data('index'),
          model = this.collection.at(index),
          modal = new RouteModal({
            model: model,
            collection: this.collection,
            el: $('#routeDataEditor')
        });
        modal.$el.modal('show');
      }
    });

    return View;
  });