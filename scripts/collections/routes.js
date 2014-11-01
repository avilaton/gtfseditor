define([
	"underscore",
	"backbone",
	'config',
	"models/route"
], function (_, Backbone, Config, RouteModel) {
	var RouteCollection;

	console.log(Config);

	RouteCollection = Backbone.Collection.extend({
		model: RouteModel,

		url: Config.server + 'api/routes/',

        parse: function (response) {
        	return response.routes;
        }
 	});

	return RouteCollection;
})