'use strict';

/**
 * @ngdoc overview
 * @name editorApp
 * @description
 * # editorApp
 *
 * Main module of the application.
 */
angular
  .module('editorApp', [
    'ngAnimate',
    'ngCookies',
    'ngMessages',
    'ngResource',
    'ngRoute',
    'ngSanitize',
    'ngTouch',
    'restangular',
    'ui.router',
    'ui.bootstrap'
  ])
  .config(function ($stateProvider, $urlRouterProvider, RestangularProvider) {

    $urlRouterProvider.otherwise('/');


    $stateProvider
      .state('home', {
        url: '/',
        templateUrl: 'views/main.html',
        controller: 'MainCtrl'
      });


    $stateProvider
      .state('routes', {
        url: '/routes',
        abstract: true,
        template: '<div ui-view></div>'
      })
      .state('routes.list', {
        url: '',
        templateUrl: 'views/routes/list.html',
        controller: 'RoutesCtrl'
      })
      .state('routes.create', {
        url: '/create',
        templateUrl: 'views/routes/edit.html',
        controller: 'RouteCtrl'
      })
      .state('routes.item', {
        url: '/:route_id',
        abstract: true,
        template: '<div ui-view></div>'
      })
      .state('routes.item.view', {
        url: '/view',
        templateUrl: 'views/routes/item.html',
        controller: 'RouteCtrl'
      })
      .state('routes.item.edit', {
        url: '/edit',
        templateUrl: 'views/routes/edit.html',
        controller: 'RouteCtrl'
      });


    $stateProvider
      .state('trips', {
        url: '/trips',
        parent: 'routes.item',
        abstract: true,
        template: '<div ui-view></div>'
      })
      .state('trips.list', {
        url: '',
        templateUrl: 'views/trips/list.html',
        controller: 'TripsCtrl'
      })
      .state('trips.create', {
        url: '/create',
        templateUrl: 'views/trips/edit.html',
        controller: 'RouteCtrl'
      })
      .state('trips.view', {
        url: '/:trip_id/view',
        templateUrl: 'views/trips/item.html',
        controller: 'RouteCtrl'
      })
      .state('trips.edit', {
        url: '/:trip_id/edit',
        templateUrl: 'views/trips/edit.html',
        controller: 'RouteCtrl'
      });


    $stateProvider
      .state('agencies', {
        url: '/agencies',
        templateUrl: 'views/agencies.list.html',
        controller: 'RoutesCtrl'
      });


    $stateProvider
      .state('calendars', {
        url: '/calendars',
        templateUrl: 'views/calendars.list.html',
        controller: 'RoutesCtrl'
      });


    $stateProvider
      .state('stops', {
        url: '/stops',
        templateUrl: 'views/stops.list.html',
        controller: 'RoutesCtrl'
      });


    RestangularProvider.setBaseUrl('http://localhost:5000/api/');
  });
