'use strict';

/**
 * @ngdoc function
 * @name editorApp.controller:AboutCtrl
 * @description
 * # AboutCtrl
 * Controller of the editorApp
 */
angular.module('editorApp')
  .controller('TripCtrl', function ($log, $scope, $state, TripsSrv, ShapesSrv, $window) {

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


    var flickrSource = new ol.source.Vector();

    function flickrStyle(feature) {
      console.log(feature)
      var style = new ol.style.Style({
        image: new ol.style.Circle({
          radius: 6,
          stroke: new ol.style.Stroke({
            color: 'white',
            width: 2
          }),
          fill: new ol.style.Fill({
            color: 'green'
          })
        }),
        stroke: new ol.style.Stroke({
          color: [0, 0, 255, 0.6],
          width: 8,
          lineCap: 'round'
        })
      });
      return [style];
    }

    var flickrLayer = new ol.layer.Vector({
      source: flickrSource,
      style: flickrStyle
    });

    new ol.Map({
      layers: [
        new ol.layer.Tile({source: new ol.source.OSM()}),
        flickrLayer
      ],
      view: new ol.View({
        center: [0, 0],
        zoom: 2
      }),
      target: 'map'
    });

    function successHandler(shape) {
      // we need to transform the geometries into the view's projection
      var transform = ol.proj.getTransform('EPSG:4326', 'EPSG:3857');
      // loop over the items in the response
      var feature = new ol.Feature();
      var lineString = new ol.geom.LineString();
      shape.coordinates.forEach(function(item) {
        // create a new feature with the item as the properties
        // add a url property for later ease of access
        // feature.set('url', item.media.m);
        // create an appropriate geometry and add it to the feature
        var coordinate = transform([parseFloat(item[0]), parseFloat(item[1])]);

        // add the feature to the source
        lineString.appendCoordinate(coordinate);
      });
      feature.setGeometry(lineString);
      flickrSource.addFeature(feature);
    }

    ShapesSrv.getSample(tripId).then(function (response) {
      successHandler(response.data);
    });

  });
