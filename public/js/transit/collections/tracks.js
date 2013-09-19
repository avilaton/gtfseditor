define([
    "underscore",
    "backbone",
    "transit/models/track"
], function (_, Backbone, TrackModel) {
    var Collection;

    Collection = Backbone.Collection.extend({
        model: TrackModel,
        
        initialize: function(){

        }
    });

    return Collection;
})