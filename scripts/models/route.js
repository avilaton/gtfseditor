define([
  "underscore",
  "backbone"
], function (_, Backbone) {

  var Model = Backbone.Model.extend({
    idAttribute: "route_id",
    url: function() {
      if (this.isNew()) {
        return 'api/routes';
      } else {
        return 'api/routes/' + this.id;
      }
    }
  });

  return Model;
})