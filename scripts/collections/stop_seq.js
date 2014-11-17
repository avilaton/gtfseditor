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

    save: function () {
      var self = this;
      var req = api.put({
        url: self.url(),
        data: JSON.stringify({
          rows: self.toJSON()
        })
      });
      return req;
    }
  });

  return Collection;
})