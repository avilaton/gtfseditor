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
                "click button.saveStop": "saveStop"
            },

            initialize: function(options){
                var self = this;

                this.controls = options.controls;

                this.editMode = false;

                this.render();
            },

            render: function () {
                this.$el.html(this.template({}));
            },

            saveStop: function (event) {
                event.preventDefault();
                console.log("save stop clicked", event, this.model);
                this.model.save();
            },

            editStop: function (event) {
                var self = this;
                event.preventDefault();

                var $target = $(event.currentTarget);
                var feature = this.model.feature;
                console.log(feature);
                
                if (this.controls.selectStops.active) {
                    //$target.addClass('btn-primary');
                    self.editMode = true;
                    // this.controls.selectStops.unselectAll();
                    this.controls.selectStops.deactivate();
                    this.controls.modifyStops.activate();
                    this.controls.modifyStops.selectFeature(feature);
                } else {
                    // $target.removeClass('btn-primary');
                    self.editMode = false;
                    this.controls.modifyStops.deactivate();
                    this.controls.selectStops.activate();
                }
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

            onCalleChange: function (event) {
                var $target = $(event.currentTarget);
                var value = $target.val();
                var properties = this.model.get("properties");
                properties.stop_calle = value;
                this.model.set({"properties": properties, changed: true});
                console.log("stop model after set", this.model);
            }
    });

return View;
})