define([
  'underscore',
  'backbone',
  'handlebars',
  'JST',
  'views/stopsList'
  ], function (_, Backbone, Handlebars, JST, StopsListView) {
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
        'click button.removeStop': 'removeStop',
        'click button.appendStop': 'appendStop',
        'click button.btn-speed': 'onClickSpeed',
        'click button.btn-add-stops': 'onClickAddStops',
        'keyup input.add-stops': 'onKeyUpAddStops',
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
        this.stopsListView = new StopsListView({
          el: '.results-view'
        });
        this.listenTo(this.stopsListView, 'add', function (stop_id) {
          this.collection.appendStopById(stop_id);
          this.collection.save();
          this.$('input.add-stops').val('');
        }, this);
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

      onClickSpeed: function (e) {
        e.preventDefault();
        var speed = this.$('input.speed').val();
        this.collection.setTimes({speed: speed|| 20.0});
      },

      onClickAddStops: function (e) {
        e.preventDefault();
        var input = this.$('input.add-stops').val(),
          stop_ids,
          collection = this.collection;

        _.each(input.split(','), function (item) {
          var stop_id = item.trim();
          if (stop_id !== '') {
            collection.appendStopById(item.trim());
          }
        });
      },

      onKeyUpAddStops: function (e) {
        var value = $(e.currentTarget).val(),
          inputField = this.$('input.add-stops'),
          self = this;
        if (value === '') {
          this.stopsListView.collection.reset();
        } else {
          $.ajax('/api/stops.json?limit=5&filter='+value).then(function (res) {
            self.stopsListView.collection.reset(res.stops);
            if (res.stops.length === 0) {
              inputField.parent().addClass('has-warning');
            } else {
              inputField.parent().removeClass('has-warning');

            }
          });
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