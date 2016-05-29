'use strict';

define([
  'underscore',
  'backbone',
  'JST'
  ], function (_, Backbone, JST) {
    var View;

    View = Backbone.View.extend({
      events: {
        'click .btn-add-stop': 'onClickAdd'
      },

      template: JST.stopsList,

      initialize: function(){
        this.collection = new Backbone.Collection();
        this.collection.on('add change remove reset', this.render, this);
        this.render();
      },

      render: function () {
        this.$el.html(this.template({
          stops: this.collection.toJSON()
        }));
      },

      onClickAdd: function (e) {
        var stop_id = $(e.currentTarget).data('stopId');
        this.trigger('add', stop_id);
        console.log('add', stop_id);
        this.collection.reset();
      }
    });

    return View;
  });