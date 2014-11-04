define([
  'jquery',
  'underscore',
  'backbone',
  'main',
  'views/stops',
  'views/navbarRight'
], function($, _, Backbone, Main, StopsView, NavbarRightView){

  var AppRouter = Backbone.Router.extend({
    routes: {
      'routes(/:route_id)': 'showRoute',
      'stops(/:stop_id)': 'stopsView',
      'calendar(/)': 'calendarView',
      'agencies(/:agency_id)': 'agenciesView',
      '*actions': 'defaultAction'
    }
  });

  var initialize = function(){
    var app_router = new AppRouter;
    
    var navbarRight = new NavbarRightView();

    app_router.on('route:showRoute', function(route_id){
      console.log('showRoute', route_id);
    });
    app_router.on('route:stopsView', function(route_id){
      var stopsView = new StopsView();
    });
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