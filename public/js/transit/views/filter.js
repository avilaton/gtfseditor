define([
    "underscore",
    "backbone",
    "handlebars",
    "text!transit/templates/filter.handlebars"
], function (_, Backbone, Handlebars, tmpl) {
    var View;

    View = Backbone.View.extend({
        el: $("#filterBox"),
        
        template: Handlebars.compile(tmpl),

        events: {
            // "click .filter-button": "onClickFilter",
            "submit .filter-form": "onSubmitFilter"
        },

        initialize: function(){
            var self = this;
            
            this.render();
            
        },

        render: function () {
            var self = this;

            this.$el.html(this.template({
                // routes: self.collection.toJSON()
            }));
        },

        onClickFilter: function (event) {
            event.preventDefault();
            console.log(event);
        },

        onSubmitFilter: function (event) {
            event.preventDefault();
            console.log(event);
        }
    });

    return View;
})