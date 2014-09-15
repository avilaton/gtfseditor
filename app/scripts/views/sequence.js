define([
  "underscore",
  "backbone",
  "handlebars",
  "text!templates/sequence.handlebars"
  ], function (_, Backbone, Handlebars, tmpl) {
    var View;

    View = Backbone.View.extend({
      el: $("#sequenceView"),

      template: Handlebars.compile(tmpl),

      events: {},

      initialize: function(){
        var self = this;

        this.render();

        this.collection.on("add remove change reset", self.render, self);
      },

      render: function () {
        var self = this;
        console.log('sequence view', this.collection.toJSON());

        this.$el.html(this.template(this.collection.toJSON()));
      }

    });

    return View;
  })