define([
    "underscore",
    "backbone",
    "handlebars",
    "text!templates/modal.handlebars",
    'api'
], function (_, Backbone, Handlebars, tmpl, Api) {
    var View;

    View = Backbone.View.extend({
        
        template: Handlebars.compile(tmpl),

        events: {
            "click .btn-save": "saveRoute",
            "keyup input": 'onEdit'
        },

        initialize: function(options){
            var self = this;
            this.render();
            this.collection.on("route_selected", self.render, self);
        },

        render: function () {
            var self = this;

            this.$el.html(this.template(this.collection.selected.toJSON()));
        },

        saveRoute: function (event) {
            var routeData = this.collection.selected.toJSON();
            var route_id = this.collection.selected.get('route_id');
            console.log(route_id, routeData);
            Api.post({
                url: 'api/routes/' + route_id,
                data: JSON.stringify(routeData)
            }).done(function (response) {
                console.log(response)
            });
        },

        onEdit: function (event) {
            var $target = $(event.currentTarget);
            this.collection.selected.set($target.attr('name'), $target.val());
        }
    });

    return View;
})