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
        "click button.drawStops": "drawStops",
        "click button.removeStop": "removeStop",
        "click button.appendStop": "appendStop",
        "click button.toggleTimepoint": "toggleTimepoint",
        "click button.saveStops": "saveStops"
      },

      initialize: function(options){
        var self = this;

        this.controls = options.controls;

        this.render();

        this.collection.on("change reset", self.render, self);
      },

      render: function () {
        var self = this;

        this.$el.html(this.template());
      },

      prevStop: function (event) {
        this.collection.skipSelect(1);
      },

      nextStop: function (event) {
        this.collection.skipSelect(-1);
      },
      
      sortStops: function (event) {
        this.collection.sortTripStops();
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
      
      drawStops: function (event) {
        var $target = $(event.currentTarget);
        $target.toggleClass('btn-primary');

        // maps.controls.selectStops.deactivate();
        // maps.controls.drawStops.activate();

        // maps.controls.drawStops.deactivate();
        // maps.controls.selectStops.activate();
      },
      
      removeStop: function (event) {
        this.collection.removeSelected();
      },
      
      appendStop: function (event) {
        this.collection.appendSelected();
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