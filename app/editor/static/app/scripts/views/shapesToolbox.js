'use strict';

define([
  'underscore',
  'backbone',
  'handlebars',
  'JST'
  ], function (_, Backbone, Handlebars, JST) {
    var View;

    View = Backbone.View.extend({
      template: JST.shapesToolbox,

      events: {
        'click button.create-shape': 'onClickCreate',
        'click button.reverseShape': 'onReverseShape',
        'click button.editShape': 'onEditShape',
        'click button.btn-delete-shape': 'onDelete',
        'click button.saveShape': 'onSave',
        'click button.btn-cancel': 'onCancel'
      },

      initialize: function(options){
        this.controls = options.controls;
        this.map = options.map;
        this.isEditing = false;
        this.isCreating = false;
        this.listenTo(this.model, 'change:shape_id', this.render, this);
      },

      render: function () {
        this.$el.html(this.template({
          isEditing: this.isEditing,
          isCreating: this.isCreating,
          shape_id: this.model.get('shape_id')
        }));
      },

      startEditing: function () {
        this.isEditing = true;
        this.isCreating = false;
        this.render();
      },

      stopEditing: function () {
        this.isEditing = false;
        this.isCreating = false;
        if (this.controls.modifyShape.active) {
          this.map.activateControl('selectStops');
          this.map.updateShapesLayer();
        }
        this.render();
      },

      startCreating: function () {
        this.isEditing = false;
        this.isCreating = true;
        this.render();
      },

      stopCreating: function () {
        this.isEditing = false;
        this.isCreating = false;
        this.render();
      },

      onClickCreate: function () {
        this.startCreating();
        if (!this.controls.drawShape.active) {
          this.map.activateControl('drawShape');
        }
      },

      onReverseShape: function () {
        this.model.reverse();
      },

      onSave: function () {
        var self = this;
        this.map.activateControl('selectStops');
        this.map.updateShapeModel();
        if (this.isEditing) {
          this.model.sync('update', this.model);
          this.stopEditing();
        } else if (this.isCreating) {
          this.model.sync('create', this.model).then(function () {
            self.model.trigger('created');
            self.stopCreating();
          });
        }
      },

      onEditShape: function () {
        this.startEditing();
        if (!this.controls.modifyShape.active) {
          this.map.activateControl('modifyShape');
        } else {
          this.map.activateControl('selectStops');
          this.map.updateShapeModel();
        }
      },

      onDelete: function () {
        var self = this;
        this.model.destroy().then(function (response) {
          console.log('destroy response', response);
          console.log(self.model);
          self.model.clear();
          self.map.updateShapesLayer();
        });
      },

      onCancel: function () {
        this.stopEditing();
        this.stopCreating();
      }
    });

    return View;
  });
