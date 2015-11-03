define([
  "underscore",
  "backbone",
  'config'
], function (_, Backbone, Config) {

  var Model = Backbone.Model.extend({
    idAttribute: "route_id",
    url: function() {
      if (this.isNew()) {
        return Config.server + 'api/routes/';
      } else {
        return Config.server + 'api/routes/' + this.id;
      }
    }
  });

  return Model;
})