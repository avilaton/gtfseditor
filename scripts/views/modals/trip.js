define([
    "underscore",
    "backbone",
    "handlebars",
    "text!templates/modals/trip.handlebars",
    'api'
], function (_, Backbone, Handlebars, tmpl, Api) {
    var View;

    View = Backbone.View.extend({
        
        template: Handlebars.compile(tmpl),

        events: {
            "click .js-save": "save",
            "keyup input": 'onEdit',
            'click input[type="checkbox"]': 'onEditCheckbox'
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
        },

        onEditCheckbox: function (event) {
            var $target = $(event.currentTarget);
            this.model.set('active', $target.prop('checked'));
        }
    });

    return View;
})