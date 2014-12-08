define([
  'underscore',
  'backbone',
  'moment',
  'api',
  'config',
  'models/stop'
], function (_, Backbone, moment, api, Config, StopModel) {
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

    toJSONwithSpeed: function () {
      var json = Backbone.Collection.prototype.toJSON.call(this),
        timeI = 0, timeF, posI, posF;

      _.forEach(json, function (item) {

        if (item.stop_time) {
          timeF = moment.duration(item.stop_time, 'HH:mm:ss').asHours();
          if (timeF === 0) {
            posI = item.shape_dist_traveled;
            return;
          }

          item.speed = ((item.shape_dist_traveled-posI)/(timeF-timeI)).toFixed(5);
          timeI = timeF;
          posI = item.shape_dist_traveled;
        }

      });
      return json;
    },

    setTimes: function (spec) {
      var speed = spec.speed || 20.0,
        posI = _.first(this.models).get('shape_dist_traveled');

      _.forEach(this.models, function (model) {
        var distance = model.get('shape_dist_traveled') - posI;
        var time = parseFloat(distance/speed);
        var fulltime = moment().startOf('day').add(time, 'hours').format('HH:mm:ss.ms');
        var duration = moment().startOf('day').add(time, 'hours').format('HH:mm:ss');
        model.set('stop_time', duration, {silent: true});
      });
      this.trigger('change');
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