'use strict';

/**
 * @ngdoc function
 * @name editorApp.controller:AboutCtrl
 * @description
 * # AboutCtrl
 * Controller of the editorApp
 */
angular.module('editorApp')
  .controller('RoutesCtrl', function ($log, $scope, Restangular, $state) {
    var routes = Restangular.all('routes');

    routes.getList().then(function (routes) {
      $scope.routes = routes;
    });

    $log.log($state.params)
  });
