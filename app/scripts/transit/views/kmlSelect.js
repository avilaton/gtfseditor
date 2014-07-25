define([
  "backbone",
  "handlebars",
  "text!transit/templates/kmlSelect.handlebars"
  ], function (Backbone, Handlebars, tmpl) {

    var View = Backbone.View.extend({

      template: Handlebars.compile(tmpl),

      events: {
        "change select": "onChange"
      },

      initialize: function(options){
        var self = this;

        this.collection.on("change add remove reset", self.render, self);
        this.collection.fetch();
      },

      render: function () {
        var self = this;
        this.$el.html(this.template({
          options: self.collection.toJSON()
        }));
      },

      onChange: function (event) {
        var selectedValue = event.currentTarget.value;
        this.collection.select(selectedValue);
      }
    });

    return View;
  })