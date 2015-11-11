'use strict';

/**
 * @ngdoc function
 * @name editorApp.controller:AboutCtrl
 * @description
 * # AboutCtrl
 * Controller of the editorApp
 */
angular.module('editorApp')
  .controller('TripsCtrl', function ($log, $scope, RoutesSrv, $state) {

    RoutesSrv.get($state.params['route_id']).then(function (route) {
      $scope.route = route;
    });

    function getTrips () {
      RoutesSrv.getTrips($state.params['route_id']).then(function (trips) {
        $scope.trips = trips;
      });
    }

    $scope.remove = function (route) {
      RoutesSrv.remove(route).then(function (argument) {
        getTrips();
      });
    };

    getTrips();
  });
