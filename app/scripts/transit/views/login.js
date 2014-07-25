define([
    "underscore",
    "backbone",
    "handlebars",
    "text!transit/templates/login.handlebars"
], function (_, Backbone, Handlebars, tmpl) {
    var View;

    View = Backbone.View.extend({
        el: $("#login-form-container"),
        
        template: Handlebars.compile(tmpl),

        events: {
            "submit form": "onSubmit"
        },

        initialize: function(){
            var self = this;
            
            this.render();
        },

        render: function () {
            var self = this;

            this.$el.html(this.template({
                // routes: self.collection.toJSON()
            }));
        },

        onSubmit: function (event) {
            event.preventDefault();
            var data = {};

            data.email = $("input[name='email']").val();
            data.password = $("input[name='password']").val();
            data.keep = $("input[name='keep']").is(':checked');

            console.log(data);
            $.post('/login', data);

            // console.log(data);
            // this.model.set(data);
        }

    });

    return View;
})