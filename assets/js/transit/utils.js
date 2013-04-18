define(["OpenLayers"], function (OpenLayers) {
    'use strict';

    var utils = {};


    utils.endsRenderer = function (map) {
        var notesLayer = map.getLayer('notes'),
            routesLayer = map.getLayer('routes');
        var startFeature = notesLayer.getFeatureById('routeStart'),
            endFeature = notesLayer.getFeatureById('routeEnd'),
            route = routesLayer.features[0],
            startPoint = route.geometry.components[0],
            endPoint = route.geometry.components[route.geometry.components.length - 1];
        if (startFeature) {
            notesLayer.removeFeatures(startFeature);
        }
        if (endFeature) {
            notesLayer.removeFeatures(endFeature);
        }

        startFeature = new OpenLayers.Feature.Vector(startPoint);
        startFeature.id = 'routeStart';
        startFeature.attributes.type = 'Start';

        endFeature = new OpenLayers.Feature.Vector(endPoint);
        endFeature.id = 'routeEnd';
        endFeature.attributes.type = 'End';

        notesLayer.addFeatures([startFeature, endFeature]);
    };

    return utils;
});