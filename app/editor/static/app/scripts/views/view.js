'use strict';

define([
  'underscore',
  'backbone',
  'handlebars',
  'text!templates/view.handlebars'
  ], function (_, Backbone, Handlebars, tmpl) {
    var View;

    View = Backbone.View.extend({
      el: $('#someDomElementId'),

      template: Handlebars.compile(tmpl),

      events: {},

      initialize: function(){
        this.render();
        this.model.on('change reset', this.render, this);
      },

      render: function () {
        this.$el.html(this.template());
      }

    });

    return View;
  });