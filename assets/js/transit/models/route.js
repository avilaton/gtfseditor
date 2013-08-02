define([
	"underscore",
	"backbone"
], function (_, Backbone) {
	var RouteModel;

	RouteModel = Backbone.Model.extend({
		defaults: {
			name: "some route"
		},
	    initialize: function(){
            console.log("Welcome to this world");
        }
 	});

	return RouteModel;
})