define([
    "underscore",
    "backbone",
    "handlebars",
    "text!transit/templates/tripsSelect.handlebars",
    "transit/collections/trips"
], function (_, Backbone, Handlebars, tmpl, TripsCollection) {
    var tripsSelect;

    tripsSelect = Backbone.View.extend({
        el: $("#tripsSelect"),

        template: Handlebars.compile(tmpl),

        events: {
            "change select": "selectTrip"
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
        }
    });

    return tripsSelect;
})