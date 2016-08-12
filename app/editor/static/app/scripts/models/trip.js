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
        return Config.api + 'trips/';
      } else {
        return Config.api + 'trips/' + this.id;
      }
    }
 	});

	return Model;
})