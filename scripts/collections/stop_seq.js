define([
  'underscore',
  'backbone',
  'api',
  'config',
  'models/stop'
], function (_, Backbone, api, Config, StopModel) {
  var Collection;

  Collection = Backbone.Collection.extend({
    model: StopModel,

    url: function () {
      return Config.server + 'api/trips/' + this.trip_id + '/stops.json';
    },
    
    initialize: function (options) {
      this.selected = new this.model;
    },

    parse: function (response) {
      return _.map(response.rows, function (row) {
          return row.stop_seq;
      });
    },

    toGeoJSON: function () {
      var self = this,
        obj = {
        crs: {
          type: "name",
          properties: {
            name: "urn:ogc:def:crs:OGC:1.3:CRS84"
          }
        },
        features:[],
        type: "FeatureCollection"
      };

      _.each(self.models, function (model) {
        obj.features.push(model.toGeoJSON());
      });

      return obj;
    },

    save: function () {
      var self = this;
      var req = api.put({
        url: self.url(),
        data: JSON.stringify({
          rows: self.toJSON()
        })
      });
      return req;
    },

    sortStops: function () {
      var self = this;
      var trip_id = this.trip_id;

      var req = api.get({
        url: Config.server + 'api/trips/' + self.trip_id +'/actions/sort-stops'
      });
      req.done(function () {
        self.fetch()
      });
      return req;
    },

    updateDist: function () {
      var self = this;
      var trip_id = this.trip_id;
      var req = api.get({
        url: Config.server + 'api/trips/' + self.trip_id +'/actions/update-dist'
      });
      req.done(function () {
        self.fetch()
      });
      return req;
    }
  });

  return Collection;
})