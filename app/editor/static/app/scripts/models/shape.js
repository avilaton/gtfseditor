'use strict';

define([
  'underscore',
  'backbone',
  'config'
], function (_, Backbone, Config) {
  var Model;

  Model = Backbone.Model.extend({
    idAttribute: 'shape_id',

    url: function () {
      return Config.api + 'trips/' + this.get('trip_id') + '/shape.json';
    },

    reverse: function () {
      var coordinates = this.get('coordinates');
      coordinates.reverse();
      this.trigger('change:coordinates', this);
    },

    toGeoJSON: function () {
      return {
        'type': 'FeatureCollection',
        'features': [{
          'type': 'Feature',
          'properties': {},
          'geometry': {
            'type': 'LineString',
            'coordinates': this.get('coordinates'),
          }
        }],
        'crs': {
          'type':'name',
          'properties': {
            'name':'urn:ogc:def:crs:OGC:1.3:CRS84'
          }
        }
      };
    }
  });

  return Model;
})