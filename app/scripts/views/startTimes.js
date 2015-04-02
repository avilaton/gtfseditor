'use strict';

define([
  'underscore',
  'backbone',
  'handlebars',
  'collections/calendars',
  'JST'
  ], function (_, Backbone, Handlebars, CalendarsCollection, JST) {
    var View;

    View = Backbone.View.extend({

      template: JST.startTimes,

      events: {
        'blur .table-editable input': 'blur',
        'click button.btn-rm': 'remove'
      },

      initialize: function(){
        this.render();
        this.collection.on('add change remove reset', this.render, this);
      },

      render: function () {
        this.$el.html(this.template({
          models: this.collection.toJSON()
        }));
      },

      remove: function (e) {
        var $target = $(e.currentTarget),
          index = $target.closest('tr').data('index'),
          model = this.collection.at(index);
        this.collection.remove(model);
      },

      blur: function (e) {
        var $target = $(e.currentTarget),
          index = $target.closest('tr').data('index'),
          attr = $target.data('attr'),
          model = this.collection.at(index);
        model.set(attr, $target.val());
      }
    });

    return View;
  });