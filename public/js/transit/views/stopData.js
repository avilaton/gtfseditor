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

            this.render();
            
            this.model.on("change", self.render, self);
        },

        render: function () {
            var self = this;
            // console.log("stop data view:", this);

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
            var value = $target.val();
            var properties = this.model.get("properties");
            properties.stop_calle = value;
            this.model.set("properties", properties);
            console.log("stop model after set", this.model);
        },

        editStop: function (event) {
          var $target = $(event.currentTarget);
          if (this.controls.selectStops.active) {
            $target.addClass('btn-primary');
            this.controls.selectStops.unselectAll();
            this.controls.selectStops.deactivate();
            this.controls.modifyStops.activate();
          } else {
            $target.removeClass('btn-primary');
            this.controls.modifyStops.deactivate();
            this.controls.selectStops.activate();
          }
        },
        
        newStop: function (event) {
          var $target = $(event.currentTarget);
          $target.toggleClass('btn-primary');

          // maps.controls.selectStops.deactivate();
          // maps.controls.drawStops.activate();

          // maps.controls.drawStops.deactivate();
          // maps.controls.selectStops.activate();
        }
        
    });

    return View;
})