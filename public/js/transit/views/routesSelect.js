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
            "change select": "selectRoute",
            'click .js-add': 'onAdd',
            'click .js-edit': 'onEdit',
            'click .js-remove': 'onRemove',
            'click .js-view-all': 'onViewAll'
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
        },

        onAdd: function (event) {
            console.log(event)
        },

        onEdit: function (event) {
            console.log(event)
        },

        onRemove: function (event) {
            console.log(event)
        },

        onViewAll: function (event) {
            console.log(event)
        }
    });

    return RoutesSelect;
})