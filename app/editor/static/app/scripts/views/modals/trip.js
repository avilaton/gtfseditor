define([
    'underscore',
    'backbone',
    'handlebars',
    'JST',
    'collections/calendars'
], function (_, Backbone, Handlebars, JST, CalendarsCollection) {
    var View;

    View = Backbone.View.extend({

        template: JST['modals/trip'],

        events: {
            'click .js-save': 'save',
            'keyup input': 'onEdit',
            'click input[type="checkbox"]': 'onEditCheckbox',
            'change select.select-service': 'onChangeService',
            'change select.select-direction': 'onChangeDirection',
            'hidden.bs.modal': 'teardown'
        },

        initialize: function(options){
            var self = this;
            this.calendars = new CalendarsCollection();
            this.calendars.fetch().then(function () {
                self.render();
            });
            this.render();
        },

        render: function () {
            var self = this;

            this.$el.html(this.template({
                trip: this.model.toJSON(),
                calendars: this.calendars.toJSON()
            }));
        },

        save: function () {
            var self = this;
            this.model.save().then(function () {
                self.collection.add(self.model);
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

        onChangeService: function (event) {
            var value = event.currentTarget.value;
            this.model.set('service_id', value !== '' ? value: null);
        },

        onChangeDirection: function (event) {
            var value = event.currentTarget.value;
            this.model.set('direction_id', value !== '' ? value: null);
        },

        teardown: function() {
          this.undelegateEvents();
        }
    });

    return View;
})