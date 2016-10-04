module.exports = function(ngModule) {
    ngModule.factory('Stats', function($resource) {
        return $resource('/api/stats');
    });
};
