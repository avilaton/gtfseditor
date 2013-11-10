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

        this.controls = options.controls;

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
      },

      editShape: function () {
        var $target = $(event.currentTarget);
        if (this.controls.selectStops.active) {
          // $target.addClass('btn-primary');
          //this.controls.selectStops.unselectAll();
          //this.controls.selectStops.deactivate();
          //this.controls.modifyStops.activate();
        } else {
          // $target.removeClass('btn-primary');
          //this.controls.modifyStops.deactivate();
          //this.controls.selectStops.activate();
        }
      }
    });

    return View;
  })