define([
	'OpenLayers',
	'underscore',
	'backbone',
	'config'
], function (OpenLayers, _, Backbone, Config) {
	var Model;

	Model = Backbone.Model.extend({
		idAttribute: 'stop_id',
		urlRoot: Config.server + 'api/stops/',
		
	    initialize: function(){

	        this.format = new OpenLayers.Format.GeoJSON({
	          'internalProjection': new OpenLayers.Projection('EPSG:900913'),
	          'externalProjection': new OpenLayers.Projection('EPSG:4326')
	        });

        },

        toGeoJSON: function () {
			return {
				'type': 'Feature',
				'id': this.get('id'),
				'properties': this.toJSON(),
				'geometry': {
					'type': 'Point',
					'coordinates': [this.get('stop_lon'), this.get('stop_lat')]
				},
				'crs': {
					'type':'name',
					'properties': {
						'name':'urn:ogc:def:crs:OGC:1.3:CRS84'
					}
				}
			};
        },

        toFeature: function () {
        	return this.format.parseFeature(this.toGeoJSON());
        }

 	});

	return Model;
})