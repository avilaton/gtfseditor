define([
    "underscore",
    "backbone",
    'config',
    'api',
    'models/tripStartTime'
], function (_, Backbone, Config, api, TripStartTimeModel) {
    var TripsCollection;

    TripsCollection = Backbone.Collection.extend({
        model: TripStartTimeModel,
        
        trip_id: '',

        url: function() {
            return Config.server + 'api/trips/' + this.trip_id + '/start-times.json';
        },

        parse: function (response) {
            return response.rows;
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
    });

    return TripsCollection;
})