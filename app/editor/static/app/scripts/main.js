/*jshint camelcase: false */

'use strict';

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
            deps: ['jquery'],
            exports: '$.fn.popover'
        },
        backbone: {
            deps: ['underscore']
        },
        'moment-duration-format': {
            deps: ['moment']
        }
    },
    paths: {
        'backbone': '../bower_components/backbone-amd/backbone-min',
        'jquery': '../bower_components/jquery/dist/jquery.min',
        'bootstrap': '../bower_components/bootstrap/dist/js/bootstrap.min',
        'OpenLayers': '../vendor/OpenLayers',
        // 'OpenLayers': '../bower_components/openlayers/lib/OpenLayers',
        'underscore': '../bower_components/underscore-amd/underscore-min',
        'handlebars': '../bower_components/handlebars/handlebars.min',
        'text': '../bower_components/requirejs-text/text',
        'async': '../bower_components/requirejs-plugins/src/async',
        'moment': '../bower_components/moment/moment',
        'moment-duration-format': '../bower_components/moment-duration-format/lib/moment-duration-format'
    }
});

require(['router', 'bootstrap', 'handlebars'],
    function (Router, Bootstrap, Handlebars) {

    Handlebars.registerHelper('checked', function (flag) {
        var boolFlag = Boolean(Number(flag));
        return boolFlag === true ? ' checked ' : '';
    });

    Handlebars.registerHelper('selected', function (value1, value2) {
        var boolFlag = value1 === value2;
        return boolFlag === true ? ' selected="selected" ' : '';
    });

    Handlebars.registerHelper('if_eq', function(a, b, opts) {
        if(a === b)
            return opts.fn(this);
        else
            return opts.inverse(this);
    });

    window.App = {};

    App.router = Router.initialize();

});
