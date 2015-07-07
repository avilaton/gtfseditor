define([
  'underscore',
  'backbone',
  'api',
  'config',
  'models/calendar'
], function (_, Backbone, api, Config, CalendarModel) {
  var RouteCollection;

  RouteCollection = Backbone.Collection.extend({
    model: CalendarModel,

    url: Config.server + 'api/calendars/',

    save: function () {
      _.forEach(this.models, function (model) {
        console.log(model, model.isNew(), model.hasChanged());
        if (model.isNew() || model.hasChanged()) {
          model.save();
        };
      });
    },

  });

  return RouteCollection;
})