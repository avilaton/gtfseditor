'use strict';

/**
 * @ngdoc factory
 * @name editorApp.ShapesSrv
 * @description
 * # ShapesSrv
 * Service in the editorApp.
 */
angular.module('editorApp')
  .factory('ShapesSrv', function (Restangular, $http) {

    var service = {};

    var ShapesRestangular = Restangular.withConfig(function(RestangularConfigurer) {
      RestangularConfigurer.setRestangularFields({
         id: 'shape_id'
      });
    });

    var trips = ShapesRestangular.all('trips');

    service.create = function(data){
      return trips.post(data);
    };

    service.get = function(id){
      return ShapesRestangular.one('trips', id).get();
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


    service.getSample = function (trip_id) {
      return $http.get('http://localhost:5000/api/trips/' + trip_id + '/shape.json');
    };

    return service;
  });
