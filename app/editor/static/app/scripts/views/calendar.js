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
        'click a.btn-create': 'onCreate',
        'click a.btn-rm': 'onRemove',
        'click a.btn-edit': 'onEdit'
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
          serviceId = $target.closest('li').data('serviceId'),
          model = this.collection.get(serviceId),
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
          serviceId = $target.closest('li').data('serviceId'),
          model = this.collection.get(serviceId);
        model.destroy();
      }
    });

    return View;
  });