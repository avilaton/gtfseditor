define([
    "underscore",
    "backbone",
    "handlebars",
    "text!transit/templates/modal.handlebars"
], function (_, Backbone, Handlebars, tmpl) {
    var View;

    View = Backbone.View.extend({
        
        template: Handlebars.compile(tmpl),

        events: {},

        initialize: function(options){
            this.render();
        },

        render: function () {
            var self = this;

            this.$el.html(this.template({}));
        }
    });

    return View;
})