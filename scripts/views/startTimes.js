define([
  'underscore',
  'backbone',
  'handlebars',
  'collections/calendars',
  'JST'
  ], function (_, Backbone, Handlebars, CalendarsCollection, JST) {
    var View;

    View = Backbone.View.extend({

      template: JST['startTimes'],

      events: {
        'click button.save-btn': 'save',
        'click button.add-btn': 'add',
        'blur .table-editable input': 'blur',
        'blur .table-editable select': 'blur',
        'click button.btn-rm': 'remove'
      },

      initialize: function(){
        var self = this;
        this.calendars = new CalendarsCollection();
        this.calendars.fetch().then(function (response) {
          self.service_ids = self.calendars.pluck('service_id');
        });
        this.render();

        this.collection.on('add remove reset', self.render, self);
      },

      render: function () {
        var self = this;

        this.$el.html(this.template({
          models: this.collection.toJSON(),
          service_ids: this.service_ids
        }));
      },

      save: function () {
        this.collection.save();
      },

      add: function () {
        this.collection.add({
          trip_id: this.collection.trip_id
        });
      },

      remove: function (e) {
        var $target = $(e.currentTarget),
          index = $target.closest('tr').data('index'),
          model = this.collection.at(index);
        this.collection.remove(model);
      },

      blur: function (e) {
        var $target = $(e.currentTarget),
          index = $target.closest('tr').data('index'),
          attr = $target.data('attr'),
          model = this.collection.at(index);
        model.set(attr, $target.val());
      }
    });

    return View;
  })