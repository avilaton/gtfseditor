define([
	"underscore",
	"backbone",
	"transit/templates"
], function (_, Backbone, templates) {
	var RouteBar;

	RouteBar = Backbone.View.extend({
		el: $("#routeBar"),

		template: templates.routes,

		events: {
			"change select": "selectRoute"
		},

	    initialize: function(){
            console.log("routeBar view initialize");
            this.render();
        },

        render: function () {
        	this.$el.html(this.template(this.model));
        	//this.$el.html(this.template(this.model.attributes));
        },

        selectRoute: function (event) {
        	console.log(event.currentTarget.value);
        }
 	});

	return RouteBar;
})