define([
	"underscore",
	"backbone",
	"models/route"
], function (_, Backbone, RouteModel) {
	var RouteCollection;

	RouteCollection = Backbone.Collection.extend({
		model: RouteModel,

		url: 'api/routes/',

        parse: function (response) {
        	return response.routes;
        }
 	});

	return RouteCollection;
})