define([
  'underscore',
  'backbone',
  'JST'
  ], function (_, Backbone, JST) {
    var View;

    View = Backbone.View.extend({
      template: JST['fileUpload'],

      events: {
        'submit form.upload': 'onSubmit'
      },

      initialize: function(){
        this.$el.html(this.template());
        this.url = 'http://localhost:8000/api/trips/' + self.tripStartTimesCol.trip_id + '/start-times.csv';
      },

      onSubmit: function (event) {
        var self = this,
          $target = $(event.currentTarget); 
        event.preventDefault();
        event.stopPropagation();

        var fileInput = $target.find('.file').get(0);
        var data = new FormData();
        data.append('upload', fileInput.files[0]);
        $.ajax({
          url: self.url,
          type: "POST",
          data: data,
          processData: false,
          contentType: false
        });
      }

    });

    return View;
  })