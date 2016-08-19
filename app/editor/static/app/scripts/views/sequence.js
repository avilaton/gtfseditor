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

      onRmStopTime: function (e) {
        var $target = $(e.currentTarget),
          stop_id = $target.closest('tr').data('stopId');
        e.preventDefault();
        this.collection.removeStop(stop_id);
      },

    });

    return View;
  })