define([
  'jquery',
  'underscore',
  'backbone',
  'main',
  'views/filter'
], function($, _, Backbone, Main, FilterView){

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

    app_router.on('route:showRoute', function(route_id){
      console.log('showRoute', route_id);
    });
    app_router.on('route:stopsView', function(route_id){
      var filterView = new FilterView();
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