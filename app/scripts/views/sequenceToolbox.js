define([
  'underscore',
  'backbone',
  'handlebars',
  'JST'
  ], function (_, Backbone, Handlebars, JST) {
    var View;

    View = Backbone.View.extend({

      template: JST['sequenceToolbox'],

      events: {
        'click button.prevStop': 'prevStop',
        'click button.nextStop': 'nextStop',
        'click button.sortStops': 'sortStops',
        'click button.offsetStops': 'offsetStops',
        'click button.updateDist': 'updateDist',
        'click button.interpolateTimes': 'interpolateTimes',
        'click button.toggleMultipleSelect': 'toggleMultipleSelect',
        'click button.removeStop': 'removeStop',
        'click button.appendStop': 'appendStop',
        'click button.saveStops': 'saveStops'
      },

      initialize: function(options){
        var self = this;

        $(document).bind('keyup', this.keypress.bind(self));

        this.controls = options.controls;
        this.collection = options.collection;

        this.render();

        this.collection.on('change reset', self.render, self);
      },

      render: function () {
        var self = this;

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

      sortStops: function (event) {
        this.collection.sortStops();
      },

      offsetStops: function (event) {
        this.collection.alignTripStops();
      },

      updateDist: function (event) {
        this.collection.updateDist();
      },

      interpolateTimes: function (event) {
        this.collection.interpolateTimes();
      },

      toggleMultipleSelect: function (event) {
        var $target = $(event.currentTarget);

        $target.toggleClass('btn-primary');

        // this.controls.selectStops.deactivate();
        // this.controls.selectMultiple.activate();

        // this.controls.selectMultiple.deactivate();
        // this.controls.selectStops.activate();
      },

      editStops: function (event) {
        var $target = $(event.currentTarget);
        if (this.controls.selectStops.active) {
          $target.addClass('btn-primary');
          this.controls.selectStops.unselectAll();
          this.controls.selectStops.deactivate();
          this.controls.modifyStops.activate();
        } else {
          $target.removeClass('btn-primary');
          this.controls.modifyStops.deactivate();
          this.controls.selectStops.activate();
        }
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