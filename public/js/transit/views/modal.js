define([
    "underscore",
    "backbone",
    "handlebars",
    "text!transit/templates/modal.handlebars"
], function (_, Backbone, Handlebars, tmpl) {
    var View;

    View = Backbone.View.extend({
        
        template: Handlebars.compile(tmpl),

        events: {
            "click .btn-save": "saveRoute"
        },

        initialize: function(options){
            var self = this;
            this.render();
            this.collection.on("route_selected", self.render, self);
        },

        render: function () {
            var self = this;
            console.log(this);

            this.$el.html(this.template(this.collection.selected.toJSON()));
        },

        saveRoute: function (event) {
            console.log(this)
        }
    });

    return View;
})