require([
    "config",
    "transit/views/login"
    ],
    function (config, LoginView) {
    'use strict';

    var app = window.app = {};

    var myLoginView = new LoginView();

    // app.state = new StateModel();

    // init.createControls();
    console.log("we have liftoff");

});
