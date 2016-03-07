'use strict';

define([
  'underscore',
  'backbone',
  'JST',
  'models/calendar',
  'collections/calendars',
  'views/modals/calendar'
  ], function (_, Backbone, JST, CalendarModel, CalendarsCollection, Modal) {
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
        this.collection.fetch({reset: true});
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
        e.preventDefault();
        var model = new CalendarModel();
        var modal = new Modal({
          model: model,
          collection: this.collection,
          el: $('#routeDataEditor')
        });
        modal.$el.modal('show');
      },

      onEdit: function (e) {
        e.preventDefault();
        var $target = $(e.currentTarget),
          index = $target.closest('tr').data('index'),
          model = this.collection.at(index),
          modal = new Modal({
            model: model,
            collection: this.collection,
            el: $('#routeDataEditor')
        });
        modal.$el.modal('show');
      },

      onRemove: function (e) {
        e.preventDefault();
        var $target = $(e.currentTarget),
          index = $target.closest('tr').data('index'),
          model = this.collection.at(index);
        model.destroy();
      }
    });

    return View;
  });