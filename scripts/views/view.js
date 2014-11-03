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
        var self = this;

        this.render();

        this.model.on('change reset', self.render, self);
      },

      render: function () {
        var self = this;

        this.$el.html(this.template());
      }

    });

    return View;
  })