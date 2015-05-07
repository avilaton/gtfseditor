'use strict';

define([
  'underscore',
  'backbone',
  'handlebars',
  'JST',
  'collections/calendars'
], function (_, Backbone, Handlebars, JST, CalendarsCollection) {
  var View;

  View = Backbone.View.extend({

    template: JST.calendarsSelect,

    events: {
      'change select': 'selectRoute'
    },

    initialize: function(){
      var self = this;
      this.collection = new CalendarsCollection();
      this.collection.fetch();
      this.collection.on('add change remove reset', this.render, this);
      this.render();
    },

    render: function () {
      this.$el.html(this.template({
          models: this.collection.toJSON()
      }));
    },

    selectRoute: function (event) {
      var value = event.currentTarget.value;
      this.selected = value;
      this.trigger('select', value);
    }
  });

  return View;
});