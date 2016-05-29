define([
  'underscore',
  'backbone',
  'config'
], function (_, Backbone, Config) {

  var Model = Backbone.Model.extend({
    idAttribute: 'agency_id',

    url: function() {
      if (this.isNew()) {
        return Config.api + 'agency/';
      } else {
        return Config.api + 'agency/' + this.id;
      }
    }
  });

  return Model;
})