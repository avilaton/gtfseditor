module.exports = function(ngModule) {
    ngModule.factory('Agencies', function($resource) {
        return $resource('/api/agency', {}, {
          get: {method: 'GET', isArray: true}
        });
    });
};
