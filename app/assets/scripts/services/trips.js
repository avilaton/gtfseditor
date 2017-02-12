module.exports = function(ngModule) {
    ngModule.factory('RouteTrips', function($resource) {
        return $resource('/api/route/:routeId/trips', {
            routeId: '@routeId'
        }, {
          get: {method: 'GET', isArray: true}
        });
    });
    ngModule.factory('RouteTrip', function($resource) {
        return $resource('/api/routes/:routeId/trips/:tripId', {
          routeId: '@routeId',
          tripId: '@tripId'
        }, {});
    });
    ngModule.factory('Trip', function($resource) {
        return $resource('/api/trips/:tripId', {
          tripId: '@tripId'
        }, {});
    });
    ngModule.factory('TripShape', function($resource) {
        return $resource('/api/trips/:tripId/shape.json', {
          tripId: '@tripId'
        }, {});
    });
    ngModule.factory('TripStops', function($resource) {
        return $resource('/api/trips/:tripId/stops.json', {
          tripId: '@tripId'
        }, {
          get: {method: 'GET', isArray: true}
        });
    });
    ngModule.service('TripStopsService', function ($http) {
      return {
        get: function get(tripId) {
          return $http.get('/api/trips/' + tripId + '/stops.json', {
            params: {embed: true}
          });
        },
        update: function (tripId, data) {
          return $http.put('/api/trips/' + tripId + '/stops.json', data);
        }
      };
    });
};
