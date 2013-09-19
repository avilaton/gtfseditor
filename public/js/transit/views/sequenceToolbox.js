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
        "click button.sortStops": "nextStop",
        "click button.offsetStops": "offsetStops",
        "click button.toggleMultipleSelect": "toggleMultipleSelect",
        "click button.editStops": "editStops",
        "click button.drawStops": "drawStops",
        "click button.removeStop": "removeStop",
        "click button.appendStop": "appendStop",
        "click button.toggleTimepoint": "toggleTimepoint",
        "click button.saveStops": "saveStops",
        "click button.saveStops": "saveStops"
      },

      initialize: function(options){
        var self = this;

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
        console.log(event);
        $('#sortStops').click(function (e){
          e.preventDefault();
          model.sortTripStops().done(maps.update());
        });
      },
      
      offsetStops: function (event) {
        console.log(event);
        $('#offsetStops').click(function (e){
          e.preventDefault();
          model.alignTripStops().done(maps.update());
        });
      },
      
      toggleMultipleSelect: function (event) {
        console.log(event);
        $('#multipleSelect').toggle(
          function () {
            $(this).addClass('btn-primary');
            maps.controls.selectStops.deactivate();
            maps.controls.selectMultiple.activate();
          },
          function () {
            $(this).removeClass('btn-primary');
            maps.controls.selectMultiple.deactivate();
            maps.controls.selectStops.activate();
          }
          );
      },
      
      editStops: function (event) {
        console.log(event);
        $('#editStops').toggle(
          function () {
            $(this).addClass('btn-primary');
            maps.controls.selectStops.deactivate();
            maps.controls.modifyStops.activate();
          }, 
          function () {
            $(this).removeClass('btn-primary');
            maps.controls.modifyStops.deactivate();
            maps.controls.selectStops.activate();
          }
          );
      },
      
      drawStops: function (event) {
        console.log(event);
        $('#drawStops').toggle(
          function () {
            $(this).addClass('btn-primary');
            maps.controls.selectStops.deactivate();
            maps.controls.drawStops.activate();
          },
          function () {
            $(this).removeClass('btn-primary');
            maps.controls.drawStops.deactivate();
            maps.controls.selectStops.activate();
          }
          );
      },
      
      removeStop: function (event) {
        console.log(event);
        $('#removeStop').click(function (e) {
          e.preventDefault();
          maps.destroySelected();
        });
      },
      
      appendStop: function (event) {
        console.log(event);
        $('#appendStop').click(function (e){
          e.preventDefault();
          maps.appendSelected();
        });
      },
      
      toggleTimepoint: function (event) {
        console.log(event);
        $('#toggleTimepoint').click(function (e) {
          e.preventDefault();
          var trip_id = model.selected.trip_id,
          stopFeature = maps.getSelectedStop(),
          is_timepoint = stopFeature.data['is_timepoint'] ? 0 : 1;

          api.put({
            route: 'trip/'+trip_id+'/stop/'+stopFeature['fid']+'/timepoint',
            params: {is_timepoint: is_timepoint},
            success: function(response) {
              console.log(response);
            }
          }).done(maps.update());
        });
      },
      
      saveStops: function (event) {
        console.log(event);
        $('#saveStops').click(function (e){
          e.preventDefault();
          saveStops()
        });
      },
      
      saveStops: function (event) {
        console.log(event);
      }
    });

return View;
})