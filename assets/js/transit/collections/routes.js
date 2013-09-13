define([
	"underscore",
	"backbone",
	"transit/models/route"
], function (_, Backbone, RouteModel) {
	var RouteCollection;

	RouteCollection = Backbone.Collection.extend({
		model: RouteModel,

		url: 'api/routes/',

	    initialize: function(){

        },

        parse: function (response) {
        	return response.routes;
        },

        select: function (route_id) {
        	var self = this;

        	var selectedModel = _.find(self.models, function (model) {
        		return model.get("route_id") == route_id;
        	});

        	this.selected = selectedModel;
        }
 	});

	return RouteCollection;
})