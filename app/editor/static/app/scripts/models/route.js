define([
  "underscore",
  "backbone",
  'config'
], function (_, Backbone, Config) {

  var Model = Backbone.Model.extend({
    idAttribute: "route_id",
    url: function() {
      if (this.isNew()) {
        return Config.api + 'routes/';
      } else {
        return Config.api + 'routes/' + this.id;
      }
    }
  });

  return Model;
})