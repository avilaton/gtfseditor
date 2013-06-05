define([
  "transit/config",
  "transit/api"], function (config, api) {
  /**
   * Currently selected objects model
   */
  'use strict';

  var model = {};

  model.unsavedChanges = false;

  model.selected = {
    route_id: null,
    trip_id: null,
    stop_id: null,
    shape_id: null
  };
  model.routes = [];
  model.trips = {};
  model.stop = {};

  model.init = function () {
    return api.get({
      route: 'routes/'
    });
  };

  model.select = function (features) {
    var selectedFeatures = JSON.parse(features).features;
    if (selectedFeatures.length == 1){
      model.stop = selectedFeatures[0];
    }  
  };

  model.updateStop = function () {
    return api.put({
        route: 'stop/'+model.stop.id, 
        params: JSON.stringify(model.stop)})
      .done(function (response){console.log(response)});
  }

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

  model.fetchStops = function() {
    return api.get({route: 'trip/'+model.selected.trip_id+'/stops'})
      .done(function (stops) {model.stops = stops;});
  };

  model.fetchShape = function() {
    return api.get({route: 'shape/'+model.selected.shape_id})
      .done(function (data) {model.shape = data;});
  };

  model.saveStops = function (stops) {
    return api.put({
        route: 'trip/'+model.selected.trip_id+'/stops',
        params: stops
      });
  };

  model.saveShape = function (shape) {
    return api.put({
        route: 'shape/'+model.selected.shape_id,
        params: shape
      });
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

  model.sortTripStops = function () {
    return api.put({
        route: 'trip/'+model.selected.trip_id+'/stops'+'?q=sort'
      });
  }

  model.alignTripStops = function () {
    return api.put({
        route: 'trip/'+model.selected.trip_id+'/stops'+'?q=align'
      });
  }

  model.mergeStops = function () {
    return
  };

  return model;
});