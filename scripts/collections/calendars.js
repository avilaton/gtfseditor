define([
	"underscore",
	"backbone",
	'config',
	"models/calendar"
], function (_, Backbone, Config, CalendarModel) {
	var RouteCollection;

	RouteCollection = Backbone.Collection.extend({
		model: CalendarModel,

		url: Config.server + 'api/calendars/',

        parse: function (response) {
        	return response.rows;
        }
 	});

	return RouteCollection;
})