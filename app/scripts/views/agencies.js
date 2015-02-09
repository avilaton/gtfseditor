'use strict';

define([
  'underscore',
  'backbone',
  'JST',
  'collections/agencies'
  ], function (_, Backbone, JST, AgenciesCollection) {
    var View;

    View = Backbone.View.extend({
      // el: $('.main-view'),
      tagName: 'div',

      events: {
        'click button.save-btn': 'save',
        'click button.add-btn': 'add',
        'click button.btn-create': 'create',
        'blur .table-editable input[type="text"]': 'blur',
        'click button.btn-rm': 'rm',
        'click input[type="checkbox"]': 'onEditCheckbox'
      },

      template: JST.agencies,

      initialize: function(){
        this.collection = new AgenciesCollection();
        this.collection.on('add change remove reset', this.render, this);
        this.render();
        this.collection.fetch();
      },

      render: function () {
        this.$el.html(this.template({
          models: this.collection.toJSON()
        }));
        $('.main-view').empty().append(this.el);
        this.delegateEvents(this.events);
      },

      save: function () {
        this.collection.save();
      },

      create: function (e) {
        var agency_id = this.$('input.agency_id').val(),
          model;

        e.preventDefault();

        if (!agency_id) {
          alert('Invalid agency_id');
          return;
        }

        model = this.collection.create({
          agency_id: agency_id
        });
      },

      rm: function (e) {
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
      }

    });

    return View;
  });