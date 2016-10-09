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
    }).when('/routes/:routeId', {
        template: '<route></route>',
    }).when('/routes/:routeId/trips/:tripId', {
        template: '<trip></trip>',
    }).otherwise({
        redirectTo: '/'
    });
}]);

// Register services
require('./services/stats')(app);
require('./services/routes')(app);
require('./services/agencies')(app);
require('./services/trips')(app);

// Register components
require('./components/home')(app);
require('./components/routes')(app);
require('./components/route')(app);
require('./components/trip')(app);
