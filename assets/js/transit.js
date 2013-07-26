require.config({
  baseUrl: 'assets/js/lib',
    shim: {
        OpenLayers: {
            exports: 'OpenLayers'
        },
        handlebars: {
            exports: 'Handlebars'
        }
    },
    paths: {
      "transit": "../transit",
      "backbone": "backbone-amd/backbone",
      //"jquery": "jquery/jquery",
      "openlayers": "/openlayers/",
      "requirejs": "/requirejs/",
      "underscore": "underscore-amd/underscore"
    }
});

require(["jquery",
        "backbone",
        "underscore",
        "transit/model",
        "transit/ui", 
        "transit/config"], function ($, Backbone, _, model, ui, config) {
    'use strict';

    var dataModel;

    console.log($(), Backbone);
    dataModel = model.init();

    ui.init({
        controls: 'editor'
    });


});
