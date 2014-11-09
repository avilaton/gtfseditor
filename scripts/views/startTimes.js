define([
  'underscore',
  'backbone',
  'handlebars',
  'JST'
  ], function (_, Backbone, Handlebars, JST) {
    var View;

    View = Backbone.View.extend({

      template: JST['startTimes'],

      events: {},

      initialize: function(){
        var self = this;

        this.render();

        this.collection.on('change reset', self.render, self);
      },

      render: function () {
        var self = this;
        console.log(this.collection.toJSON());

        this.$el.html(this.template(this.collection.toJSON()));
      }

    });

    return View;
  })