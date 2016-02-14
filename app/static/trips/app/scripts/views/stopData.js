define([
    'underscore',
    'backbone',
    'JST',
    'collections/stopTrips'
    ], function (_, Backbone, JST, StopTripsCollection) {
        var View;

        View = Backbone.View.extend({

            template: JST['stopData'],

            events: {
                'click button.show-trips': 'showTrips'
            },

            initialize: function(options){
                var self = this;

                this.model.on('change', this.render, this);
                this.model.on('destroy', function () {
                    delete this.trips;
                    this.$el.html(this.template());
                }, this);

                this.render();
            },

            render: function () {
                this.$el.html(this.template({
                    stop: this.model.toJSON(),
                    trips: this.trips
                }));
            },

            showTrips: function () {
                var self = this;
                this.tripsCol = new StopTripsCollection({
                    stop_id: this.model.get('stop_id')
                });
                this.tripsCol.fetch().then(function () {
                    self.$el.html(self.template({
                        stop: self.model.toJSON(),
                        trips: self.tripsCol.toJSON()
                    }));
                });
            }

    });

return View;
})