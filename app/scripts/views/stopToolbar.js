define([
    'underscore',
    'backbone',
    'handlebars',
    'JST',
    'views/modals/stop'
    ], function (_, Backbone, Handlebars, JST, StopModal) {
        var View;

        View = Backbone.View.extend({

            template: JST['stopToolbar'],

            events: {
                'click button.create-stop': 'newStop',
                'click button.edit-stop': 'editStop',
                'click button.move-stop': 'moveStop',
                'click button.rm-stop': 'removeStop',
                'click button.save-stop': 'saveStop',
                'click button.clear-edit': 'clearEdits',
                'click button.cancel-edit': 'cancel'
            },

            initialize: function(options){
                this.controls = options.controls;
                this.render();
            },

            render: function () {
                this.$el.html(this.template({}));

                this.stopModal = new StopModal({
                    model: this.model,
                    el: $('#routeDataEditor')
                });
            },

            disable: function () {
                this.$('.btn').attr('disabled', 'disabled');
            },

            enable: function () {
                this.$('.btn').removeAttr('disabled');
            },

            cancel: function (event) {
                this.editMode(false);
                this.controls.modifyStops.deactivate();
                this.controls.drawStops.deactivate();
                this.controls.selectStops.activate();
                this.controls.clearEdits();
            },

            editMode: function (flag) {
                this.$('.toolbar-edit').toggleClass('hidden', flag);
                this.$('.toolbar-commit').toggleClass('hidden', !flag);
            },

            saveStop: function (event) {
                event.preventDefault();
                this.disable();
                var self = this;
                this.model.save().always(function () {
                    self.editMode(false);
                    self.controls.modifyStops.deactivate();
                    self.controls.drawStops.deactivate();
                    self.controls.selectStops.activate();
                    self.controls.clearEdits();
                    self.enable();
                });
            },

            removeStop: function (event) {
                event.preventDefault();
                // console.log(this.model.feature.destroy());
                this.model.destroy();
            },

            editStop: function (event) {
                var self = this;
                this.stopModal.render();
                this.stopModal.$el.modal('show');
                this.stopModal.$el.on('hide.bs.modal', function () {
                    self.editMode(false);
                    self.controls.modifyStops.deactivate();
                    self.controls.drawStops.deactivate();
                    self.controls.selectStops.activate();
                    self.controls.clearEdits();
                });
            },

            moveStop: function (event) {
                event.preventDefault();
                var self = this,
                    $target = $(event.currentTarget),
                    feature = this.model.toFeature();

                if (feature) {
                    this.controls.copyFeature(feature, 'drawStops');
                };
                this.editMode(true);
                this.controls.selectStops.unselectAll();
                this.controls.selectStops.deactivate();
                this.controls.modifyStops.activate();
                this.controls.modifyStops.selectControl.select(feature);
            },

            newStop: function (event) {
                this.editMode(true);
                this.controls.selectStops.unselectAll();
                this.controls.selectStops.deactivate();
                this.controls.drawStops.activate();
            },

            clearEdits: function (event) {
                this.controls.clearEdits();
            }
    });

return View;
})