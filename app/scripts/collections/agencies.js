define([
  'underscore',
  'backbone',
  'api',
  'config',
  'models/agency'
], function (_, Backbone, api, Config, AgencyModel) {
  var RouteCollection;

  RouteCollection = Backbone.Collection.extend({
    model: AgencyModel,

    url: Config.server + 'api/agency/',

    parse: function (response) {
      return response.agencies;
    },

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