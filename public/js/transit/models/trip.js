define([
	"underscore",
	"backbone"
], function (_, Backbone) {
	var Model;

	Model = Backbone.Model.extend({
		idAttribute: "trip_id",

	    initialize: function(){
            
        }
 	});

	return Model;
})