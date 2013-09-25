define([
	"underscore",
	"backbone"
], function (_, Backbone) {
	var Model;

	Model = Backbone.Model.extend({
		// idAttribute: "stop_id",
		urlRoot: '/api/stop',
		
	    initialize: function(){
            
        }
 	});

	return Model;
})