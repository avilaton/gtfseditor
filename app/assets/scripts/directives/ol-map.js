module.exports = function(ngModule) {
  ngModule.directive('olMap', function () {
    return {
      restrict: 'A',
      link: function (scope, element, attrs) {
        var attr = 'olMap';
        var prop = attrs[attr];
        var map = (scope.$eval(prop));
        map.setTarget(element[0]);
      }
    };
  });
};