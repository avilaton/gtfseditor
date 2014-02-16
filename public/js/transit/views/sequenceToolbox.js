define([
  "underscore",
  "backbone",
  "handlebars",
  "text!transit/templates/sequenceToolbox.handlebars"
  ], function (_, Backbone, Handlebars, tmpl) {
    var View;

    View = Backbone.View.extend({
      el: $("#sequenceToolbox"),

      template: Handlebars.compile(tmpl),

      events: {
        "click button.prevStop": "prevStop",
        "click button.nextStop": "nextStop",
        "click button.sortStops": "sortStops",
        "click button.offsetStops": "offsetStops",
        "click button.toggleMultipleSelect": "toggleMultipleSelect",
        "click button.editStops": "editStops",
        "click button.removeStop": "removeStop",
        "click button.appendStop": "appendStop",
        "click button.toggleTimepoint": "toggleTimepoint",
        "click button.saveStops": "saveStops"
      },

      initialize: function(options){
        var self = this;

        $(document).bind('keyup', this.keypress.bind(self));

        this.controls = options.controls;
        this.selectedStop = options.stop;

        this.render();

        this.collection.on("change reset", self.render, self);
      },

      render: function () {
        var self = this;

        this.$el.html(this.template());
      },

      keypress : function (event) {
        if (event.keyCode == 82)
          this.removeStop();
      },

      prevStop: function (event) {
        var self = this;
        var selMember = this.collection.findWhere({"id": self.model.get("id")});
        if (selMember) {
          var index = this.collection.indexOf(selMember);
          var modelAbove = this.collection.at(index-1);
          if (modelAbove) {
            this.model.set(modelAbove.toJSON());
            this.collection.trigger('trip_stop_selected');
          };
        };
      },

      nextStop: function (event) {
        var self = this;
        var selMember = this.collection.findWhere({"id": self.model.get("id")});
        if (selMember) {
          var index = this.collection.indexOf(selMember);
          var modelBelow = this.collection.at(index+1);
          if (modelBelow) {
            this.model.set(modelBelow.toJSON());
            this.collection.trigger('trip_stop_selected');
          };
        };
      },
      
      sortStops: function (event) {
        this.collection.sortStops();
      },
      
      offsetStops: function (event) {
        this.collection.alignTripStops();
      },
      
      toggleMultipleSelect: function (event) {
        var $target = $(event.currentTarget);

        $target.toggleClass('btn-primary');
          
        // this.controls.selectStops.deactivate();
        // this.controls.selectMultiple.activate();
      
        // this.controls.selectMultiple.deactivate();
        // this.controls.selectStops.activate();
      },
      
      editStops: function (event) {
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

      removeStop: function (event) {
        this.collection.removeStop(this.model);
      },
      
      appendStop: function (event) {
        this.collection.appendStop(this.model);
      },
      
      toggleTimepoint: function (event) {
        this.collection.selected.toggleTimepoint();
        // api.put({
        //   route: 'trip/'+trip_id+'/stop/'+stopFeature['fid']+'/timepoint',
        //   params: {is_timepoint: is_timepoint},
        //   success: function(response) {
        //     console.log(response);
        //   }
        // });
      },
      
      saveStops: function (event) {
        this.collection.save();
      }

    });

return View;
})