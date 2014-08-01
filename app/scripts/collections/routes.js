define([
	"underscore",
	"backbone",
	"models/route"
], function (_, Backbone, RouteModel) {
	var RouteCollection;

	RouteCollection = Backbone.Collection.extend({
		model: RouteModel,

		url: 'api/routes/',

	    initialize: function(){
            this.selected = new this.model;
        },

        parse: function (response) {
        	return response.routes;
        },

        select: function (route_id) {
        	var self = this;

        	var selectedModel = _.find(self.models, function (model) {
        		return model.get("route_id") == route_id;
        	});

            // this.selected = selectedModel;
            this.selected.set(selectedModel.toJSON());
            console.log(this.selected, selectedModel.toJSON());

            self.trigger('route_selected', selectedModel);
        }
 	});

	return RouteCollection;
})