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
        transit: '../transit'
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
