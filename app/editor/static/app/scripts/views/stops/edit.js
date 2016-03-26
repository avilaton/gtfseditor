'use strict';

define([
    'underscore',
    'backbone',
    'handlebars',
    'JST',
    'views/filter',
    'views/stops/map',
    'models/stop'
    ], function (_, Backbone, Handlebars, JST, FilterView, StopMapView, StopModel) {

        var View;

        View = Backbone.View.extend({
            el: $('.main-view'),

            template: JST['stops/edit'],

            events: {
                'keyup input': 'onEdit',
                'click .save-stop': 'save',
            },

            initialize: function(options){
                var self = this;
                this.stop_id = options.stop_id;
                this.model = new StopModel({stop_id: this.stop_id});
                if (!_.isUndefined(this.stop_id)) {
                    this.model.fetch().then(function () {
                        self.render();
                    });
                } else {
                    this.render();
                }
            },

            render: function () {
                this.$el.html(this.template({
                    stop: this.model.toJSON()
                }));

                this.mapView = new StopMapView({
                    el: '.map-view',
                    model: this.model
                });

                if (!_.isUndefined(this.stop_id)) {
                    var feature = this.model.toFeature();

                    if (feature) {
                        this.mapView.controls.copyFeature(feature, 'drawStops');
                    }
                    this.mapView.controls.selectStops.unselectAll();
                    this.mapView.controls.selectStops.deactivate();
                    this.mapView.controls.modifyStops.activate();
                    this.mapView.controls.modifyStops.selectControl.select(feature);
                } else {
                    this.mapView.controls.selectStops.unselectAll();
                    this.mapView.controls.selectStops.deactivate();
                    this.mapView.controls.drawStops.activate();
                }
            },

            onEdit: function (event) {
                var $target = $(event.currentTarget);
                this.model.set($target.attr('name'), $target.val());
            },

            save: function () {
                this.model.save().then(function() {
                    App.router.navigate('#/stops');
                });
            },

        });

    return View;

});