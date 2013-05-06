define(['transit/config'], function(config){
	/**
	 * Currently selected objects model
	 */
	'use strict';

	var model = {};

	model.route_id = '';
	model.trip_id = '';

	model.stops = [];

	model.shape = '';

	return model
});