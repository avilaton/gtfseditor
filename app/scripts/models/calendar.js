define([
  "underscore",
  "backbone",
  'config'
], function (_, Backbone, Config) {

  var Model = Backbone.Model.extend({
    idAttribute: "service_id",
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