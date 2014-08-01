define([
    "underscore",
    "backbone",
    "handlebars",
    "text!templates/routesSelect.handlebars",
    "collections/trips",
    'models/route',
    'views/modals/route'
], function (_, Backbone, Handlebars, tmpl, TripsCollection, RouteModel, RouteModal) {
    var View;

    View = Backbone.View.extend({
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

        onAdd: function () {
            var model = new RouteModel();
            var routeModal = new RouteModal({
                model: model,
                el: $('#routeDataEditor')
            });
            routeModal.$el.modal('show');
        },

        onEdit: function () {
            var routeModal = new RouteModal({
                model: this.collection.selected,
                el: $('#routeDataEditor')
            });
            routeModal.$el.modal('show');
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