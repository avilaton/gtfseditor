'use strict';

define([
  'underscore',
  'backbone',
  'handlebars',
  'JST'
], function (_, Backbone, Handlebars, JST) {
  var View;

  View = Backbone.View.extend({
    template: JST['modals/calendar'],

    events: {
      'click .js-save': 'save',
      'keyup input': 'onEdit',
      'click input[type="checkbox"]': 'onEditCheckbox',
      'hidden.bs.modal': 'teardown'
    },

    initialize: function(){
      this.render();
    },

    render: function () {
      this.$el.html(this.template(this.model.toJSON()));
    },

    save: function () {
      var self = this;
      this.model.save().then(function () {
        self.$el.modal('hide');
      });
    },

    onEdit: function (event) {
      var $target = $(event.currentTarget);
      this.model.set($target.attr('name'), $target.val());
    },

    onEditCheckbox: function (event) {
        var $target = $(event.currentTarget);
        this.model.set( $target.prop('name'), $target.prop('checked')? '1': '0');
    },

    teardown: function() {
      this.undelegateEvents();
    }
  });

  return View;
});