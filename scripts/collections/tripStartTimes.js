define([
    "underscore",
    "backbone",
    'config',
    "models/tripStartTime"
], function (_, Backbone, Config, TripStartTimeModel) {
    var TripsCollection;

    TripsCollection = Backbone.Collection.extend({
        model: TripStartTimeModel,
        
        trip_id: '',

        url: function() {
            return Config.server + 'api/trips/' + this.trip_id + '/start-times.json';
        },

        parse: function (response) {
            return response.rows;
        }

    });

    return TripsCollection;
})