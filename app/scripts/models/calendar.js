define([
  'underscore',
  'backbone',
  'config'
], function (_, Backbone, Config) {

  var Model = Backbone.Model.extend({
    idAttribute: 'service_id',

    defaults: {
      monday: '0',
      tuesday: '0',
      wednesday: '0',
      thursday: '0',
      friday: '0',
      saturday: '0',
      sunday: '0'
    },

    url: function() {
      if (this.isNew()) {
        return Config.server + 'api/calendars';
      } else {
        return Config.server + 'api/calendars/' + this.id;
      }
    }
  });

  return Model;
})