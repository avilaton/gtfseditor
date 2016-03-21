define([
  'underscore',
  'backbone',
  'handlebars',
  'JST'
  ], function (_, Backbone, Handlebars, JST) {
    var View;

    View = Backbone.View.extend({

      template: JST['tripToolbox'],

      events: {
        'click button.prevStop': 'prevStop',
        'click button.nextStop': 'nextStop',
        'click button.removeStop': 'removeStop',
        'click button.appendStop': 'appendStop',
        'click button.btn-save': 'saveStops'
      },

      initialize: function(options){
        var self = this;

        $(document).bind('keyup', this.keypress.bind(self));

        this.render();

        this.collection.on('change reset', self.render, self);
      },

      render: function () {
        this.$el.html(this.template());
      },

      keypress : function (event) {
        if (event.keyCode == 82)
          this.removeStop();
      },

      prevStop: function (event) {
        var self = this;
        var selMember = this.collection.findWhere({'stop_id': self.model.get('stop_id')});
        if (selMember) {
          var index = this.collection.indexOf(selMember);
          var modelAbove = this.collection.at(index-1);
          if (modelAbove) {
            this.model.set(modelAbove.toJSON());
            this.collection.trigger('trip_stop_selected');
          };
        };
      },

      nextStop: function (event) {
        var self = this;
        var selMember = this.collection.findWhere({'stop_id': self.model.get('stop_id')});
        if (selMember) {
          var index = this.collection.indexOf(selMember);
          var modelBelow = this.collection.at(index+1);
          if (modelBelow) {
            this.model.set(modelBelow.toJSON());
            this.collection.trigger('trip_stop_selected');
          };
        };
      },

      removeStop: function (event) {
        var stop_id = this.model.get('stop_id');
        this.collection.removeStop(stop_id);
      },

      appendStop: function (event) {
        var stop = this.model;
        this.collection.appendStop(stop);
      },

      saveStops: function (event) {
        this.collection.save();
      }

    });

return View;
})