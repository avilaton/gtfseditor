define([
    "underscore",
    "backbone",
    "handlebars",
    "text!transit/templates/stopData.handlebars"
], function (_, Backbone, Handlebars, tmpl) {
    var View;

    View = Backbone.View.extend({
        el: $('#stopData'),
        
        template: Handlebars.compile(tmpl),

        events: {
            "change select": "selectRoute"
        },

        initialize: function(){
            var self = this;
            
            this.render();
            
            this.model.on("change", self.render, self);
        },

        render: function () {
            var self = this;

            this.$el.html(this.template({
                stop: self.model.toJSON()
            }));
        }
    });

    return View;
})