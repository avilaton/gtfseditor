define([
  "underscore",
  "backbone",
  "handlebars",
  "text!transit/templates/shapesToolbox.handlebars"
  ], function (_, Backbone, Handlebars, tmpl) {
    var View;

    View = Backbone.View.extend({
      el: $("#shapesToolbox"),

      template: Handlebars.compile(tmpl),

      events: {
        "click button.revertShape": "revertShape",
        "click button.editShape": "editShape",
        "click button.saveShape": "saveShape"
      },

      initialize: function(options){
        var self = this;

        this.render();

        this.model.on("change reset", self.render, self);
      },

      render: function () {
        var self = this;

        this.$el.html(this.template());
      },

      revertShape: function (event) {
        this.model.reverse();
      },

      saveShape: function (event) {
        this.model.save();
      }
    });

    return View;
  })