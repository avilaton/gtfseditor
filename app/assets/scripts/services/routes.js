module.exports = function(ngModule) {
    ngModule.factory('Routes', function($resource) {
        return $resource('/api/routes', {}, {
          get: {method: 'GET', isArray: true}
        });
    });
    ngModule.factory('Route', function($resource) {
        return $resource('/api/routes/:routeId', {
          routeId: '@routeId'
        }, {});
    });
};
