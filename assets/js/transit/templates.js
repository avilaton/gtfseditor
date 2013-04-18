define(["handlebars"], function(Handlebars) {
    var templates = {};


    Handlebars.registerHelper('boolCompare', function (is_timepoint) {
        if (is_timepoint) {
            return "Si"
        } else {
            return "No"
        }
        return statusClass[status];
    });

    //templates.stops = Handlebars.compile($('#stopsTemplate').html());

    templates.stop = Handlebars.compile($('#stopInfoTemplate').html());

    templates.multiple = Handlebars.compile($('#multipleTemplate').html());

    templates.schedule = Handlebars.compile($('#scheduleTemplate').html());

    return templates;
});