require([
    "config",
    "transit/init",
    "transit/models/state"
    ],
    function (config, init, StateModel) {
    'use strict';

    var app = window.app = {};

    app.state = new StateModel();

    init.createControls();

});
