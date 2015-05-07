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
        'click button.create-shape': 'create',
        'click button.reverseShape': 'reverseShape',
        'click button.editShape': 'editShape',
        'click button.delete': 'delete',
        'click button.saveShape': 'save'
      },

      initialize: function(options){
        var self = this;

        this.controls = options.controls;
        this.map = options.map;

        this.render();
      },

      render: function () {
        this.$el.html(this.template());
      },

      create: function () {
        var $target = $(event.target);
        if (!this.controls.drawShape.active) {
          this.map.activateControl('drawShape');
          $target.addClass('btn-primary');
        } else {
          this.map.activateControl('selectStops');
          this.map.updateShapeModel();
          $target.removeClass('btn-primary');
          this.model.sync('create', this.model);
        }
      },

      reverseShape: function (event) {
        this.model.reverse();
      },

      save: function (event) {
        this.model.sync('update', this.model);
      },

      editShape: function () {
        var $target = $(event.target);
        if (!this.controls.modifyShape.active) {
          this.map.activateControl('modifyShape');
          $target.addClass('btn-primary');
        } else {
          this.map.activateControl('selectStops');
          this.map.updateShapeModel();
          $target.removeClass('btn-primary');
        }
      },

      delete: function () {
        this.model.destroy();
      }
    });

    return View;
  })