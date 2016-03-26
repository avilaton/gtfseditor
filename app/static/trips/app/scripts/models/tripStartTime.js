'use strict';

define([
  'underscore',
  'backbone'
], function (_, Backbone) {
  var Model;

  Model = Backbone.Model.extend({
    validate: function (attrs) {
      var re = /^\d{2}:\d{2}:\d{2}$/;
      if (!re.test(attrs.start_time)) {
        return 'Invalid Value';
      }
    }
  });

  return Model;
});