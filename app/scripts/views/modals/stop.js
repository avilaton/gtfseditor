define([
    'underscore',
    'backbone',
    'handlebars',
    'JST'
], function (_, Backbone, Handlebars, JST) {
    var View;

    View = Backbone.View.extend({

        template: JST['modals/stop'],

        events: {
            'click .js-save': 'save',
            'keyup input': 'onEdit'
        },

        initialize: function(options){
            var self = this;
            this.render();
        },

        render: function () {
            var self = this;

            this.$el.html(this.template(this.model.toJSON()));
        },

        save: function (event) {
            this.model.save();
        },

        onEdit: function (event) {
            var $target = $(event.currentTarget);
            this.model.set($target.attr('name'), $target.val());
        }
    });

    return View;
})