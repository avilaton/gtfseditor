'use strict';

define([
  'underscore',
  'backbone',
  'handlebars',
  'JST'
], function (_, Backbone, Handlebars, JST) {
  var View;

  View = Backbone.View.extend({

    template: JST.calendarsTools,

    events: {
      'click button.save-btn': 'save',
      'click button.add-btn': 'add',
      'click button.btn-offset': 'onClickOffset'
    },

    initialize: function(){
      this.render();
    },

    render: function () {
      this.$el.html(this.template());
    },

    save: function (e) {
      e.preventDefault();
      this.collection.save();
    },

    add: function (e) {
      e.preventDefault();
      this.collection.add({
        trip_id: this.collection.trip_id,
        service_id: this.collection.service_id
      });
    },

    onClickOffset: function (e) {
      e.preventDefault();
      var offset = this.$('input.offset-min').val();
      this.collection.offsetTimes({offset: offset || 10});
    }
  });

  return View;
});