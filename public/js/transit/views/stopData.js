define([
    "underscore",
    "backbone",
    "handlebars",
    "text!transit/templates/stopData.handlebars"
    ], function (_, Backbone, Handlebars, tmpl) {
        var View;

        View = Backbone.View.extend({
            el: $('#stopData'),

            template: Handlebars.compile(tmpl),

            events: {
                "click button.save-stop": "onClickSave",
                "blur input.properties-stop-calle": "onCalleChange",
                "blur input.edit-stop-calle": "onCalleChange",
                "click button.toggleMultipleSelect": "toggleMultipleSelect",
                "click button.newStop": "newStop",
                "click button.editStop": "editStop",
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
                event.preventDefault();
                console.log("save stop clicked", event, this.model);
                this.model.save();
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