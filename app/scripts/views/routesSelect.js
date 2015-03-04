define([
    "underscore",
    "backbone",
    "handlebars",
    'JST',
    'collections/routes',
    'views/modals/route'
], function (_, Backbone, Handlebars, JST, RoutesCollection, RouteModal) {
    var View;

    View = Backbone.View.extend({

        template: JST['routesSelect'],

        events: {
            "change select": "selectRoute",
            'click .js-add': 'onAdd',
            'click .js-edit': 'onEdit',
            'click .js-remove': 'onRemove',
            'click .js-view-all': 'onViewAll'
        },

        initialize: function(){
            var self = this;

            this.collection = new RoutesCollection();

            this.collection.on("change add remove reset", self.render, self);
            this.collection.fetch();
        },

        render: function () {
            var self = this;

            this.$el.html(this.template({
                routes: self.collection.toJSON()
            }));
        },

        selectRoute: function (event) {
            var value = event.currentTarget.value;
            this.selected = value;
            this.trigger('select', value);
        },

        onAdd: function () {
            var model = new this.collection.model();
            var routeModal = new RouteModal({
                model: model,
                el: $('#routeDataEditor')
            });
            routeModal.$el.modal('show');
        },

        onEdit: function () {
            var model = this.collection.get(this.selected);
            var routeModal = new RouteModal({
                model: model,
                el: $('#routeDataEditor')
            });
            routeModal.$el.modal('show');
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