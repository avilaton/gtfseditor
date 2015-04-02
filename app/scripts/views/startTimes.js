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
        'click button.btn-offset': 'onClickOffset',
        'blur .table-editable input': 'blur',
        'blur .table-editable select': 'blur',
        'click button.btn-rm': 'remove'
      },

      initialize: function(){
        this.render();
        this.collection.on('add change remove reset', this.render, this);
      },

      render: function () {
        this.$el.html(this.template({
          models: this.collection.toJSON()
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
      },

      onClickOffset: function (e) {
        e.preventDefault();
        var offset = this.$('input.offset-min').val();
        this.collection.offsetTimes({offset: offset || 10});
      }
    });

    return View;
  })