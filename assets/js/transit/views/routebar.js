define([
	"underscore",
	"backbone",
	"handlebars",
	"transit/templates",
	"text!transit/templates/routebar.handlebars"
], function (_, Backbone, Handlebars, templates, tmpl) {
	var RouteBar;

	RouteBar = Backbone.View.extend({
		el: $("#routeBar"),

		template: Handlebars.compile(tmpl),

		events: {
			"change select": "selectRoute"
		},

	    initialize: function(){
            console.log("routeBar view initialize");
            this.render();
        },

        render: function () {
        	this.$el.html(this.template(this.model));
        },

        selectRoute: function (event) {
        	console.log(event.currentTarget.value);
        }
 	});

	return RouteBar;
})