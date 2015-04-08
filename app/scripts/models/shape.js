define([
  'underscore',
  'backbone',
  'config'
], function (_, Backbone, Config) {
  var Model;

  Model = Backbone.Model.extend({
    idAttribute: 'shape_id',

    url: function () {
      if (this.isNew()) {
        return Config.server + 'api/shapes/';
      } else {
        return Config.server + 'api/shapes/' + this.shape_id + '.json';
      }
    },

    reverse: function () {
      var coordinates = this.get('coordinates');
      coordinates.reverse();
      this.set('coordinates', coordinates);
      this.trigger('change');
    },

    toGeoJSON: function () {
      return {
        'type': 'FeatureCollection',
        'features': [{
          'type': 'Feature',
          'id': this.get('shape_id'),
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