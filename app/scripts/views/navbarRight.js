define([
  'backbone',
  'handlebars',
  'text!templates/navbarRight.handlebars'
  ], function (Backbone, Handlebars, tmpl) {
    var View;

    View = Backbone.View.extend({
      el: $('.js-navbar-right'),

      template: Handlebars.compile(tmpl),

      initialize: function(options){
        this.render();
      },

      render: function () {
        this.$el.html(this.template());
      }
    });

    return View;
  })