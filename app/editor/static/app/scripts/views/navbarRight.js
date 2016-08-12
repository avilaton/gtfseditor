define([
  'backbone',
  'handlebars',
  'JST'
  ], function (Backbone, Handlebars, JST) {
    var View;

    View = Backbone.View.extend({
      el: $('.js-navbar-right'),

      template: JST['navbarRight'],

      initialize: function(options){
        this.render();
      },

      render: function () {
        this.$el.html(this.template());
      }
    });

    return View;
  })