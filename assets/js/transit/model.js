define(["transit/config",
  "transit/api"], function (config, api) {
  /**
   * Currently selected objects model
   */
  'use strict';

  var model = {};

  model.unsavedChanges = False;

  model.selected = {
    route_id: null,
    trip_id: null,
    stop_id: null,
    shape_id: null
  };
  model.routes = [];
  model.trips = {};

  model.init = function () {
    return api.get({
      route: 'routes/'
    });
  };

  model.fetchRoutes = function () {
    return api.get({route: 'routes/'})
      .pipe(function(response) {return response.routes;})
      .done(function (routes) {model.routes = routes;});
  };

  model.fetchTrips = function () {
    return api.get({route: 'route/'+model.selected.route_id+'/trips'})
      .pipe(function(response) {return response.trips;})
      .done(function (trips) {model.trips = trips;});
  };

  model.getTripShape = function (trip_id) {
    model.selected.shape_id = null;
    for (var i = 0; i < model.trips.length; i++) {
      if (model.trips[i].trip_id == trip_id) {
        model.selected.shape_id = model.trips[i].shape_id
      }
    };
    return model.selected.shape_id;
  }

  return model;
});