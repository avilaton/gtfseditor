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
      'click button.btn-offset': 'onClickOffset',
      'click button.btn-bulk-load': 'onClickBulk',
      'click button.btn-reset': 'onClickReset'
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
    },

    onClickBulk: function (e) {
      var self = this,
        text = this.$('textarea.bulk-load').val(),
        values;
      e.preventDefault();
      if (!this.collection.trip_id || !this.collection.service_id) {
        return;
      }
      values = _.map(text.split(/[ ,\n]+/), function (item, idx) {
        return {
          start_time: item.trim() + ':00',
          trip_id: self.collection.trip_id,
          service_id: self.collection.service_id
        };
      });
      this.collection.add(values);
      this.$('textarea.bulk-load').val('');
    },

    onClickReset: function (e) {
      e.preventDefault();
      this.collection.reset();
    }
  });

  return View;
});