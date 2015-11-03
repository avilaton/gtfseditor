define([
	'OpenLayers',
	'underscore',
	'backbone',
	'config'
], function (OpenLayers, _, Backbone, Config) {
	var Model;

	Model = Backbone.Model.extend({
		idAttribute: 'stop_id',
 	});

	return Model;
})