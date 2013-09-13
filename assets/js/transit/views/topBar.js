define([
    "underscore",
    "backbone",
    "handlebars",
    "text!transit/templates/topBar.handlebars",
    "transit/collections/trips"
], function (_, Backbone, Handlebars, tmpl, TripsCollection) {
    var tripsSelect;

    tripsSelect = Backbone.View.extend({
        el: $("#topBar"),

        template: Handlebars.compile(tmpl),

        events: {
            "change select": "selectTrip"
        },

        initialize: function(){
            var self = this;
            
            this.render();
        },

        render: function () {
            var self = this;

            this.$el.html(this.template({
                // routesSelect: "hello"
                // routes: self.collection.toJSON()
            }));
        }

    });

    return tripsSelect;
})