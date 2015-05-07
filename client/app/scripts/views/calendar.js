'use strict';

define([
  'underscore',
  'backbone',
  'JST',
  'collections/calendars',
  'views/modals/calendar'
  ], function (_, Backbone, JST, CalendarsCollection, Modal) {
    var View;

    View = Backbone.View.extend({
      tagName: 'div',

      events: {
        'click button.btn-create': 'onCreate',
        'click button.btn-rm': 'onRemove',
        'click button.btn-edit': 'onEdit'
      },

      template: JST.calendar,

      initialize: function(){
        this.collection = new CalendarsCollection();
        this.collection.fetch();
        this.collection.on('add change remove reset', this.render, this);
        this.render();
      },

      render: function () {
        this.$el.html(this.template({
          models: this.collection.toJSON()
        }));
        $('.main-view').empty().append(this.el);
        this.delegateEvents(this.events);
      },

      onCreate: function (e) {
        var model = this.collection.create();
        var modal = new Modal({
          model: model,
          el: $('#routeDataEditor')
        });
        modal.$el.modal('show');
      },

      onEdit: function (e) {
        var $target = $(e.currentTarget),
          index = $target.closest('tr').data('index'),
          model = this.collection.at(index),
          modal = new Modal({
            model: model,
            el: $('#routeDataEditor')
        });
        modal.$el.modal('show');
      },

      onRemove: function (e) {
        var $target = $(e.currentTarget),
          index = $target.closest('tr').data('index'),
          model = this.collection.at(index);
        model.destroy();
      }
    });

    return View;
  });