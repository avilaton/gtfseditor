define([
    "underscore",
    "backbone",
    "handlebars",
    "transit/templates",
    "text!transit/templates/routesSelect.handlebars",
    "transit/collections/trips"
], function (_, Backbone, Handlebars, templates, tmpl, TripsCollection) {
    var RoutesSelect;

    RoutesSelect = Backbone.View.extend({
        el: $("#routeBar"),
        
        template: Handlebars.compile(tmpl),

        events: {
            "change select": "selectRoute"
        },

        initialize: function(){
            var self = this;
            
            this.render();
            
            this.collection.on("change add remove reset", self.render, self);

            this.collection.on("route_selected", self.yamon, self);
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

    return RoutesSelect;
})