define([
  "underscore",
  "backbone",
  "handlebars",
  "text!templates/tripsSelect.handlebars",
  "collections/trips",
  'models/trip',
  'views/modals/trip'
  ], function (_, Backbone, Handlebars, tmpl, TripsCollection, TripModel, TripModal) {
    var View;

    View = Backbone.View.extend({
      el: $("#tripsSelect"),

      template: Handlebars.compile(tmpl),

      events: {
          "change select": "selectTrip",
          'click .js-add': 'onAdd',
          'click .js-edit': 'onEdit',
          'click .js-remove': 'onRemove',
          'click .js-view-all': 'onViewAll'
      },

      initialize: function(options){
        var self = this;

        self.routesCollection = options.routesCollection;

        self.routesCollection.on('route_selected', self.routeChanged, self);

        this.render();
        
        this.collection.on("change add remove reset", self.render, self);
      },

      routeChanged: function (event) {
        this.collection.route_id = event.get("route_id");
        this.collection.fetch();
      },

      render: function () {
        var self = this;

        this.$el.html(this.template({
          trips: self.collection.toJSON()
        }));
      },

      selectTrip: function (event) {
        var self = this;
        var selectedValue = event.currentTarget.value;

        self.collection.select(selectedValue);
      },

      onAdd: function () {
        var model = new TripModel();
        var tripModal = new TripModal({
            model: model,
            el: $('#routeDataEditor')
        });
        tripModal.$el.modal('show');
      },

      onEdit: function () {
        var tripModal = new TripModal({
            model: this.collection.selected,
            el: $('#routeDataEditor')
        });
        tripModal.$el.modal('show');
      },

      onRemove: function () {
        this.collection.selected.destroy();
      },

      onViewAll: function () {
        console.log(event)
      }
    });

    return View;
  })