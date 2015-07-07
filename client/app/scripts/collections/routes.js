define([
	'underscore',
	'backbone',
	'config',
	'models/route'
], function (_, Backbone, Config, RouteModel) {
	var RouteCollection;

	RouteCollection = Backbone.Collection.extend({
		model: RouteModel,

		url: Config.server + 'api/routes/',

 	});

	return RouteCollection;
})