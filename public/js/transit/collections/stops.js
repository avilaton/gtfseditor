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
            this.selected = new this.model;
        },

        parse: function (response) {
            this.geoJSON = response;
            return response.features;
        },

        select: function (stop_id) {
            var self = this;

            if (this.selected.get("id") == stop_id) {
                console.log("already selected, do nothing");
                return;
            } else {
                self.selected = _.find(self.models, function (model) {
                    return model.get("id") == stop_id;
                });

                self.trigger('trip_stop_selected', self.selected);
            }
        },

        skipSelect: function (steps) {
            var self = this
            var currentStopSeq = this.selected.get("properties").stop_seq;
            var searchStopSeq = currentStopSeq + steps;
            
            var newSelectedModel = _.find(self.models, function (model) {
                return model.get("properties").stop_seq == searchStopSeq;
            });

            this.select(newSelectedModel.get("id"));
        },

        save: function () {
            throw "not implemented";
        }
    });

    return Collection;
})