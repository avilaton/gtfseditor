define([
	"underscore",
	"backbone",
    'config'
], function (_, Backbone, Config) {

	var Model = Backbone.Model.extend({idAttribute:'value'});

	var Collection = Backbone.Collection.extend({
		model: Model,

		url: Config.server + 'api/kml/',

	    initialize: function(){
            this.selected = '';
        },

        parse: function (response) {
        	return response.options;
        },

        select: function (filename) {
        	this.selected = filename;

            this.trigger('select', this);
        }
 	});

	return Collection;
})