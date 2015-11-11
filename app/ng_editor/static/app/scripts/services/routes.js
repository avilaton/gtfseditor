'use strict';

/**
 * @ngdoc factory
 * @name editorApp.RoutesSrv
 * @description
 * # RoutesSrv
 * Service in the editorApp.
 */
angular.module('editorApp')
  .factory('RoutesSrv', function (Restangular) {

    var service = {};

    var RoutesRestangular = Restangular.withConfig(function(RestangularConfigurer) {
      RestangularConfigurer.setRestangularFields({
         id: 'route_id'
      });
    });

    var routes = RoutesRestangular.all('routes');

    service.create = function(data){
      return routes.post(data);
    };

    service.get = function(id){
      return RoutesRestangular.one('routes', id).get();
    };

    service.all = function(){
      return routes.getList();
    };

    service.update = function(route){
      return route.put();
    };

    service.remove = function(route){
      return route.remove();
    };

    return service;
  });
