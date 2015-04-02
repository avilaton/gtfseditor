define([
    "underscore",
    "backbone",
    'config',
    'api',
    'models/tripStartTime',
    'moment',
    'moment-duration-format'
], function (_, Backbone, Config, api, TripStartTimeModel) {
    var TripsCollection;

    TripsCollection = Backbone.Collection.extend({
        model: TripStartTimeModel,

        trip_id: '',
        service_id: '',

        url: function() {
            return Config.server + 'api/trips/' + this.trip_id + '/calendars/' + this.service_id + '/start-times.json';
        },

        save: function () {
            var self = this;
            var req = api.put({
                url: self.url(),
                data: JSON.stringify(self.toJSON())
            });
            return req;
        },

        offsetTimes: function (spec) {
          var offset = spec.offset || 10;

          _.forEach(this.models, function (model) {
            var start_time = model.get('start_time'),
                offset_time = moment.duration(start_time).add(Number(offset), 'minutes').format('HH:mm:ss', { forceLength: true });
            model.set('start_time', offset_time);
          });
          this.trigger('change');
        },
    });

    return TripsCollection;
})