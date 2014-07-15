define([
	"underscore",
	"backbone"
], function (_, Backbone) {
	var Model;

	Model = Backbone.Model.extend({
		idAttribute: "trip_id",
    url: function() {
      if (this.isNew()) {
        return 'api/trips';
      } else {
        return 'api/trips/' + this.id;
      }
    }
 	});

	return Model;
})