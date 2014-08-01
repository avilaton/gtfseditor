define([
	"underscore",
	"backbone"
], function (_, Backbone) {

	var Model = Backbone.Model.extend({idAttribute:'value'});

	var Collection = Backbone.Collection.extend({
		model: Model,

		url: 'api/kml/',

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