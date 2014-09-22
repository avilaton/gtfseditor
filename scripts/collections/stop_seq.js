define([
    "underscore",
    "backbone",
    "api",
    "models/stop"
], function (_, Backbone, api, StopModel) {
    var Collection;

    Collection = Backbone.Collection.extend({
        model: StopModel,

        url: function () {
            return 'api/trips/' + this.trip_id + '/stops.json';
        },
        
        initialize: function (options) {
            this.selected = new this.model;
        },

        parse: function (response) {
            return _.map(response.rows, function (row) {
                return row.stop;
            });
        }
    });

    return Collection;
})