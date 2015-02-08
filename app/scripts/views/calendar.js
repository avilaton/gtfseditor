define([
  'underscore',
  'backbone',
  'JST',
  'collections/calendars'
  ], function (_, Backbone, JST, CalendarsCollection) {
    var View;

    View = Backbone.View.extend({
      el: $('.main-view'),

      events: {
        'click button.save-btn': 'save',
        'click button.add-btn': 'add',
        'blur .table-editable input[type="text"]': 'blur',
        'click button.btn-rm': 'remove',
        'click input[type="checkbox"]': 'onEditCheckbox'
      },

      template: JST['calendar'],

      initialize: function(){
        this.collection = new CalendarsCollection();
        this.collection.fetch();
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
        this.collection.add({});
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
        console.log(model.toJSON());
      },

      onEditCheckbox: function (e) {
        var $target = $(e.currentTarget),
          index = $target.closest('tr').data('index'),
          day = $target.attr('name'),
          value = String(Number($target.prop('checked'))),
          model = this.collection.at(index);
        console.log(day, value);
        model.set(day, value);
      }

    });

    return View;
  })