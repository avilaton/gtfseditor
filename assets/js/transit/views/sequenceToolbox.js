define([
  "underscore",
  "backbone",
  "handlebars",
  "text!transit/templates/sequenceToolbox.handlebars"
  ], function (_, Backbone, Handlebars, tmpl) {
    var View;

    View = Backbone.View.extend({
      el: $("#sequenceToolbox"),

      template: Handlebars.compile(tmpl),

      events: {
        "click button.prevStop": "prevStop",
        "click button.nextStop": "nextStop"
      },

      initialize: function(options){
        var self = this;

        this.render();

        this.collection.on("change reset", self.render, self);
      },

      render: function () {
        var self = this;

        this.$el.html(this.template());
      },

      prevStop: function (event) {
        this.collection.skipSelect(1);
      },

      nextStop: function (event) {
        this.collection.skipSelect(-1);
      }
    });

    return View;
  })