define([
    'underscore',
    'backbone',
    'config',
    'models/trip'
], function (_, Backbone, Config, TripModel) {
    var TripsCollection;

    TripsCollection = Backbone.Collection.extend({
        model: TripModel,

        route_id: '',

        url: function() {
            return Config.server + 'api/routes/' + this.route_id + '/trips';
        },

        select: function (trip_id) {
            var self = this;

            var selectedModel = _.find(self.models, function (model) {
                return model.get('trip_id') == trip_id;
            });

            this.selected = selectedModel;

            self.trigger('trip_selected', selectedModel);
        }
    });

    return TripsCollection;
})