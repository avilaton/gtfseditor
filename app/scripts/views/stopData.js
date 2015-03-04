define([
    'underscore',
    'backbone',
    'handlebars',
    'JST'
    ], function (_, Backbone, Handlebars, JST) {
        var View;

        View = Backbone.View.extend({

            template: JST['stopData'],

            initialize: function(options){
                var self = this;

                this.model.on('change', this.render, this);
                this.model.on('destroy', function () {
                    this.$el.html(this.template());
                }, this);

                this.render();
            },

            render: function () {
                this.$el.html(this.template({
                    stop: this.model.toJSON()
                }));
            }

    });

return View;
})