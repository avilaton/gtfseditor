define([
  'jquery',
  'underscore',
  'backbone',
  'views/stops',
  'views/routes',
  'views/routeTrip',
  'views/calendar',
  'views/agencies',
  'views/home',
  'views/routesList',
  'views/tripsList',
  'views/navbarRight'
], function ($, _, Backbone, StopsView, RoutesView, RouteTripView, CalendarView,
  AgenciesView, HomeView, RoutesListView, TripsListView, NavbarRightView){

  var AppRouter = Backbone.Router.extend({
    routes: {
      '': 'Home',
      'routes': 'Routes',
      'routes/:route_id': 'Route',
      'routes/:route_id/trips': 'Trips',
      'routes/:route_id/trips/:trip_id': 'Trip',
      'stops(/:stop_id)': 'Stops',
      'calendar(/)': 'Calendars',
      'agencies(/)': 'Agencies',
      '*actions': 'defaultAction'
    }
  });

  var initialize = function(){
    var app_router = new AppRouter,
      navbarRight = new NavbarRightView(),
      mainView;

    function clean () {
      if (mainView) {
        // mainView.close();
      }
    }

    app_router.on('route:Home', function(route_id){
      clean();
      mainView = new HomeView();
    });
    app_router.on('route:Routes', function(){
      clean();
      mainView = new RoutesListView();
    });
    app_router.on('route:Trip', function(route_id, trip_id){
      clean();
      mainView = new RouteTripView({route_id: route_id, trip_id: trip_id});
    });
    app_router.on('route:Trips', function(route_id){
      clean();
      mainView = new TripsListView({route_id: route_id});
    });
    app_router.on('route:Stops', function(route_id){
      clean();
      mainView = new StopsView();
    });
    app_router.on('route:Calendars', function(trip_id){
      clean();
      mainView = new CalendarView();
    });
    app_router.on('route:Agencies', function(trip_id){
      clean();
      mainView = new AgenciesView();
    });
    app_router.on('route:defaultAction', function(actions){
      clean();
      mainView = new RoutesView();
    });
    Backbone.history.start();


  };
  return {
    initialize: initialize
  };
});