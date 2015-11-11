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
    //
    // For any unmatched url, redirect to /state1
    $urlRouterProvider.otherwise("/");
    //
    // Now set up the states
    $stateProvider
      .state('home', {
        url: "",
        templateUrl: "views/main.html",
        controller: 'MainCtrl'
      })
      .state('routes', {
        abstract: true,
        template: '<div ui-view></div>'
      })
      .state('routes.list', {
        url: "/routes",
        templateUrl: "views/routes.list.html",
        controller: 'RoutesCtrl'
      })
      .state('routes.item', {
        url: "/routes/:route_id",
        templateUrl: "views/routes.item.html",
        controller: 'RouteCtrl'
      })
      .state('agencies', {
        url: "/agencies",
        templateUrl: "views/agencies.list.html",
        controller: 'RoutesCtrl'
      })
      .state('calendars', {
        url: "/calendars",
        templateUrl: "views/calendars.list.html",
        controller: 'RoutesCtrl'
      })
      .state('stops', {
        url: "/stops",
        templateUrl: "views/stops.list.html",
        controller: 'RoutesCtrl'
      });

    RestangularProvider.setBaseUrl('http://localhost:5000/api/');
  });
