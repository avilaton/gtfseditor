define([
    "underscore",
    "backbone",
    "handlebars",
    "text!transit/templates/stopToolbar.handlebars"
    ], function (_, Backbone, Handlebars, tmpl) {
        var View;

        View = Backbone.View.extend({
            el: $('#stopToolbar'),

            template: Handlebars.compile(tmpl),

            events: {
                "click button.newStop": "newStop",
                "click button.editStop": "editStop",
                "click button.removeStop": "removeStop",
                "click button.saveStop": "saveStop"
            },

            initialize: function(options){
                var self = this;

                this.controls = options.controls;

                this.stopDataView = options.stopDataView;

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
                this.model.destroy();
            },

            editStop: function (event) {
                var self = this;
                var $target = $(event.currentTarget);
                var feature = this.model.feature;
                event.preventDefault();
                
                if (this.controls.selectStops.active) {
                    $target.addClass('btn-primary');
                    this.stopDataView.setEditMode(true);
                    // this.controls.selectStops.unselectAll();
                    this.controls.selectStops.deactivate();
                    this.controls.modifyStops.activate();
                    this.controls.modifyStops.selectFeature(feature);
                } else {
                    $target.removeClass('btn-primary');
                    this.stopDataView.setEditMode(false);
                    this.controls.modifyStops.deactivate();
                    this.controls.selectStops.activate();
                    this.controls.selectStops.select(feature);
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

            }
    });

return View;
})