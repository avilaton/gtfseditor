define([
  'underscore',
  'backbone',
  'handlebars',
  'JST',
  'models/shape'
  ], function (_, Backbone, Handlebars, JST, ShapeModel) {
    var View;

    View = Backbone.View.extend({
      template: JST.shapesToolbox,

      events: {
        'click button.create-shape': 'onCreate',
        'click button.reverseShape': 'onReverseShape',
        'click button.editShape': 'onEditShape',
        'click button.delete': 'onDelete',
        'click button.saveShape': 'onSave'
      },

      initialize: function(options){
        var self = this;

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

      onCreate: function () {
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
        };
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
        this.model.destroy();
      }
    });

    return View;
  })