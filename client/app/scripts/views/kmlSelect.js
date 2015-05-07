define([
  "backbone",
  "handlebars",
  'collections/kml',
  "text!templates/kmlSelect.handlebars"
  ], function (Backbone, Handlebars, KmlCollection, tmpl) {

    var View = Backbone.View.extend({

      template: Handlebars.compile(tmpl),

      events: {
        "change select": "onChange"
      },

      initialize: function(options){
        var self = this;
        this.collection = new KmlCollection();
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
        var value = event.currentTarget.value;
        this.collection.select(value);
        this.trigger('select', value);
      }
    });

    return View;
  })