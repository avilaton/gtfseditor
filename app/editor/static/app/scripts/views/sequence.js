define([
  "underscore",
  "backbone",
  "handlebars",
  'JST'
  ], function (_, Backbone, Handlebars, JST) {
    var View;

    View = Backbone.View.extend({

      template: JST['sequence'],

      events: {
        'click tr': 'onClickRow',
        'click td.stop-time': 'onClickStopTime',
        'keyup td.stop-time': 'onKeyUpStopTime',
        'blur td.stop-time': 'onBlurStopTime',
        'click a.remove-stop-time': 'onRmStopTime',
        'click a.move-stop-up': 'onMoveStopUp',
        'click a.move-stop-down': 'onMoveStopDown',
      },

      initialize: function(){
        this.render();
        this.dragRow = null;
        this.collection.on("add remove change reset", this.render, this);
      },

      render: function () {
        this.$el.html(this.template(this.collection.toJSONwithSpeed()));
      },

      onBlurStopTime: function (e) {
        var $target = $(e.currentTarget);
        var stop_index = $target.parent().data('stop-index');
        var model = this.collection.at(stop_index);
        model.set('stop_time', $target.text());
      },

      onClickRow: function (event) {
        var $target = $(event.currentTarget),
        stop_id = $target.data('stopId');
      },

      onClickStopTime: function (e) {
        var $target = $(event.currentTarget);
      },

      onKeyUpStopTime: function (e) {
        var $target = $(event.currentTarget);
      },

      onRmStopTime: function (e) {
        var $target = $(e.currentTarget);
        var stopIndex = $target.closest('tr').data('stopIndex');
        var model = this.collection.at(stopIndex);
        e.preventDefault();
        this.collection.remove(model);
      },

      onMoveStopUp: function (e) {
        var $target = $(e.currentTarget);
        var stopIndex = $target.closest('tr').data('stopIndex');
        var model = this.collection.at(stopIndex);
        e.preventDefault();
        this.collection.moveUp(model);
      },

      onMoveStopDown: function (e) {
        var $target = $(e.currentTarget);
        var stopIndex = $target.closest('tr').data('stopIndex');
        var model = this.collection.at(stopIndex);
        e.preventDefault();
        this.collection.moveDown(model);
      },

    });

    return View;
  })