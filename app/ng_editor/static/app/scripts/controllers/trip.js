'use strict';

/**
 * @ngdoc function
 * @name editorApp.controller:AboutCtrl
 * @description
 * # AboutCtrl
 * Controller of the editorApp
 */
angular.module('editorApp')
  .controller('TripCtrl', function ($log, $scope, $state, TripsSrv, $window) {

    var tripId = $state.params['trip_id'];

    if (tripId) {
      TripsSrv.get(tripId)
        .then(function (trip) {
          $scope.trip = trip;
        });
    } else {
      $scope.trip = {};
    }

    $scope.save = function (trip) {
      if (trip['trip_id']) {
        $scope.trip.save().then(function () {
          $state.go('trips.list');
        });
      } else {
        TripsSrv.create(trip).then(function () {
          $state.go('trips.list');
        });
      }
    };

    $scope.remove = function () {
      TripsSrv.remove($scope.trip);
    };

    $scope.cancel = function () {
      $window.history.back();
    };
  });
