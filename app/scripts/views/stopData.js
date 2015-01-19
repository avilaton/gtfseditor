define([
    "underscore",
    "backbone",
    "handlebars",
    'JST'
    ], function (_, Backbone, Handlebars, JST) {
        var View;

        View = Backbone.View.extend({
            el: $('#stopData'),

            template: JST['stopData'],

            events: {
                "click button.save-stop": "onClickSave",
                "blur input.properties-stop-calle": "onCalleChange",
                "blur input.edit-stop-calle": "onCalleChange",
                "click button.toggleMultipleSelect": "toggleMultipleSelect",
                "click button.newStop": "newStop",
                "click button.saveStop": "saveStop"
            },

            initialize: function(options){
                var self = this;

                this.controls = options.controls;

                this.editMode = false;

                this.render();

                this.model.on("change", self.render, self);
            },

            render: function () {
                var self = this;

                this.$el.html(this.template({
                    stop: self.model.toJSON(),
                    editMode: self.editMode
                }));
            },

            saveStop: function (event) {
                var self = this;
                event.preventDefault();
                console.log("save stop clicked", event, this.model);
                var promise = this.model.save();
                promise.done(function (response) {
                    self.setEditMode(false);
                }).fail(function (err, response) {
                    console.log("saving failed", err, response)
                });
            },

            setEditMode: function (editMode) {
                this.editMode = editMode;
                this.render();
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