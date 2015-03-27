'use strict';

define([
    'underscore',
    'backbone',
    'handlebars',
    'JST',
    'collections/agencies'
], function (_, Backbone, Handlebars, JST, AgenciesCollection) {
    var View;

    View = Backbone.View.extend({

        template: JST['modals/route'],

        events: {
            'click .js-save': 'save',
            'keyup input': 'onEdit',
            'click input[type="checkbox"]': 'onEditCheckbox',
            'change select.select-agency': 'onChangeAgency'
        },

        initialize: function(){
            var self = this;
            this.agencies = new AgenciesCollection();
            this.agencies.fetch().then(function () {
                self.render();
            });
        },

        render: function () {
            this.$el.html(this.template({
                route: this.model.toJSON(),
                agencies: this.agencies.toJSON()
            }));
        },

        save: function () {
            var self = this;
            this.model.save().then(function () {
                self.$el.modal('hide');
            });
        },

        onEdit: function (event) {
            var $target = $(event.currentTarget);
            this.model.set($target.attr('name'), $target.val());
        },

        onEditCheckbox: function (event) {
            var $target = $(event.currentTarget);
            this.model.set('active', $target.prop('checked'));
        },

        onChangeAgency: function (event) {
            var value = event.currentTarget.value;
            this.model.set('agency_id', value !== '' ? value: null);
        }
    });

    return View;
});