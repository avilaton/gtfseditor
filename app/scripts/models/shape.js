define([
	"underscore",
	"backbone",
	'config'
], function (_, Backbone, Config) {
	var Model;

	Model = Backbone.Model.extend({
		idAttribute: "shape_id",

		urlRoot: Config.server + 'api/shape',

	    initialize: function(){

        },

        reverse: function () {
        	var features = this.get("features");
        	features[0].geometry.coordinates.reverse();
        	this.set("features", features);
        	this.trigger("change");
        }
 	});

	return Model;
})