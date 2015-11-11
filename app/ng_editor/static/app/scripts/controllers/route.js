'use strict';

/**
 * @ngdoc function
 * @name editorApp.controller:AboutCtrl
 * @description
 * # AboutCtrl
 * Controller of the editorApp
 */
angular.module('editorApp')
  .controller('RouteCtrl', function ($log, $scope, Restangular, $state) {
    $scope.isEditing = false;

    Restangular.one('routes', $state.params.route_id).get()
      .then(function (route) {
        $log.log('route found', route);
        route.id = route.route_id;
        $scope.route = route;
      });

    $scope.update = function () {
      $log.log('saving...');
      $scope.route.save();
    };
  });
