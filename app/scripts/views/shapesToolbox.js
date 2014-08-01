define([
  "underscore",
  "backbone",
  "handlebars",
  "text!templates/shapesToolbox.handlebars"
  ], function (_, Backbone, Handlebars, tmpl) {
    var View;

    View = Backbone.View.extend({
      el: $("#shapesToolbox"),

      template: Handlebars.compile(tmpl),

      events: {
        "click button.reverseShape": "reverseShape",
        "click button.editShape": "editShape",
        "click button.saveShape": "saveShape"
      },

      initialize: function(options){
        var self = this;

        this.controls = options.controls;
        this.map = options.map;

        this.render();

        this.model.on("change reset", self.render, self);
      },

      render: function () {
        var self = this;

        this.$el.html(this.template());
      },

      reverseShape: function (event) {
        this.model.reverse();
      },

      saveShape: function (event) {
        this.model.save();
      },

      editShape: function () {
        var $target = $(event.target);
        console.log("controls status", this.controls.modifyShape);
        if (!this.controls.modifyShape.active) {
          this.map.activateControl("modifyShape");
          $target.addClass('btn-primary');
        } else {
          this.map.activateControl("selectStops");
          this.map.updateShapeModel();
          $target.removeClass('btn-primary');
        }
      }
    });

    return View;
  })