define([
    "underscore",
    "backbone",
    "transit/models/stop"
], function (_, Backbone, StopModel) {
    var Collection;

    Collection = Backbone.Collection.extend({
        model: StopModel,

        url: function () {
            return 'api/trip/' + this.trip_id + '/stops';
        },
        
        initialize: function(){

        },

        parse: function (response) {
            this.geoJSON = response;
            return response.features;
        }
    });

    return Collection;
})