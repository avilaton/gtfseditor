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
    url: function () {
      return Config.server + 'api/trips/' + this.trip_id + '/stops.json';
    },

    initialize: function (options) {
      this.selected = new this.model;
    },

    parse: function (response) {
      return _.map(response.rows, function (row) {
          row.stop_seq._stop = row.stop;
          return row.stop_seq;
        });
    },

    toJSON: function(){
      var json = Backbone.Collection.prototype.toJSON.call(this);
      // remove the fields that do not need to be sent back
      _.each(json, function (model) {
        delete model._stop;
      });
      return json;
    },

    toGeoJSON: function () {
      var self = this,
        obj = {
        crs: {
          type: 'name',
          properties: {
            name: 'urn:ogc:def:crs:OGC:1.3:CRS84'
          }
        },
        features:[],
        type: 'FeatureCollection'
      };

      _.each(self.models, function (model) {
        var stop = model.get('_stop');
        if (!stop) return;

        obj.features.push({
          geometry: {
            coordinates: [
              stop.stop_lon,
              stop.stop_lat
            ],
            type: 'Point'
          },
          id: stop.stop_id,
          properties: {
            stop_id: stop.stop_id
          },
          type: 'Feature'
        });
      });

      return obj;
    },

    appendStop: function (model) {
      var max = 0, lastStop,
        stop_id = model.get('stop_id');

      if (!this.isEmpty()) {
        lastStop = this.max(function(model) {
            return model.get('stop_sequence');
        });
        max = Number(lastStop.get('stop_sequence'));
      };

      this.add({
        stop_id: stop_id,
        stop_sequence: max + 1,
        trip_id: this.trip_id,
        _stop: model.toJSON()
      });
    },

    removeStop: function (stop_id) {
      var self = this;
      this.each(function(model){
        if (model.get('stop_id') === stop_id) {
          self.remove(model);
        };
      });
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
        self.fetch({reset: true});
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
        self.fetch({reset: true});
      });
      return req;
    }
  });

  return Collection;
})