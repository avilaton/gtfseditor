define(["jquery", "transit/config"], function ($, config) {
	'use strict';

    var api = {};

    function ajax(spec) {
        var type = spec.type || 'GET';
        var route = spec.route || '';
        var params = spec.params || {};
        var successHandler = spec.successHandler || undefined;
        
        $.extend(params, {'database': config.database});
        $.ajax({
            type: type,
            dataType: 'json',
            data: params,
            url: config.cgiUrl+route,
            success: successHandler,
            statusCode: {
                404: function () {
                    //~ $("#response").html('Could not contact server.');
                    console.log('transit.js error: Could not contact server.');
                },
                500: function () {
                    //~ $("#response").html('A server-side error has occurred.');
                    console.log('transit.js error: A server-side error has occurred.');
                }
            },
            error: function (xhr, ajaxOptions, thrownError) {
                console.log(ajaxOptions);
                console.log(thrownError);
            }
        });
    }

    api.getRoutes = function (successHandler) {
        ajax({type: 'GET', route:'routes', successHandler: successHandler});
        return this;
    };

    api.getTrips = function (route_id, successHandler) {
        ajax({type: 'GET', route:'route/'+route_id+'/trips', successHandler: successHandler});
        return this;
    };

    api.getTracks = function (successHandler) {
        ajax({action: 'getTracks'}, successHandler);
        return this;
    };


    api.getTripStops = function (trip_id, successHandler) {
        ajax({action: 'getTripStops', trip_id: trip_id},
            successHandler);
        return this;
    };

    api.getSchedule = function (route_id, successHandler) {
        ajax({action: 'getRouteSchedule', route_id: route_id},
            successHandler);
        return this;
    };

    api.getServices = function (route_id, successHandler) {
        ajax({action: 'getRouteServices', route_id: route_id},
            successHandler);
        return this;
    };

    api.sortStops = function (trip_id, successHandler) {
        ajax({action: 'sortStops', trip_id: trip_id},
            successHandler);
        return this;
    };

    api.offsetStops = function (trip_id, successHandler) {
        ajax({action: 'offsetStops', trip_id: trip_id},
            successHandler);
        return this;
    };

    api.revShape = function (trip_id, successHandler) {
        ajax({action: 'revShape', trip_id: trip_id},
            successHandler);
        return this;
    };

    api.saveStops = function (trip_id, stops, successHandler) {
        ajax({action: 'saveStops', trip_id: trip_id, stops: stops},
            successHandler);
        return this;
    };

    api.saveShape = function (shape, successHandler) {
        ajax({action: 'saveShape', shape: shape},
            successHandler);
        return this;
    };

    api.toggleTimepoint = function (spec, successHandler) {
        ajax({action: 'toggleTimepoint',
            trip_id: spec.trip_id,
            stop_id: spec.stop_id
            },
            successHandler);
        return this;
    };

    api.mergeStops = function (keep, merge, successHandler) {
        ajax({action: 'mergeStops', keep: keep, merge: merge},
            successHandler);
        return this;
    };

    api.findStop = function (stop_id, successHandler) {
        ajax({action: 'findStop', stop_id: stop_id},
            successHandler);
        return this;
    };

    return api;

});