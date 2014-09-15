define([
	"OpenLayers",
	"underscore",
	"backbone"
], function (OpenLayers, _, Backbone) {
	var Model;

	Model = Backbone.Model.extend({
		// idAttribute: "stop_id",
		urlRoot: '/api/stops',
		
	    initialize: function(){

	        this.format = new OpenLayers.Format.GeoJSON({
	          'internalProjection': new OpenLayers.Projection("EPSG:900913"),
	          'externalProjection': new OpenLayers.Projection("EPSG:4326")
	        });

        },

        toGeoJSON: function () {
        	return this.toJSON();
        },

        toFeature: function () {
        	return this.format.parseFeature(this.toJSON());
        }

 	});

	return Model;
})