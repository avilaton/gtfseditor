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

    parse: function (response) {
      return response.calendars;
    },

    save: function () {
        var self = this;
        var req = api.put({
            url: self.url,
            data: JSON.stringify({
                calendars: self.toJSON()
            })
        });
        return req;
    },

  });

  return RouteCollection;
})