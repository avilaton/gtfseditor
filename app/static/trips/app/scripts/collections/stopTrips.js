define([
	'underscore',
	'backbone',
	'config'
], function (_, Backbone, Config) {
	var RouteCollection;

	RouteCollection = Backbone.Collection.extend({

    initialize: function (options) {
      this.stop_id = options.stop_id;
    },

		url: function () {
      return Config.server + 'api/stops/' + this.stop_id + '/seqs.json';
    }

 	});

	return RouteCollection;
})