define([
  'jquery',
  'underscore',
  'backbone',
  'views/stops',
  'views/routes',
  'views/calendar',
  'views/agencies',
  'views/navbarRight'
], function ($, _, Backbone, StopsView, RoutesView, CalendarView, AgenciesView,
  NavbarRightView){

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
    var app_router = new AppRouter,
      navbarRight = new NavbarRightView(),
      mainView;

    function clean () {
      if (mainView) {
        // mainView.close();
      }
    }

    app_router.on('route:showRoute', function(route_id){
      clean();
      mainView = new RoutesView();
    });
    app_router.on('route:stopsView', function(route_id){
      clean();
      mainView = new StopsView();
    });
    app_router.on('route:calendarView', function(trip_id){
      clean();
      mainView = new CalendarView();
    });
    app_router.on('route:agenciesView', function(trip_id){
      clean();
      mainView = new AgenciesView();
    });
    app_router.on('route:defaultAction', function(actions){
      clean();
      // We have no matching route, lets just log what the URL was
      mainView = new RoutesView();
    });
    Backbone.history.start();


  };
  return {
    initialize: initialize
  };
});