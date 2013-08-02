require.config({
    baseUrl: 'assets/js',
    shim: {
        OpenLayers: {
            exports: 'OpenLayers'
        },
        handlebars: {
            exports: 'Handlebars'
        }
    },
    paths: {
        "backbone": "lib/backbone-amd/backbone",
        "jquery": "lib/jquery/jquery",
        "OpenLayers": "lib/OpenLayers",
        // "OpenLayers": "lib/openlayers/lib/OpenLayers",
        "underscore": "lib/underscore-amd/underscore",
        "handlebars": "lib/handlebars/handlebars"
    }
});

require(["transit/model",
        "transit/ui", 
        "transit/config"], function (model, ui, config) {
    'use strict';

    var dataModel;

    dataModel = model.init();

    ui.init({
        controls: 'editor'
    });


});
