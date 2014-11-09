define([
  'jquery',
  'underscore',
  'backbone',
  'views/stops',
  'views/routes',
  'views/times',
  'views/navbarRight'
], function ($, _, Backbone, StopsView, RoutesView, TimesView, NavbarRightView){

  var AppRouter = Backbone.Router.extend({
    routes: {
      'routes(/:route_id)': 'showRoute',
      'stops(/:stop_id)': 'stopsView',
      'times(/:trip_id)': 'timesView',
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
      var routesView = new RoutesView();
    });
    app_router.on('route:stopsView', function(route_id){
      var stopsView = new StopsView();
    });
    app_router.on('route:timesView', function(trip_id){
      console.log('tripView', trip_id);
      var timesView = new TimesView();
    });
    app_router.on('route:defaultAction', function(actions){
      // We have no matching route, lets just log what the URL was
      var routesView = new RoutesView();
      console.log('No route:', actions);
    });
    Backbone.history.start();

    // Main.init();

  };
  return {
    initialize: initialize
  };
});