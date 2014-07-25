define([
  "jquery", 
  //"transit/config"
  ], 
function ($) {
  'use strict';

  var api = {};

  var config = {};
  config.cgiUrl = '';

  function ajax(spec) {
    var type = spec.type || 'GET';
    var route = spec.route || '';
    var params = spec.params || {};
    var success = spec.success || undefined;

    return $.ajax({
      type: type,
      contentType: 'application/json',
      dataType: 'json',
      data: params,
      url: config.cgiUrl+route,
      success: success,
      statusCode: {
        404: function () {
          console.log('transit.js error: Could not contact server.');
        },
        500: function () {
          console.log('transit.js error: A server-side error has occurred.');
        }
      },
      error: function (xhr, ajaxOptions, thrownError) {
        console.log(ajaxOptions);
        console.log(thrownError);
      }
    });
  }

  /**
   * RESTful thinking... trying to implement 4 verbs
   */
  api.get = function(spec) {
    spec = $.extend(spec, {type: 'GET'});
    return ajax(spec);
  };
  api.post = function(spec) {
    spec = $.extend(spec, {type: 'POST'});
    return ajax(spec);
  };
  api.put = function(spec) {
    spec = $.extend(spec, {type: 'PUT'});
    return ajax(spec);
  };
  api.delete = function(spec) {
    spec = $.extend(spec, {type: 'DELETE'});
    return ajax(spec);
  };





  api.getSchedule = function (route_id, success) {
    ajax({action: 'getRouteSchedule', route_id: route_id},
      success);
    return this;
  };

  api.getServices = function (route_id, success) {
    ajax({action: 'getRouteServices', route_id: route_id},
      success);
    return this;
  };

  api.sortStops = function (trip_id, success) {
    ajax({action: 'sortStops', trip_id: trip_id},
      success);
    return this;
  };

  api.offsetStops = function (trip_id, success) {
    ajax({action: 'offsetStops', trip_id: trip_id},
      success);
    return this;
  };

  api.mergeStops = function (keep, merge, success) {
    ajax({action: 'mergeStops', keep: keep, merge: merge},
      success);
    return this;
  };

  return api;

});