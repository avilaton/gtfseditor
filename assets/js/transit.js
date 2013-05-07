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
        "transit/config",
        "jquery"], function (model, ui, config, $) {
    'use strict';

    var dataModel;

    dataModel = model.init();

    dataModel.done(function(response) {
        window.dataModel = dataModel;
    })
    //console.log(dataModel);

    ui.init({
        dataModel: dataModel,
        controls: 'editor'
    });


});
