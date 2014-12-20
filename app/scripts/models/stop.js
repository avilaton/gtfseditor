define([
	"OpenLayers",
	"underscore",
	"backbone",
	'config'
], function (OpenLayers, _, Backbone, Config) {
	var Model;

	Model = Backbone.Model.extend({
		idAttribute: "stop_id",
		urlRoot: Config.server + 'api/stops',
		
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