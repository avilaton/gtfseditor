define([
  'jquery',
  'underscore',
  'backbone',
  'main'
], function($, _, Backbone, Main){

  var AppRouter = Backbone.Router.extend({
    routes: {
      // Define some URL routes
      'route/:route_id': 'showRoute',

      // Default
      '*actions': 'defaultAction'
    }
  });

  var initialize = function(){
    var app_router = new AppRouter;

    app_router.on('route:showRoute', function(route_id){

      console.log('showRoute', route_id);
    });
    app_router.on('route:defaultAction', function(actions){
      // We have no matching route, lets just log what the URL was
      console.log('No route:', actions);
    });
    Backbone.history.start();

    // Main.init();
  };
  return {
    initialize: initialize
  };
});