require.config({
    baseUrl: 'js',
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
        "backbone": "../../bower_components/backbone-amd/backbone",
        "jquery": "../../bower_components/jquery/jquery",
        "bootstrap": "../../bower_components/bootstrap/docs/assets/js/bootstrap",
        "OpenLayers": "lib/OpenLayers",
        // "OpenLayers": "../../bower_components/openlayers/lib/OpenLayers",
        "underscore": "../../bower_components/underscore-amd/underscore",
        "handlebars": "../../bower_components/handlebars/handlebars",
        "text": "../../bower_components/requirejs-text/text"
    }
});
