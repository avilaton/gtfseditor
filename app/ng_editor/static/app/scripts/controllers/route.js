'use strict';

/**
 * @ngdoc function
 * @name editorApp.controller:AboutCtrl
 * @description
 * # AboutCtrl
 * Controller of the editorApp
 */
angular.module('editorApp')
  .controller('RouteCtrl', function ($log, $scope, Restangular, $state, RoutesSrv, $window) {

    var routeId = $state.params['route_id'];

    if (routeId) {
      RoutesSrv.get(routeId)
        .then(function (route) {
          $scope.route = route;
        });
    } else {
      $scope.route = {};
    }

    $scope.save = function (route) {
      if (route['route_id']) {
        $scope.route.save().then(function () {
          $state.go('routes.list');
        });
      } else {
        RoutesSrv.create(route).then(function () {
          $state.go('routes.list');
        });
      }
    };

    $scope.remove = function () {
      RoutesSrv.remove($scope.route);
    };

    $scope.cancel = function () {
      $window.history.back();
    };
  });
