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
            "blur span.edit-stop-calle": "onCalleChange"
        },

        initialize: function(){
            var self = this;
            
            this.render();
            
            this.model.on("change", self.render, self);
        },

        render: function () {
            var self = this;
            console.log("stop data view:", this);

            this.$el.html(this.template({
                stop: self.model.toJSON()
            }));
        },

        onClickSave: function (event) {
            console.log("save stop clicked", event, this.model);
            this.model.save();
        },

        onCalleChange: function (event) {
            var $target = $(event.currentTarget);
            var value = $target.text();
            var properties = this.model.get("properties");
            properties.stop_calle = value;
            this.model.set("properties", properties);
            console.log("stop model after set", this.model);
        }
    });

    return View;
})