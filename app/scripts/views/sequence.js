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
        'drop tr': 'onDrop',
        'click button.btn-save': 'onClickSave',
        'click button.btn-speed': 'onClickSpeed',
        'click button.btn-add-stops': 'onClickAddStops',
        'blur td.stop-time': 'onBlurStopTime'
      },

      initialize: function(){
        this.render();
        this.dragRow = null;
        this.collection.on("add remove change reset", this.render, this);
      },

      render: function () {
        this.$el.html(this.template(this.collection.toJSONwithSpeed()));
      },

      onClickSave: function (e) {
        this.collection.save();
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

      onBlurStopTime: function (e) {
        var $target = $(e.currentTarget);
        var stop_id = $target.parent().data('stop-id');
        var model = this.collection.get(stop_id);
        model.set('stop_time', $target.text());
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