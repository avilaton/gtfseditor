define([
	"underscore",
	"backbone",
  'config'
], function (_, Backbone, Config) {
	var Model;

	Model = Backbone.Model.extend({
		idAttribute: "trip_id",
    url: function() {
      if (this.isNew()) {
        return Config.server + 'api/trips';
      } else {
        return Config.server + 'api/trips/' + this.id;
      }
    }
 	});

	return Model;
})