define([
    "underscore",
    "backbone",
    "handlebars",
    "text!transit/templates/tripsSelect.handlebars",
    "transit/collections/trips"
], function (_, Backbone, Handlebars, tmpl, TripsCollection) {
    var tripsSelect;

    tripsSelect = Backbone.View.extend({

        template: Handlebars.compile(tmpl),

        events: {
            "change select": "selectTrip"
        },

        initialize: function(){
            var self = this;
            
            this.render();
            
            this.collection.on("change add remove reset", self.render, self);

            this.collection.on("trip_selected", self.yamon, self);
        },

        render: function () {
            var self = this;

            this.$el.html(this.template({
                routes: self.collection.toJSON()
            }));
        },

        selectRoute: function (event) {
            var self = this;
            var selectedValue = event.currentTarget.value;

            self.collection.select(selectedValue);

            self.collection.trigger("route_selected");

        },

        yamon: function (event) {
            var routeModel = this.collection.selected;
            var trips = new TripsCollection(routeModel);
            trips.fetch();
            this.trips = trips.toJSON();
            console.log(this);
        }
    });

    return tripsSelect;
})