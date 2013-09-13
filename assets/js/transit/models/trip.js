define([
	"underscore",
	"backbone"
], function (_, Backbone) {
	var TripModel;

	TripModel = Backbone.Model.extend({
		idAttribute: "trip_id",

	    initialize: function(){
            
        }
 	});

	return TripModel;
})