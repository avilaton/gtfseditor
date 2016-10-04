var angular = require('angular');

var app = angular.module('app', [
    require('angular-resource'),
    require('angular-route'),
    ]);


app.config(['$routeProvider', function ($routeProvider) {
    $routeProvider.when('/', {
        template: '<index></index>',
    }).when('/routes/', {
        template: '<routes></routes>',
    }).otherwise({
        redirectTo: '/'
    });
}]);
