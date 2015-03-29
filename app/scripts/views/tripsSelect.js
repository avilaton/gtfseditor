define([
  "underscore",
  "backbone",
  "handlebars",
  'JST',
  "collections/trips",
  'views/modals/trip'
  ], function (_, Backbone, Handlebars, JST, TripsCollection, TripModal) {
    var View;

    View = Backbone.View.extend({
      el: $("#tripsSelect"),

      template: JST['tripsSelect'],

      events: {
          "change select": "selectTrip",
          'click .js-add': 'onAdd',
          'click .js-edit': 'onEdit',
          'click .js-remove': 'onRemove',
          'click .js-view-all': 'onViewAll'
      },

      initialize: function(options){
        var self = this;

        this.collection = new TripsCollection();
        
        this.collection.on("change add remove reset", self.render, self);
        this.render();
      },

      render: function () {
        var self = this;

        this.$el.html(this.template({
          trips: self.collection.toJSON()
        }));
      },

      selectTrip: function (event) {
        var self = this;
        var value = event.currentTarget.value;
        this.selected = value;

        self.collection.select(value);
        this.trigger('select', value);
      },

      onAdd: function () {
        var model = this.collection.create();
        var tripModal = new TripModal({
            model: model,
            el: $('#routeDataEditor')
        });
        tripModal.$el.modal('show');
      },

      onEdit: function () {
        var model = this.collection.get(this.selected);
        var tripModal = new TripModal({
            model: model,
            el: $('#routeDataEditor')
        });
        tripModal.$el.modal('show');
      },

      onRemove: function () {
        var model = this.collection.get(this.selected);
        model.destroy();
      },

      onViewAll: function () {
        console.log(event)
      }
    });

    return View;
  })