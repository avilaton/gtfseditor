define([
  'underscore',
  'backbone',
  'JST'
  ], function (_, Backbone, JST) {

    var View = Backbone.View.extend({

      template: JST.kmlSelect,

      events: {
        'change input': 'onChange'
      },

      initialize: function(){
        this.render();
      },

      render: function () {
        this.$el.html(this.template());
      },

      onChange: function (event) {
        var files = event.target.files,
          reader = new FileReader(),
          self = this;

        reader.onload = function(e) {
          self.trigger('select', e.target.result);
        };
        reader.readAsText(files[0]);
      }
    });

    return View;
  })