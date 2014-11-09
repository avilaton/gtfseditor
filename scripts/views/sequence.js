define([
  "underscore",
  "backbone",
  "handlebars",
  'JST'
  ], function (_, Backbone, Handlebars, JST) {
    var View;

    View = Backbone.View.extend({
      el: $("#sequenceView"),

      template: JST['sequence'],

      events: {
        'click tr': 'onClickRow',
        'click td.stop-time': 'onClickStopTime',
        'keyup td.stop-time': 'onKeyUpStopTime',
        'dragstart tr': 'onDragStart',
        'dragenter tr': 'onDragEnter',
        'dragover tr': 'onDragOver',
        'dragleave tr': 'onDragLeave',
        'drop tr': 'onDrop'
      },

      initialize: function(){
        this.render();
        this.dragRow = null;
        this.collection.on("add remove change reset", this.render, this);
      },

      render: function () {
        this.$el.html(this.template(this.collection.toJSON()));
      },

      onClickRow: function (event) {
        var $target = $(event.currentTarget),
        stop_id = $target.data('stopId');
        console.log(event, stop_id);
      },

      onClickStopTime: function (e) {
        var $target = $(event.currentTarget);
        console.log(e);
      },

      onKeyUpStopTime: function (e) {
        var $target = $(event.currentTarget);
        console.log(e);
      },

      onDragStart: function (e) {
        var $target = $(e.currentTarget);
        console.log($target.data('stopId'), e);
        this.dragRow = e.originalEvent;
        e.originalEvent.dataTransfer.effectAllowed = 'move';
        e.originalEvent.dataTransfer.setData('text/html', this.dragRow.innerHTML);
      },

      onDragEnter: function (e) {
        var $target = $(e.currentTarget);
        // console.log($target.data('stopId'), e);
      },

      onDragOver: function (e) {
        var $target = $(e.currentTarget);
        // console.log($target.data('stopId'), e);
        if (e.originalEvent.preventDefault) {
          e.originalEvent.preventDefault(); // Necessary. Allows us to drop.
        }

        e.originalEvent.dataTransfer.dropEffect = 'move';  // See the section on the DataTransfer object.

        return false;
      },

      onDragLeave: function (e) {
        var $target = $(e.currentTarget);
        // console.log($target.data('stopId'), e);
      },

      onDrop: function (e) {
        var $target = $(e.currentTarget);
        console.log($target.data('stopId'), e);
        if (e.originalEvent.stopPropagation) {
          e.originalEvent.stopPropagation(); // stops the browser from redirecting.
        }
        this.dragRow.innerHTML = e.originalEvent.innerHTML;
        e.originalEvent.innerHTML = this.dragRow.dataTransfer.getData('text/html');
      }
    });

    return View;
  })