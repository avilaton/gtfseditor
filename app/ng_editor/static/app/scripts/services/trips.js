'use strict';

/**
 * @ngdoc factory
 * @name editorApp.TripsSrv
 * @description
 * # TripsSrv
 * Service in the editorApp.
 */
angular.module('editorApp')
  .factory('TripsSrv', function (Restangular) {

    var service = {};

    var TripsRestangular = Restangular.withConfig(function(RestangularConfigurer) {
      RestangularConfigurer.setRestangularFields({
         id: 'trip_id'
      });
    });

    var trips = TripsRestangular.all('trips');

    service.create = function(data){
      return trips.post(data);
    };

    service.get = function(id){
      return TripsRestangular.one('trips', id).get();
    };

    service.all = function(){
      return trips.getList();
    };

    service.update = function(route){
      return route.put();
    };

    service.remove = function(route){
      return route.remove();
    };

    return service;
  });
