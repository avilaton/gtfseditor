import angular from 'angular';
var lodash = require('lodash');
var NavBarComponent = require('./components/navbar')

var app = angular.module('app', [
    require('angular-resource'),
    require('angular-route'),
    require('angular-ui-bootstrap'),
    require('angular-loading-bar'),
    NavBarComponent,
    ]);

app.constant('_', lodash);

app.config(['$routeProvider', function ($routeProvider) {
    $routeProvider.when('/', {
        template: '<home></home>',
    }).when('/routes/', {
        template: '<routes></routes>',
    }).when('/routes/:routeId', {
        template: '<route></route>',
    }).when('/routes/:routeId/edit', {
        template: '<route-form></route-form>',
    }).when('/routes/:routeId/trips/:tripId', {
        template: '<trip></trip>',
    }).when('/stops/', {
        template: '<stops></stops>',
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
require('./components/routes/route-form')(app);
require('./components/route')(app);
require('./components/trip')(app);
require('./components/stop-sequence')(app);
require('./components/stops')(app);

// Register directives
require('./directives/ol-map')(app);
