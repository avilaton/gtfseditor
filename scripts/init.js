require.config({
    baseUrl: 'scripts',
    shim: {
        OpenLayers: {
            exports: 'OpenLayers'
        },
        handlebars: {
            exports: 'Handlebars'
        },
        bootstrap: {
            deps: ["jquery"],
            exports: "$.fn.popover"
        },
        backbone: {
            deps: ["underscore"]
        }
    },
    paths: {
        "backbone": "/bower_components/backbone-amd/backbone-min",
        "jquery": "/bower_components/jquery/dist/jquery.min",
        "bootstrap": "/bower_components/bootstrap/dist/js/bootstrap.min",
        "OpenLayers": "/vendor/OpenLayers",
        // "OpenLayers": "/bower_components/openlayers/lib/OpenLayers",
        "underscore": "/bower_components/underscore-amd/underscore-min",
        "handlebars": "/bower_components/handlebars/handlebars.min",
        "text": "/bower_components/requirejs-text/text",
        "async": "/bower_components/requirejs-plugins/src/async"
    }
});

require(['router'],
    function (Router) {
    'use strict';

    Router.initialize();

});
