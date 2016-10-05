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
};
