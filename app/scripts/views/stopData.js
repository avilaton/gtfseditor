define([
    "underscore",
    "backbone",
    "handlebars",
    'JST'
    ], function (_, Backbone, Handlebars, JST) {
        var View;

        View = Backbone.View.extend({

            template: JST['stopData'],

            initialize: function(options){
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