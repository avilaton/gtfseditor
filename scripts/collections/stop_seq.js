define([
  "underscore",
  "backbone",
  "api",
  'config',
  "models/stop"
], function (_, Backbone, api, Config, StopModel) {
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
          return row.stop_seq;
      });
    },

    save: function () {
      console.log(this)
    }
  });

  return Collection;
})