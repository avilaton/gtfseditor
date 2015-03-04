define([
    "underscore",
    "backbone",
    "handlebars",
    'JST',
    'views/modals/stop'
    ], function (_, Backbone, Handlebars, JST, StopModal) {
        var View;

        View = Backbone.View.extend({

            template: JST['stopToolbar'],

            events: {
                "click button.newStop": "newStop",
                "click button.edit-stop": "editStop",
                "click button.move-stop": "moveStop",
                "click button.removeStop": "removeStop",
                "click button.saveStop": "saveStop",
                "click button.clearEdits": "clearEdits"
            },

            initialize: function(options){
                var self = this;

                this.controls = options.controls;

                this.editMode = false;

                this.render();
            },

            render: function () {
                this.$el.html(this.template({}));
                this.saveBtn = this.$el.find('.saveStop');
                this.editBtn = this.$el.find('.editStop');
            },

            saveStop: function (event) {
                event.preventDefault();
                console.log("save stop clicked", event, this.model);
                this.model.save();
            },

            removeStop: function (event) {
                event.preventDefault();
                console.log("remove stop clicked", event, this.model);
                console.log(this.model.feature.destroy());
                this.model.destroy();
            },

            editStop: function (event) {
                var stopModal = new StopModal({
                    model: this.model,
                    el: $('#routeDataEditor')
                });
                stopModal.$el.modal('show');
            },

            moveStop: function (event) {
                event.preventDefault();
                var self = this;
                var $target = $(event.currentTarget);
                var feature = this.model.toFeature();

                if (!this.editMode) {
                    if (feature) {
                        this.controls.copyFeature(feature, 'drawStops');
                    };
                    $target.addClass('btn-primary');
                    this.controls.selectStops.unselectAll();
                    this.controls.selectStops.deactivate();
                    this.controls.modifyStops.activate();
                    this.controls.modifyStops.selectControl.select(feature);
                } else {
                    $target.removeClass('btn-primary');
                    this.controls.modifyStops.deactivate();

                    this.controls.selectStops.activate();
                    // this.controls.selectStops.select(feature);
                }
                self.editMode = !self.editMode;
            },

            newStop: function (event) {
                var $target = $(event.currentTarget);
                $target.toggleClass('btn-primary');
                if (this.controls.selectStops.active) {
                    $target.addClass('btn-primary');
                    this.controls.selectStops.unselectAll();
                    this.controls.selectStops.deactivate();
                    this.controls.drawStops.activate();
                } else {
                    $target.removeClass('btn-primary');
                    this.controls.drawStops.deactivate();
                    this.controls.selectStops.activate();
                }

            },

            clearEdits: function (event) {
                this.controls.clearEdits();
            }
    });

return View;
})