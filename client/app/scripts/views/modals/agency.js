'use strict';

define([
  'underscore',
  'backbone',
  'handlebars',
  'JST'
], function (_, Backbone, Handlebars, JST) {
  var View;

  View = Backbone.View.extend({
    template: JST['modals/agency'],

    events: {
      'click .js-save': 'save',
      'keyup input': 'onEdit',
      'hidden.bs.modal': 'teardown'
    },

    initialize: function(){
      this.render();
    },

    render: function () {
      var self = this;
      this.$el.html(this.template(this.model.toJSON()));
    },

    save: function (event) {
      var self = this;
      this.model.save().then(function () {
        self.$el.modal('hide');
      });
    },

    onEdit: function (event) {
      var $target = $(event.currentTarget);
      this.model.set($target.attr('name'), $target.val());
    },

    teardown: function() {
      this.undelegateEvents();
    }
  });

  return View;
});