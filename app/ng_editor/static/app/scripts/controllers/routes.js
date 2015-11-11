'use strict';

/**
 * @ngdoc function
 * @name editorApp.controller:AboutCtrl
 * @description
 * # AboutCtrl
 * Controller of the editorApp
 */
angular.module('editorApp')
  .controller('RoutesCtrl', function ($log, $scope, RoutesSrv, $state) {

    function getRoutes () {
      RoutesSrv.all().then(function (routes) {
        $scope.routes = routes;
      });
    }

    $scope.remove = function (route) {
      RoutesSrv.remove(route).then(function (argument) {
        getRoutes();
      });
    };
    window.RoutesSrv = RoutesSrv;
    getRoutes();
  });
