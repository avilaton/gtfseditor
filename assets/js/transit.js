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
        "backbone": "../../bower_components/backbone-amd/backbone",
        "jquery": "../../bower_components/jquery/jquery",
        "OpenLayers": "lib/OpenLayers",
        // "OpenLayers": "../../bower_components/openlayers/lib/OpenLayers",
        "underscore": "../../bower_components/underscore-amd/underscore",
        "handlebars": "../../bower_components/handlebars/handlebars",
        "text": "../../bower_components/requirejs-text/text"
    }
});

require([
    "transit/init",
    "transit/model",
    "transit/ui", 
    "transit/config"
    ],
    function (init, model, ui, config) {
    'use strict';

    var dataModel;

    dataModel = model.init();

    ui.init({
        controls: 'editor'
    });

    init.createControls();

});
