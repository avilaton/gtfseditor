var angular = require('angular')
var templateUrl = require('./navbar.html');

var ngModule = angular.module('components.navbar', [
])
  .component('navbar', {
    templateUrl: templateUrl
  })

module.exports = ngModule.name
