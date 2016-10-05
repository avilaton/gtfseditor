var angular = require('angular');
var lodash = require('lodash');

var app = angular.module('app', [
    require('angular-resource'),
    require('angular-route'),
    require('angular-ui-bootstrap'),
    require('angular-loading-bar')
    ]);

app.constant('_', lodash);

app.config(['$routeProvider', function ($routeProvider) {
    $routeProvider.when('/', {
        template: '<home></home>',
    }).when('/routes/', {
        template: '<routes></routes>',
    }).otherwise({
        redirectTo: '/'
    });
}]);

// Register services
require('./services/stats')(app);
require('./services/routes')(app);
require('./services/agencies')(app);

// Register components
require('./components/home')(app);
require('./components/routes')(app);
