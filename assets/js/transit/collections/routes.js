define([
	"underscore",
	"backbone",
	"transit/models/route"
], function (_, Backbone, RouteModel) {
	var RouteCollection;

	RouteCollection = Backbone.Collection.extend({
		model: RouteModel,

	    initialize: function(){
            console.log("Welcome to this world", this);
        }
 	});

	return RouteCollection;
})