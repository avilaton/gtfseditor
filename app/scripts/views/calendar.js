'use strict';

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
        'click button.btn-create': 'create',
        'blur .table-editable input[type="text"]': 'blur',
        'click button.btn-rm': 'remove',
        'click input[type="checkbox"]': 'onEditCheckbox'
      },

      template: JST.calendar,

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

      create: function (e) {
        var service_id = this.$('input.service_id').val(),
          model;

        e.preventDefault();

        if (!service_id) {
          alert('Invalid service_id');
          return;
        }

        model = this.collection.create({
          service_id: service_id
        });
      },

      remove: function (e) {
        var $target = $(e.currentTarget),
          index = $target.closest('tr').data('index'),
          model = this.collection.at(index);
        model.destroy();
      },

      blur: function (e) {
        var $target = $(e.currentTarget),
          index = $target.closest('tr').data('index'),
          attr = $target.data('attr'),
          model = this.collection.at(index);
        model.set(attr, $target.val());
      },

      onEditCheckbox: function (e) {
        var $target = $(e.currentTarget),
          index = $target.closest('tr').data('index'),
          day = $target.attr('name'),
          value = String(Number($target.prop('checked'))),
          model = this.collection.at(index);
        model.set(day, value);
      }

    });

    return View;
  });