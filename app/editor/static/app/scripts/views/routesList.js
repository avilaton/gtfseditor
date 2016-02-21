'use strict';

define([
  'underscore',
  'backbone',
  'JST',
  'models/route',
  'collections/routes',
  'views/modals/route'
  ], function (_, Backbone, JST, RouteModel, RoutesCollection, RouteModal) {
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
        this.collection = new RoutesCollection();
        this.collection.on('add change remove reset', this.render, this);
        this.render();
        this.collection.fetch();
      },

      render: function () {
        this.$el.html(this.template({
          models: this.collection.toJSON()
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