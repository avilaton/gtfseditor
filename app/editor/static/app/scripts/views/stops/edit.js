'use strict';

define([
    'underscore',
    'backbone',
    'handlebars',
    'JST',
    'views/stopData',
    'views/filter',
    'views/stopMap',
    'views/stopToolbar',
    'models/stop'
    ], function (_, Backbone, Handlebars, JST, StopDataView, FilterView, StopMapView,
                 StopToolbarView, StopModel) {

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
                this.model = new StopModel({stop_id: options.stop_id});
                this.model.fetch().then(function () {
                    self.render();
                });

                this.render();
            },

            render: function () {
                this.$el.html(this.template({
                    stop: this.model.toJSON()
                }));

                this.stopMapView = new StopMapView({
                    el: '.map-view',
                    model: this.model
                });

                this.model.on('sync', function () {
                    this.refreshStops();
                }, this);
            },

            refreshStops: function () {
                this.stopMapView.layers.stopsBboxLayer.layer.refresh({force:true});
            },

            onEdit: function (event) {
                var $target = $(event.currentTarget);
                this.model.set($target.attr('name'), $target.val());
            },

            save: function () {
                this.model.save();
            },

        });

    return View;

});