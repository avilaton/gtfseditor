'use strict';

define([
  'underscore',
  'backbone',
  'JST',
  'config'
  ], function (_, Backbone, JST, Config) {
    var View;

    View = Backbone.View.extend({
      tagName: 'div',

      template: JST.home,

      initialize: function(){
        var self = this;
        $.get(Config.server + 'api/stats').then(function(stats) {
          self.stats = stats;
          self.render();
        });
      },

      render: function () {
        this.$el.html(this.template({
          stats: this.stats
        }));
        $('.main-view').empty().append(this.el);
        this.delegateEvents(this.events);
      }
    });

    return View;
  });