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
    var url = spec.url || '';
    var data = spec.data || {};
    var success = spec.success || undefined;

    return $.ajax({
      type: type,
      contentType: 'application/json',
      dataType: 'json',
      data: data,
      url: config.cgiUrl+url,
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

  return api;

});