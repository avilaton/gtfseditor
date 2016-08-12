define([
    "underscore",
    "backbone",
    "api",
    'config',
    "models/stop"
], function (_, Backbone, api, Config, StopModel) {
    var Collection;

    Collection = Backbone.Collection.extend({
        model: StopModel,

        url: function () {
            return Config.server + 'api/trips/' + this.trip_id + '/stops.geojson';
        },
        
        initialize: function (options) {
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

        toGeoJSON: function () {
            var self = this;
            var obj = {
                crs: {
                    type: "name",
                    properties: {
                        name: "urn:ogc:def:crs:OGC:1.3:CRS84"
                    }
                },
                features:[],
                type: "FeatureCollection"
            };

            _.each(self.models, function (model) {
                obj.features.push(model.toGeoJSON());
            });
            this.geoJSON = obj;
            return JSON.stringify(this.geoJSON);
        },
        
        save: function () {
            var self = this;
            var req = api.put({
                url: self.url(),
                data: self.toGeoJSON()
            });
            return req;
        },

        appendStop: function (SelectedStop) {
            var self = this;
            var feature = SelectedStop.clone();
            this.add(feature);
            this.toGeoJSON();
            this.trigger("stop_added", self);
        },

        removeStop: function (SelectedStop) {
            var self = this;
            var feature = SelectedStop.clone();
            this.remove(feature);
            this.toGeoJSON();
            this.trigger("stop_removed", self);
        },

        sortStops: function () {
            var self = this;
            var trip_id = this.trip_id;

            var req = api.get({
                url: Config.server + 'api/trips/' + self.trip_id +'/actions/sort-stops'
            });
            req.done(function () {
                self.fetch()
            })
            return req;
        },

        updateDist: function () {
            var self = this;
            var trip_id = this.trip_id;
            console.log('this far', self.trip_id);
            var req = api.get({
                url: Config.server + 'api/trips/' + self.trip_id +'/actions/update-dist'
            });
            req.done(function () {
                self.fetch()
            })
            return req;
        }
    });

    return Collection;
})