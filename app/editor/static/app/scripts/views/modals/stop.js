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
            'keyup input': 'onEdit',
            'hidden.bs.modal': 'teardown'

        },

        initialize: function(options){
            var self = this;
            this.render();
        },

        render: function () {
            var self = this;

            this.$el.html(this.template(this.model.toJSON()));
        },

        save: function () {
            var self = this;
            this.model.save().then(function () {
                self.$el.modal('hide');
            });
        },

        onEdit: function (event) {
            var $target = $(event.currentTarget),
                name = $target.attr('name');

            this.model.set(name, $target.val());
        },

        teardown: function() {
          this.undelegateEvents();
        }
    });

    return View;
})