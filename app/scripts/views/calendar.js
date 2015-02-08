define([
  'underscore',
  'backbone',
  'JST',
  'collections/calendars'
  ], function (_, Backbone, JST, CalendarsCollection) {
    var View;

    View = Backbone.View.extend({
      el: $('.main-view'),

      template: JST['calendar'],

      initialize: function(){
        this.collection = new CalendarsCollection();
        this.collection.fetch();
        this.render();
        this.collection.on('add change remove reset', this.render, this);
      },

      render: function () {
        console.log(this.collection.toJSON());
        this.$el.html(this.template({
          models: this.collection.toJSON()
        }));
      }

    });

    return View;
  })