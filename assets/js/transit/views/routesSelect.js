define([
    "underscore",
    "backbone",
    "handlebars",
    "text!transit/templates/routesSelect.handlebars",
    "transit/collections/trips"
], function (_, Backbone, Handlebars, tmpl, TripsCollection) {
    var RoutesSelect;

    RoutesSelect = Backbone.View.extend({
        el: $("#routesSelect"),
        
        template: Handlebars.compile(tmpl),

        events: {
            "change select": "selectRoute"
        },

        initialize: function(){
            var self = this;
            
            this.render();
            
            this.collection.on("change add remove reset", self.render, self);
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
        }
    });

    return RoutesSelect;
})