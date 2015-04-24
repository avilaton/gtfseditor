define(['handlebars'], function(Handlebars) {

this["JST"] = this["JST"] || {};

this["JST"]["agencies"] = Handlebars.template({"1":function(depth0,helpers,partials,data) {
  var helper, lambda=this.lambda, escapeExpression=this.escapeExpression, functionType="function", helperMissing=helpers.helperMissing;
  return "      <tr data-index=\""
    + escapeExpression(lambda((data && data.index), depth0))
    + "\">\n        <td>"
    + escapeExpression(((helper = (helper = helpers.agency_name || (depth0 != null ? depth0.agency_name : depth0)) != null ? helper : helperMissing),(typeof helper === functionType ? helper.call(depth0, {"name":"agency_name","hash":{},"data":data}) : helper)))
    + "</td>\n        <td>"
    + escapeExpression(((helper = (helper = helpers.agency_url || (depth0 != null ? depth0.agency_url : depth0)) != null ? helper : helperMissing),(typeof helper === functionType ? helper.call(depth0, {"name":"agency_url","hash":{},"data":data}) : helper)))
    + "</td>\n        <td>"
    + escapeExpression(((helper = (helper = helpers.agency_timezone || (depth0 != null ? depth0.agency_timezone : depth0)) != null ? helper : helperMissing),(typeof helper === functionType ? helper.call(depth0, {"name":"agency_timezone","hash":{},"data":data}) : helper)))
    + "</td>\n        <td>"
    + escapeExpression(((helper = (helper = helpers.agency_lang || (depth0 != null ? depth0.agency_lang : depth0)) != null ? helper : helperMissing),(typeof helper === functionType ? helper.call(depth0, {"name":"agency_lang","hash":{},"data":data}) : helper)))
    + "</td>\n        <td>"
    + escapeExpression(((helper = (helper = helpers.agency_phone || (depth0 != null ? depth0.agency_phone : depth0)) != null ? helper : helperMissing),(typeof helper === functionType ? helper.call(depth0, {"name":"agency_phone","hash":{},"data":data}) : helper)))
    + "</td>\n        <td class=\"\">\n          <button class=\"btn btn-default btn-rm\"><span class=\"glyphicon glyphicon-remove\"></span></button>\n          <button class=\"btn btn-default btn-edit\"><span class=\"glyphicon glyphicon-pencil\"></span></button>\n        </td>\n      </tr>\n";
},"compiler":[6,">= 2.0.0-beta.1"],"main":function(depth0,helpers,partials,data) {
  var stack1, buffer = "<div class=\"col-md-12 panel-right\">\n  <h1>Agencies</h1>\n  <div class=\"row voffset1\">\n    <div class=\"col-md-12\">\n      <form class=\"form-inline\">\n        <button class=\"btn btn-default btn-create\"><span class=\"glyphicon glyphicon-plus\"></span> New</button>\n      </form>\n    </div>\n  </div>\n  <table class=\"table\">\n    <thead>\n      <tr>\n        <th>Name</th>\n        <th>URL</th>\n        <th>Timezone</th>\n        <th>Language</th>\n        <th>Phone</th>\n        <th></th>\n      </tr>\n    </thead>\n    <tbody>\n";
  stack1 = helpers.each.call(depth0, (depth0 != null ? depth0.models : depth0), {"name":"each","hash":{},"fn":this.program(1, data),"inverse":this.noop,"data":data});
  if (stack1 != null) { buffer += stack1; }
  return buffer + "    </tbody>\n  </table>\n</div>\n";
},"useData":true});



this["JST"]["calendar"] = Handlebars.template({"1":function(depth0,helpers,partials,data) {
  var stack1, helper, lambda=this.lambda, escapeExpression=this.escapeExpression, functionType="function", helperMissing=helpers.helperMissing, buffer = "      <tr data-index=\""
    + escapeExpression(lambda((data && data.index), depth0))
    + "\">\n        <td>"
    + escapeExpression(((helper = (helper = helpers.service_name || (depth0 != null ? depth0.service_name : depth0)) != null ? helper : helperMissing),(typeof helper === functionType ? helper.call(depth0, {"name":"service_name","hash":{},"data":data}) : helper)))
    + "</td>\n        <td>"
    + escapeExpression(((helper = (helper = helpers.start_date || (depth0 != null ? depth0.start_date : depth0)) != null ? helper : helperMissing),(typeof helper === functionType ? helper.call(depth0, {"name":"start_date","hash":{},"data":data}) : helper)))
    + "</td>\n        <td>"
    + escapeExpression(((helper = (helper = helpers.end_date || (depth0 != null ? depth0.end_date : depth0)) != null ? helper : helperMissing),(typeof helper === functionType ? helper.call(depth0, {"name":"end_date","hash":{},"data":data}) : helper)))
    + "</td>\n        <td><span class=\"glyphicon glyphicon-";
  stack1 = ((helpers.if_eq || (depth0 && depth0.if_eq) || helperMissing).call(depth0, (depth0 != null ? depth0.monday : depth0), "1", {"name":"if_eq","hash":{},"fn":this.program(2, data),"inverse":this.noop,"data":data}));
  if (stack1 != null) { buffer += stack1; }
  buffer += "\"></span></td>\n        <td><span class=\"glyphicon glyphicon-";
  stack1 = ((helpers.if_eq || (depth0 && depth0.if_eq) || helperMissing).call(depth0, (depth0 != null ? depth0.tuesday : depth0), "1", {"name":"if_eq","hash":{},"fn":this.program(2, data),"inverse":this.noop,"data":data}));
  if (stack1 != null) { buffer += stack1; }
  buffer += "\"></span></td>\n        <td><span class=\"glyphicon glyphicon-";
  stack1 = ((helpers.if_eq || (depth0 && depth0.if_eq) || helperMissing).call(depth0, (depth0 != null ? depth0.wednesday : depth0), "1", {"name":"if_eq","hash":{},"fn":this.program(2, data),"inverse":this.noop,"data":data}));
  if (stack1 != null) { buffer += stack1; }
  buffer += "\"></span></td>\n        <td><span class=\"glyphicon glyphicon-";
  stack1 = ((helpers.if_eq || (depth0 && depth0.if_eq) || helperMissing).call(depth0, (depth0 != null ? depth0.thursday : depth0), "1", {"name":"if_eq","hash":{},"fn":this.program(2, data),"inverse":this.noop,"data":data}));
  if (stack1 != null) { buffer += stack1; }
  buffer += "\"></span></td>\n        <td><span class=\"glyphicon glyphicon-";
  stack1 = ((helpers.if_eq || (depth0 && depth0.if_eq) || helperMissing).call(depth0, (depth0 != null ? depth0.friday : depth0), "1", {"name":"if_eq","hash":{},"fn":this.program(2, data),"inverse":this.noop,"data":data}));
  if (stack1 != null) { buffer += stack1; }
  buffer += "\"></span></td>\n        <td><span class=\"glyphicon glyphicon-";
  stack1 = ((helpers.if_eq || (depth0 && depth0.if_eq) || helperMissing).call(depth0, (depth0 != null ? depth0.saturday : depth0), "1", {"name":"if_eq","hash":{},"fn":this.program(2, data),"inverse":this.noop,"data":data}));
  if (stack1 != null) { buffer += stack1; }
  buffer += "\"></span></td>\n        <td><span class=\"glyphicon glyphicon-";
  stack1 = ((helpers.if_eq || (depth0 && depth0.if_eq) || helperMissing).call(depth0, (depth0 != null ? depth0.sunday : depth0), "1", {"name":"if_eq","hash":{},"fn":this.program(2, data),"inverse":this.noop,"data":data}));
  if (stack1 != null) { buffer += stack1; }
  return buffer + "\"></span></td>\n        <td class=\"vcenter\">\n          <button class=\"btn btn-default btn-rm\"><span class=\"glyphicon glyphicon-remove\"></span></button>\n          <button class=\"btn btn-default btn-edit\"><span class=\"glyphicon glyphicon-pencil\"></span></button>\n        </td>\n      </tr>\n";
},"2":function(depth0,helpers,partials,data) {
  return "ok";
  },"compiler":[6,">= 2.0.0-beta.1"],"main":function(depth0,helpers,partials,data) {
  var stack1, buffer = "<div class=\"col-md-12 panel-right\">\n  <h1>Service periods</h1>\n  <div class=\"row voffset1\">\n    <div class=\"col-md-12\">\n      <form class=\"form-inline\">\n        <button class=\"btn btn-default btn-create\"><span class=\"glyphicon glyphicon-plus\"></span> New</button>\n      </form>\n    </div>\n  </div>\n  <table class=\"table\">\n    <thead>\n      <tr>\n        <th class=\"col-md-2\">Service Name</th>\n        <th class=\"col-md-1\">Starts</th>\n        <th class=\"col-md-1\">Ends</th>\n        <th class=\"col-md-1\">Monday</th>\n        <th class=\"col-md-1\">Tuesday</th>\n        <th class=\"col-md-1\">Wednesday</th>\n        <th class=\"col-md-1\">Thursday</th>\n        <th class=\"col-md-1\">Friday</th>\n        <th class=\"col-md-1\">Saturday</th>\n        <th class=\"col-md-1\">Sunday</th>\n        <th class=\"col-md-1\"></th>\n      </tr>\n    </thead>\n    <tbody>\n";
  stack1 = helpers.each.call(depth0, (depth0 != null ? depth0.models : depth0), {"name":"each","hash":{},"fn":this.program(1, data),"inverse":this.noop,"data":data});
  if (stack1 != null) { buffer += stack1; }
  return buffer + "    </tbody>\n  </table>\n</div>\n";
},"useData":true});



this["JST"]["calendarsSelect"] = Handlebars.template({"1":function(depth0,helpers,partials,data) {
  var helper, functionType="function", helperMissing=helpers.helperMissing, escapeExpression=this.escapeExpression;
  return "          <option value=\""
    + escapeExpression(((helper = (helper = helpers.service_id || (depth0 != null ? depth0.service_id : depth0)) != null ? helper : helperMissing),(typeof helper === functionType ? helper.call(depth0, {"name":"service_id","hash":{},"data":data}) : helper)))
    + "\">"
    + escapeExpression(((helper = (helper = helpers.service_name || (depth0 != null ? depth0.service_name : depth0)) != null ? helper : helperMissing),(typeof helper === functionType ? helper.call(depth0, {"name":"service_name","hash":{},"data":data}) : helper)))
    + "</option>\n";
},"compiler":[6,">= 2.0.0-beta.1"],"main":function(depth0,helpers,partials,data) {
  var stack1, buffer = "<form class=\"form-horizontal\" role=\"form\">\n  <div class=\"form-group\">\n    <label for=\"route\" class=\"col-sm-2 control-label\">Calendars</label>\n    <div class=\"col-sm-8\">\n      <select class=\"form-control\">\n        <option value=\"\"> -- </option>\n";
  stack1 = helpers.each.call(depth0, (depth0 != null ? depth0.models : depth0), {"name":"each","hash":{},"fn":this.program(1, data),"inverse":this.noop,"data":data});
  if (stack1 != null) { buffer += stack1; }
  return buffer + "      </select>\n    </div>\n  </div>\n</form>\n";
},"useData":true});



this["JST"]["calendarsTools"] = Handlebars.template({"compiler":[6,">= 2.0.0-beta.1"],"main":function(depth0,helpers,partials,data) {
  return "<div class=\"row\">\n  <div class=\"col-md-12\">\n    <form class=\"form-inline\">\n      <div class=\"form-group\">\n        <label for=\"speed\">Offset</label>\n        <input name=\"offset-min\" type=\"number\" class=\"form-control offset-min\" placeholder=\"minutes\">\n        <button class=\"btn btn-default btn-offset\">Set</button>\n      </div>\n    </form>\n  </div>\n</div>\n\n<hr>\n\n<div class=\"row\">\n  <div class=\"col-md-12\">\n    <form class=\"form\">\n      <div class=\"form-group\">\n        <label for=\"bulk\">Add many (HH:MM)</label>\n        <textarea class=\"form-control bulk-load\" rows=\"3\" name=\"bulk\" placeholder=\"Insert times separated by commas or newlines, for example: 08:11, 09:21, 10:43\"></textarea>\n        <button class=\"btn btn-default btn-bulk-load pull-right voffset1\">Load</button>\n      </div>\n    </form>\n  </div>\n</div>\n\n<div class=\"row\">\n  <div class=\"col-md-12\">\n    <form class=\"form-inline voffset1 pull-right\">\n      <div class=\"form-group\">\n        <button class=\"btn btn-default add-btn\">\n          <span class=\"glyphicon glyphicon-plus\"></span> Add Time\n        </button>\n        <button class=\"btn btn-default btn-reset\">\n          <span class=\"glyphicon glyphicon-trash\"></span> Clean\n        </button>\n      </div>\n    </form>\n  </div>\n</div>\n\n<div class=\"row\">\n  <div class=\"col-md-12\">\n    <form class=\"form-inline voffset1 pull-right\">\n      <div class=\"form-group\">\n        <button class=\"btn btn-default save-btn\">\n          <span class=\"glyphicon glyphicon-save\"></span> Save Times\n        </button>\n      </div>\n    </form>\n  </div>\n</div>";
  },"useData":true});



this["JST"]["fileUpload"] = Handlebars.template({"compiler":[6,">= 2.0.0-beta.1"],"main":function(depth0,helpers,partials,data) {
  return "<form role=\"form\" class=\"upload\">\n  <div class=\"form-group\">\n    <label for=\"exampleInputFile\">File input</label>\n    <input type=\"file\" name=\"file\" class=\"file\">\n    <p class=\"help-block\">specified format</p>\n  </div>\n  <button type=\"submit\" class=\"btn btn-default btn-upload\">Submit</button>\n</form>";
  },"useData":true});



this["JST"]["filter"] = Handlebars.template({"compiler":[6,">= 2.0.0-beta.1"],"main":function(depth0,helpers,partials,data) {
  return "<div class=\"input-group\">\n  <input type=\"text\" class=\"form-control filter-value\" placeholder=\"Enter a stop_code\">\n  <span class=\"input-group-btn\">\n    <button class=\"btn btn-default filter-button\" type=\"button\"><i class=\"glyphicon glyphicon-search\"></i></button>\n  </span>\n</div>\n";
  },"useData":true});



this["JST"]["kmlSelect"] = Handlebars.template({"1":function(depth0,helpers,partials,data) {
  var helper, functionType="function", helperMissing=helpers.helperMissing, escapeExpression=this.escapeExpression;
  return "	    <option value=\""
    + escapeExpression(((helper = (helper = helpers.value || (depth0 != null ? depth0.value : depth0)) != null ? helper : helperMissing),(typeof helper === functionType ? helper.call(depth0, {"name":"value","hash":{},"data":data}) : helper)))
    + "\">"
    + escapeExpression(((helper = (helper = helpers.value || (depth0 != null ? depth0.value : depth0)) != null ? helper : helperMissing),(typeof helper === functionType ? helper.call(depth0, {"name":"value","hash":{},"data":data}) : helper)))
    + "</option>\n";
},"compiler":[6,">= 2.0.0-beta.1"],"main":function(depth0,helpers,partials,data) {
  var stack1, buffer = "<label for=\"kml\">Kml\n	<select class=\"form-control\" id=\"kml\">\n	  <option value=\"\"> -- </option>\n";
  stack1 = helpers.each.call(depth0, (depth0 != null ? depth0.options : depth0), {"name":"each","hash":{},"fn":this.program(1, data),"inverse":this.noop,"data":data});
  if (stack1 != null) { buffer += stack1; }
  return buffer + "	</select>\n</label>\n";
},"useData":true});



this["JST"]["login"] = Handlebars.template({"compiler":[6,">= 2.0.0-beta.1"],"main":function(depth0,helpers,partials,data) {
  return "<form class=\"form-signin\">\n	<h2 class=\"form-signin-heading\">Please sign in</h2>\n	<input type=\"text\" class=\"input-block-level\" placeholder=\"Email address\" name=\"email\">\n	<input type=\"password\" class=\"input-block-level\" placeholder=\"Password\" name=\"password\">\n	<label class=\"checkbox\">\n	  <input type=\"checkbox\" value=\"remember-me\" name=\"keep\"> Remember me\n	</label>\n	<button class=\"btn btn-large btn-primary\" type=\"submit\">Sign in</button>\n</form>";
  },"useData":true});



this["JST"]["modals/agency"] = Handlebars.template({"1":function(depth0,helpers,partials,data) {
  return "      <h3 class=\"modal-title\">Edit Agency</h3>\n";
  },"3":function(depth0,helpers,partials,data) {
  return "      <h3 class=\"modal-title\">Add New Agency</h3>\n";
  },"compiler":[6,">= 2.0.0-beta.1"],"main":function(depth0,helpers,partials,data) {
  var stack1, helper, functionType="function", helperMissing=helpers.helperMissing, escapeExpression=this.escapeExpression, buffer = "<div class=\"modal-dialog\">\n  <div class=\"modal-content\">\n    <div class=\"modal-header\">\n      <button type=\"button\" class=\"close\" data-dismiss=\"modal\" aria-hidden=\"true\">\n        <span aria-hidden=\"true\">&times;</span><span class=\"sr-only\">Close</span>\n      </button>\n";
  stack1 = helpers['if'].call(depth0, (depth0 != null ? depth0.agency_id : depth0), {"name":"if","hash":{},"fn":this.program(1, data),"inverse":this.program(3, data),"data":data});
  if (stack1 != null) { buffer += stack1; }
  return buffer + "    </div>\n\n    <div class=\"modal-body\">\n      <form role=\"form\" >\n        <div class=\"form-group\">\n          <label for=\"agency_lang\">agency_lang</label>\n          <input class=\"form-control\" type=\"text\" name=\"agency_lang\" placeholder=\"agency_lang\" value=\""
    + escapeExpression(((helper = (helper = helpers.agency_lang || (depth0 != null ? depth0.agency_lang : depth0)) != null ? helper : helperMissing),(typeof helper === functionType ? helper.call(depth0, {"name":"agency_lang","hash":{},"data":data}) : helper)))
    + "\">\n        </div>\n        <div class=\"form-group\">\n          <label for=\"agency_name\">agency_name</label>\n            <input class=\"form-control\" type=\"text\" name=\"agency_name\" placeholder=\"agency_name\" value=\""
    + escapeExpression(((helper = (helper = helpers.agency_name || (depth0 != null ? depth0.agency_name : depth0)) != null ? helper : helperMissing),(typeof helper === functionType ? helper.call(depth0, {"name":"agency_name","hash":{},"data":data}) : helper)))
    + "\">\n        </div>\n        <div class=\"form-group\">\n          <label for=\"agency_phone\">agency_phone</label>\n            <input class=\"form-control\" type=\"text\" name=\"agency_phone\" placeholder=\"agency_phone\" value=\""
    + escapeExpression(((helper = (helper = helpers.agency_phone || (depth0 != null ? depth0.agency_phone : depth0)) != null ? helper : helperMissing),(typeof helper === functionType ? helper.call(depth0, {"name":"agency_phone","hash":{},"data":data}) : helper)))
    + "\">\n        </div>\n        <div class=\"form-group\">\n          <label for=\"agency_timezone\">agency_timezone</label>\n            <input class=\"form-control\" type=\"text\" name=\"agency_timezone\" placeholder=\"agency_timezone\" value=\""
    + escapeExpression(((helper = (helper = helpers.agency_timezone || (depth0 != null ? depth0.agency_timezone : depth0)) != null ? helper : helperMissing),(typeof helper === functionType ? helper.call(depth0, {"name":"agency_timezone","hash":{},"data":data}) : helper)))
    + "\">\n        </div>\n        <div class=\"form-group\">\n          <label for=\"agency_url\">agency_url</label>\n          <input class=\"form-control\" type=\"text\" name=\"agency_url\" placeholder=\"agency_url\" value=\""
    + escapeExpression(((helper = (helper = helpers.agency_url || (depth0 != null ? depth0.agency_url : depth0)) != null ? helper : helperMissing),(typeof helper === functionType ? helper.call(depth0, {"name":"agency_url","hash":{},"data":data}) : helper)))
    + "\">\n        </div>\n      </form>\n    </div>\n\n    <div class=\"modal-footer\">\n      <button type=\"button\" class=\"btn btn-default\" data-dismiss=\"modal\">Close</button>\n      <button type=\"button\" class=\"btn btn-primary js-save\">Save changes</button>\n    </div>\n  </div>\n</div>\n";
},"useData":true});



this["JST"]["modals/calendar"] = Handlebars.template({"1":function(depth0,helpers,partials,data) {
  return "      <h3 class=\"modal-title\">Edit Service Period</h3>\n";
  },"3":function(depth0,helpers,partials,data) {
  return "      <h3 class=\"modal-title\">Add New Service Period</h3>\n";
  },"compiler":[6,">= 2.0.0-beta.1"],"main":function(depth0,helpers,partials,data) {
  var stack1, helper, functionType="function", helperMissing=helpers.helperMissing, escapeExpression=this.escapeExpression, buffer = "<div class=\"modal-dialog\">\n  <div class=\"modal-content\">\n    <div class=\"modal-header\">\n      <button type=\"button\" class=\"close\" data-dismiss=\"modal\" aria-hidden=\"true\">\n        <span aria-hidden=\"true\">&times;</span><span class=\"sr-only\">Close</span>\n      </button>\n";
  stack1 = helpers['if'].call(depth0, (depth0 != null ? depth0.service_id : depth0), {"name":"if","hash":{},"fn":this.program(1, data),"inverse":this.program(3, data),"data":data});
  if (stack1 != null) { buffer += stack1; }
  return buffer + "    </div>\n\n    <div class=\"modal-body\">\n      <form role=\"form\" >\n        <div class=\"form-group\">\n          <label for=\"service_name\">service_name</label>\n            <input class=\"form-control\" type=\"text\" name=\"service_name\" placeholder=\"service_name\" value=\""
    + escapeExpression(((helper = (helper = helpers.service_name || (depth0 != null ? depth0.service_name : depth0)) != null ? helper : helperMissing),(typeof helper === functionType ? helper.call(depth0, {"name":"service_name","hash":{},"data":data}) : helper)))
    + "\">\n        </div>\n        <div class=\"form-group\">\n          <label for=\"start_date\">start_date</label>\n            <input class=\"form-control\" type=\"text\" name=\"start_date\" placeholder=\"start_date\" value=\""
    + escapeExpression(((helper = (helper = helpers.start_date || (depth0 != null ? depth0.start_date : depth0)) != null ? helper : helperMissing),(typeof helper === functionType ? helper.call(depth0, {"name":"start_date","hash":{},"data":data}) : helper)))
    + "\">\n        </div>\n        <div class=\"form-group\">\n          <label for=\"end_date\">end_date</label>\n            <input class=\"form-control\" type=\"text\" name=\"end_date\" placeholder=\"end_date\" value=\""
    + escapeExpression(((helper = (helper = helpers.end_date || (depth0 != null ? depth0.end_date : depth0)) != null ? helper : helperMissing),(typeof helper === functionType ? helper.call(depth0, {"name":"end_date","hash":{},"data":data}) : helper)))
    + "\">\n        </div>\n        <div class=\"form-group\">\n          <label>\n            <input type=\"checkbox\" name=\"monday\" "
    + escapeExpression(((helpers.checked || (depth0 && depth0.checked) || helperMissing).call(depth0, (depth0 != null ? depth0.monday : depth0), {"name":"checked","hash":{},"data":data})))
    + ">monday\n          </label>\n        </div>\n        <div class=\"form-group\">\n          <label>\n            <input type=\"checkbox\" name=\"tuesday\" "
    + escapeExpression(((helpers.checked || (depth0 && depth0.checked) || helperMissing).call(depth0, (depth0 != null ? depth0.tuesday : depth0), {"name":"checked","hash":{},"data":data})))
    + ">tuesday\n          </label>\n        </div>\n        <div class=\"form-group\">\n          <label>\n            <input type=\"checkbox\" name=\"wednesday\" "
    + escapeExpression(((helpers.checked || (depth0 && depth0.checked) || helperMissing).call(depth0, (depth0 != null ? depth0.wednesday : depth0), {"name":"checked","hash":{},"data":data})))
    + ">wednesday\n          </label>\n        </div>\n        <div class=\"form-group\">\n          <label>\n            <input type=\"checkbox\" name=\"thursday\" "
    + escapeExpression(((helpers.checked || (depth0 && depth0.checked) || helperMissing).call(depth0, (depth0 != null ? depth0.thursday : depth0), {"name":"checked","hash":{},"data":data})))
    + ">thursday\n          </label>\n        </div>\n        <div class=\"form-group\">\n          <label>\n            <input type=\"checkbox\" name=\"friday\" "
    + escapeExpression(((helpers.checked || (depth0 && depth0.checked) || helperMissing).call(depth0, (depth0 != null ? depth0.friday : depth0), {"name":"checked","hash":{},"data":data})))
    + ">friday\n          </label>\n        </div>\n        <div class=\"form-group\">\n          <label>\n            <input type=\"checkbox\" name=\"saturday\" "
    + escapeExpression(((helpers.checked || (depth0 && depth0.checked) || helperMissing).call(depth0, (depth0 != null ? depth0.saturday : depth0), {"name":"checked","hash":{},"data":data})))
    + ">saturday\n          </label>\n        </div>\n        <div class=\"form-group\">\n          <label>\n            <input type=\"checkbox\" name=\"sunday\" "
    + escapeExpression(((helpers.checked || (depth0 && depth0.checked) || helperMissing).call(depth0, (depth0 != null ? depth0.sunday : depth0), {"name":"checked","hash":{},"data":data})))
    + ">sunday\n          </label>\n        </div>\n      </form>\n    </div>\n\n    <div class=\"modal-footer\">\n      <button type=\"button\" class=\"btn btn-default\" data-dismiss=\"modal\">Close</button>\n      <button type=\"button\" class=\"btn btn-primary js-save\">Save changes</button>\n    </div>\n  </div>\n</div>\n";
},"useData":true});



this["JST"]["modals/route"] = Handlebars.template({"1":function(depth0,helpers,partials,data) {
  var stack1, lambda=this.lambda, escapeExpression=this.escapeExpression;
  return "      <h3 class=\"modal-title\">Edit Route: "
    + escapeExpression(lambda(((stack1 = (depth0 != null ? depth0.route : depth0)) != null ? stack1.route_short_name : stack1), depth0))
    + "</h3>\n";
},"3":function(depth0,helpers,partials,data) {
  return "      <h3 class=\"modal-title\">Add New Route</h3>\n";
  },"5":function(depth0,helpers,partials,data,depths) {
  var stack1, helper, functionType="function", helperMissing=helpers.helperMissing, escapeExpression=this.escapeExpression, buffer = "                <option value=\""
    + escapeExpression(((helper = (helper = helpers.agency_id || (depth0 != null ? depth0.agency_id : depth0)) != null ? helper : helperMissing),(typeof helper === functionType ? helper.call(depth0, {"name":"agency_id","hash":{},"data":data}) : helper)))
    + "\" ";
  stack1 = ((helpers.selected || (depth0 && depth0.selected) || helperMissing).call(depth0, (depth0 != null ? depth0.agency_id : depth0), ((stack1 = (depths[1] != null ? depths[1].route : depths[1])) != null ? stack1.agency_id : stack1), {"name":"selected","hash":{},"fn":this.program(6, data, depths),"inverse":this.noop,"data":data}));
  if (stack1 != null) { buffer += stack1; }
  return buffer + ">"
    + escapeExpression(((helper = (helper = helpers.agency_name || (depth0 != null ? depth0.agency_name : depth0)) != null ? helper : helperMissing),(typeof helper === functionType ? helper.call(depth0, {"name":"agency_name","hash":{},"data":data}) : helper)))
    + "</option>\n";
},"6":function(depth0,helpers,partials,data) {
  return "";
},"8":function(depth0,helpers,partials,data) {
  return "checked";
  },"compiler":[6,">= 2.0.0-beta.1"],"main":function(depth0,helpers,partials,data,depths) {
  var stack1, lambda=this.lambda, escapeExpression=this.escapeExpression, buffer = "<div class=\"modal-dialog\">\n  <div class=\"modal-content\">\n    <div class=\"modal-header\">\n      <button type=\"button\" class=\"close\" data-dismiss=\"modal\" aria-hidden=\"true\">\n        <span aria-hidden=\"true\">&times;</span><span class=\"sr-only\">Close</span>\n      </button>\n";
  stack1 = helpers['if'].call(depth0, ((stack1 = (depth0 != null ? depth0.route : depth0)) != null ? stack1.route_id : stack1), {"name":"if","hash":{},"fn":this.program(1, data, depths),"inverse":this.program(3, data, depths),"data":data});
  if (stack1 != null) { buffer += stack1; }
  buffer += "    </div>\n\n    <div class=\"modal-body\">\n      <form role=\"form\" >\n        <div class=\"form-group\">\n          <label for=\"route_short_name\">route_short_name</label>\n          <input class=\"form-control\" type=\"text\" name=\"route_short_name\" placeholder=\"route_short_name\" value=\""
    + escapeExpression(lambda(((stack1 = (depth0 != null ? depth0.route : depth0)) != null ? stack1.route_short_name : stack1), depth0))
    + "\">\n        </div>\n        <div class=\"form-group\">\n          <label for=\"route_long_name\">route_long_name</label>\n            <input class=\"form-control\" type=\"text\" name=\"route_long_name\" placeholder=\"route_long_name\" value=\""
    + escapeExpression(lambda(((stack1 = (depth0 != null ? depth0.route : depth0)) != null ? stack1.route_long_name : stack1), depth0))
    + "\">\n        </div>\n        <div class=\"form-group\">\n          <label for=\"agency-id\" class=\"control-label\">agency</label>\n            <select class=\"form-control select-agency\" id=\"agency-id\">\n              <option value=\"\"> -- </option>\n";
  stack1 = helpers.each.call(depth0, (depth0 != null ? depth0.agencies : depth0), {"name":"each","hash":{},"fn":this.program(5, data, depths),"inverse":this.noop,"data":data});
  if (stack1 != null) { buffer += stack1; }
  buffer += "            </select>\n        </div>\n        <div class=\"form-group\">\n          <label for=\"route_type\">route_type</label>\n          <input class=\"form-control\" type=\"text\" name=\"route_type\" placeholder=\"route_type\" value=\""
    + escapeExpression(lambda(((stack1 = (depth0 != null ? depth0.route : depth0)) != null ? stack1.route_type : stack1), depth0))
    + "\">\n        </div>\n        <div class=\"form-group\">\n          <label for=\"route_color\">route_color</label>\n            <input class=\"form-control\" type=\"text\" name=\"route_color\" placeholder=\"route_color\" value=\""
    + escapeExpression(lambda(((stack1 = (depth0 != null ? depth0.route : depth0)) != null ? stack1.route_color : stack1), depth0))
    + "\">\n        </div>\n        <div class=\"form-group\">\n          <label for=\"route_desc\">route_desc</label>\n            <input class=\"form-control\" type=\"text\" name=\"route_desc\" placeholder=\"route_desc\" value=\""
    + escapeExpression(lambda(((stack1 = (depth0 != null ? depth0.route : depth0)) != null ? stack1.route_desc : stack1), depth0))
    + "\">\n        </div>\n        <div class=\"form-group\">\n            <label>\n              <input type=\"checkbox\" ";
  stack1 = helpers['if'].call(depth0, ((stack1 = (depth0 != null ? depth0.route : depth0)) != null ? stack1.active : stack1), {"name":"if","hash":{},"fn":this.program(8, data, depths),"inverse":this.noop,"data":data});
  if (stack1 != null) { buffer += stack1; }
  return buffer + "> Active\n            </label>\n        </div>\n      </form>\n    </div>\n\n    <div class=\"modal-footer\">\n      <button type=\"button\" class=\"btn btn-default\" data-dismiss=\"modal\">Close</button>\n      <button type=\"button\" class=\"btn btn-primary js-save\">Save changes</button>\n    </div>\n  </div>\n</div>\n";
},"useData":true,"useDepths":true});



this["JST"]["modals/stop"] = Handlebars.template({"1":function(depth0,helpers,partials,data) {
  var helper, functionType="function", helperMissing=helpers.helperMissing, escapeExpression=this.escapeExpression;
  return "      <h3 class=\"modal-title\">Edit Stop: "
    + escapeExpression(((helper = (helper = helpers.stop_code || (depth0 != null ? depth0.stop_code : depth0)) != null ? helper : helperMissing),(typeof helper === functionType ? helper.call(depth0, {"name":"stop_code","hash":{},"data":data}) : helper)))
    + "</h3>\n";
},"3":function(depth0,helpers,partials,data) {
  return "      <h3 class=\"modal-title\">Add New Stop</h3>\n";
  },"compiler":[6,">= 2.0.0-beta.1"],"main":function(depth0,helpers,partials,data) {
  var stack1, helper, functionType="function", helperMissing=helpers.helperMissing, escapeExpression=this.escapeExpression, buffer = "<div class=\"modal-dialog\">\n  <div class=\"modal-content\">\n    <div class=\"modal-header\">\n      <button type=\"button\" class=\"close\" data-dismiss=\"modal\" aria-hidden=\"true\">\n        <span aria-hidden=\"true\">&times;</span><span class=\"sr-only\">Close</span>\n      </button>\n";
  stack1 = helpers['if'].call(depth0, (depth0 != null ? depth0.stop_id : depth0), {"name":"if","hash":{},"fn":this.program(1, data),"inverse":this.program(3, data),"data":data});
  if (stack1 != null) { buffer += stack1; }
  return buffer + "    </div>\n\n    <div class=\"modal-body\">\n      <form role=\"form\" >\n        <div class=\"form-group\">\n          <label for=\"stop_code\">stop_code</label>\n          <input class=\"form-control\" type=\"text\" name=\"stop_code\" placeholder=\"stop_code\" value=\""
    + escapeExpression(((helper = (helper = helpers.stop_code || (depth0 != null ? depth0.stop_code : depth0)) != null ? helper : helperMissing),(typeof helper === functionType ? helper.call(depth0, {"name":"stop_code","hash":{},"data":data}) : helper)))
    + "\">\n        </div>\n        <div class=\"form-group\">\n          <label for=\"stop_name\">stop_name</label>\n          <input class=\"form-control\" type=\"text\" name=\"stop_name\" placeholder=\"stop_name\" value=\""
    + escapeExpression(((helper = (helper = helpers.stop_name || (depth0 != null ? depth0.stop_name : depth0)) != null ? helper : helperMissing),(typeof helper === functionType ? helper.call(depth0, {"name":"stop_name","hash":{},"data":data}) : helper)))
    + "\">\n        </div>\n        <div class=\"form-group\">\n          <label for=\"stop_calle\">stop_calle</label>\n            <input class=\"form-control\" type=\"text\" name=\"stop_calle\" placeholder=\"stop_calle\" value=\""
    + escapeExpression(((helper = (helper = helpers.stop_calle || (depth0 != null ? depth0.stop_calle : depth0)) != null ? helper : helperMissing),(typeof helper === functionType ? helper.call(depth0, {"name":"stop_calle","hash":{},"data":data}) : helper)))
    + "\">\n        </div>\n        <div class=\"form-group\">\n          <label for=\"stop_numero\">stop_numero</label>\n            <input class=\"form-control\" type=\"text\" name=\"stop_numero\" placeholder=\"stop_numero\" value=\""
    + escapeExpression(((helper = (helper = helpers.stop_numero || (depth0 != null ? depth0.stop_numero : depth0)) != null ? helper : helperMissing),(typeof helper === functionType ? helper.call(depth0, {"name":"stop_numero","hash":{},"data":data}) : helper)))
    + "\">\n        </div>\n        <div class=\"form-group\">\n          <label for=\"stop_esquina\">stop_esquina</label>\n            <input class=\"form-control\" type=\"text\" name=\"stop_esquina\" placeholder=\"stop_esquina\" value=\""
    + escapeExpression(((helper = (helper = helpers.stop_esquina || (depth0 != null ? depth0.stop_esquina : depth0)) != null ? helper : helperMissing),(typeof helper === functionType ? helper.call(depth0, {"name":"stop_esquina","hash":{},"data":data}) : helper)))
    + "\">\n        </div>\n        <div class=\"form-group\">\n          <label for=\"stop_entre\">stop_entre</label>\n            <input class=\"form-control\" type=\"text\" name=\"stop_entre\" placeholder=\"stop_entre\" value=\""
    + escapeExpression(((helper = (helper = helpers.stop_entre || (depth0 != null ? depth0.stop_entre : depth0)) != null ? helper : helperMissing),(typeof helper === functionType ? helper.call(depth0, {"name":"stop_entre","hash":{},"data":data}) : helper)))
    + "\">\n        </div>\n        <div class=\"form-group\">\n          <label for=\"stop_desc\">stop_desc</label>\n          <input class=\"form-control\" type=\"text\" name=\"stop_desc\" placeholder=\"stop_desc\" value=\""
    + escapeExpression(((helper = (helper = helpers.stop_desc || (depth0 != null ? depth0.stop_desc : depth0)) != null ? helper : helperMissing),(typeof helper === functionType ? helper.call(depth0, {"name":"stop_desc","hash":{},"data":data}) : helper)))
    + "\">\n        </div>\n      </form>\n    </div>\n\n    <div class=\"modal-footer\">\n      <button type=\"button\" class=\"btn btn-default\" data-dismiss=\"modal\">Close</button>\n      <button type=\"button\" class=\"btn btn-primary js-save\">Save changes</button>\n    </div>\n  </div>\n</div>\n";
},"useData":true});



this["JST"]["modals/trip"] = Handlebars.template({"1":function(depth0,helpers,partials,data) {
  var helper, functionType="function", helperMissing=helpers.helperMissing, escapeExpression=this.escapeExpression;
  return "      <h3 class=\"modal-title\">Edit Trip id: "
    + escapeExpression(((helper = (helper = helpers.trip_headsign || (depth0 != null ? depth0.trip_headsign : depth0)) != null ? helper : helperMissing),(typeof helper === functionType ? helper.call(depth0, {"name":"trip_headsign","hash":{},"data":data}) : helper)))
    + "</h3>\n";
},"3":function(depth0,helpers,partials,data) {
  return "      <h3 class=\"modal-title\">Add New Trip</h3>\n";
  },"5":function(depth0,helpers,partials,data) {
  return "checked";
  },"compiler":[6,">= 2.0.0-beta.1"],"main":function(depth0,helpers,partials,data) {
  var stack1, helper, functionType="function", helperMissing=helpers.helperMissing, escapeExpression=this.escapeExpression, buffer = "<div class=\"modal-dialog\">\n  <div class=\"modal-content\">\n    <div class=\"modal-header\">\n      <button type=\"button\" class=\"close\" data-dismiss=\"modal\" aria-hidden=\"true\">\n        <span aria-hidden=\"true\">&times;</span><span class=\"sr-only\">Close</span>\n      </button>\n";
  stack1 = helpers['if'].call(depth0, (depth0 != null ? depth0.trip_id : depth0), {"name":"if","hash":{},"fn":this.program(1, data),"inverse":this.program(3, data),"data":data});
  if (stack1 != null) { buffer += stack1; }
  buffer += "    </div>\n\n    <div class=\"modal-body\">\n      <form role=\"form\" >\n        <div class=\"form-group\">\n          <label for=\"trip_short_name\">trip_short_name</label>\n          <input class=\"form-control\" type=\"text\" name=\"trip_short_name\" placeholder=\"trip_short_name\" value=\""
    + escapeExpression(((helper = (helper = helpers.trip_short_name || (depth0 != null ? depth0.trip_short_name : depth0)) != null ? helper : helperMissing),(typeof helper === functionType ? helper.call(depth0, {"name":"trip_short_name","hash":{},"data":data}) : helper)))
    + "\">\n        </div>\n        <div class=\"form-group\">\n          <label for=\"route_id\">route_id</label>\n          <input class=\"form-control\" type=\"text\" name=\"route_id\" placeholder=\"route_id\" value=\""
    + escapeExpression(((helper = (helper = helpers.route_id || (depth0 != null ? depth0.route_id : depth0)) != null ? helper : helperMissing),(typeof helper === functionType ? helper.call(depth0, {"name":"route_id","hash":{},"data":data}) : helper)))
    + "\">\n        </div>\n        <div class=\"form-group\">\n          <label for=\"service_id\">service_id</label>\n            <input class=\"form-control\" type=\"text\" name=\"service_id\" placeholder=\"service_id\" value=\""
    + escapeExpression(((helper = (helper = helpers.service_id || (depth0 != null ? depth0.service_id : depth0)) != null ? helper : helperMissing),(typeof helper === functionType ? helper.call(depth0, {"name":"service_id","hash":{},"data":data}) : helper)))
    + "\">\n        </div>\n        <div class=\"form-group\">\n          <label for=\"shape_id\">shape_id</label>\n            <input class=\"form-control\" type=\"text\" name=\"shape_id\" placeholder=\"shape_id\" value=\""
    + escapeExpression(((helper = (helper = helpers.shape_id || (depth0 != null ? depth0.shape_id : depth0)) != null ? helper : helperMissing),(typeof helper === functionType ? helper.call(depth0, {"name":"shape_id","hash":{},"data":data}) : helper)))
    + "\">\n        </div>\n        <div class=\"form-group\">\n          <label for=\"trip_headsign\">trip_headsign</label>\n            <input class=\"form-control\" type=\"text\" name=\"trip_headsign\" placeholder=\"trip_headsign\" value=\""
    + escapeExpression(((helper = (helper = helpers.trip_headsign || (depth0 != null ? depth0.trip_headsign : depth0)) != null ? helper : helperMissing),(typeof helper === functionType ? helper.call(depth0, {"name":"trip_headsign","hash":{},"data":data}) : helper)))
    + "\">\n        </div>\n        <div class=\"form-group\">\n          <label for=\"direction_id\">direction_id</label>\n          <input class=\"form-control\" type=\"text\" name=\"direction_id\" placeholder=\"direction_id\" value=\""
    + escapeExpression(((helper = (helper = helpers.direction_id || (depth0 != null ? depth0.direction_id : depth0)) != null ? helper : helperMissing),(typeof helper === functionType ? helper.call(depth0, {"name":"direction_id","hash":{},"data":data}) : helper)))
    + "\">\n        </div>\n        <div class=\"form-group\">\n            <label>\n              <input type=\"checkbox\" ";
  stack1 = helpers['if'].call(depth0, (depth0 != null ? depth0.active : depth0), {"name":"if","hash":{},"fn":this.program(5, data),"inverse":this.noop,"data":data});
  if (stack1 != null) { buffer += stack1; }
  return buffer + "> Active\n            </label>\n        </div>\n      </form>\n    </div>\n\n    <div class=\"modal-footer\">\n      <button type=\"button\" class=\"btn btn-default\" data-dismiss=\"modal\">Close</button>\n      <button type=\"button\" class=\"btn btn-primary js-save\">Save changes</button>\n    </div>\n  </div>\n</div>\n";
},"useData":true});



this["JST"]["multipleStops"] = Handlebars.template({"1":function(depth0,helpers,partials,data) {
  var stack1, helper, functionType="function", helperMissing=helpers.helperMissing, escapeExpression=this.escapeExpression, buffer = "    <tr data-stop_id="
    + escapeExpression(((helper = (helper = helpers.fid || (depth0 != null ? depth0.fid : depth0)) != null ? helper : helperMissing),(typeof helper === functionType ? helper.call(depth0, {"name":"fid","hash":{},"data":data}) : helper)))
    + ">\n      <td><button class=\"btn btn-mini\" id=\""
    + escapeExpression(((helper = (helper = helpers.fid || (depth0 != null ? depth0.fid : depth0)) != null ? helper : helperMissing),(typeof helper === functionType ? helper.call(depth0, {"name":"fid","hash":{},"data":data}) : helper)))
    + "\"><i class=\"icon-forward\"></i></button>"
    + escapeExpression(((helper = (helper = helpers.fid || (depth0 != null ? depth0.fid : depth0)) != null ? helper : helperMissing),(typeof helper === functionType ? helper.call(depth0, {"name":"fid","hash":{},"data":data}) : helper)))
    + "</td>\n      <td>\n";
  stack1 = helpers.each.call(depth0, ((stack1 = (depth0 != null ? depth0.attributes : depth0)) != null ? stack1.stop_lineas : stack1), {"name":"each","hash":{},"fn":this.program(2, data),"inverse":this.noop,"data":data});
  if (stack1 != null) { buffer += stack1; }
  return buffer + "\n      </td>\n    </tr>\n";
},"2":function(depth0,helpers,partials,data) {
  var lambda=this.lambda, escapeExpression=this.escapeExpression;
  return "      <span>"
    + escapeExpression(lambda(depth0, depth0))
    + ", </span>";
},"compiler":[6,">= 2.0.0-beta.1"],"main":function(depth0,helpers,partials,data) {
  var stack1, buffer = "<h4>Selected Stops</h4>\n<table class=\"table table-hover table-condensed\">\n  <thead>\n  <tr>\n    <th>Stop-id</th>\n    <th>lineas</th>\n  </tr>\n  </thead>\n  <tbody>\n";
  stack1 = helpers.each.call(depth0, (depth0 != null ? depth0.features : depth0), {"name":"each","hash":{},"fn":this.program(1, data),"inverse":this.noop,"data":data});
  if (stack1 != null) { buffer += stack1; }
  return buffer + "  </tbody>\n</table>";
},"useData":true});



this["JST"]["navbar-right"] = Handlebars.template({"compiler":[6,">= 2.0.0-beta.1"],"main":function(depth0,helpers,partials,data) {
  return "<ul class=\"nav navbar-top-links navbar-right\">\n  <li class=\"dropdown\">\n    <a class=\"dropdown-toggle\" data-toggle=\"dropdown\" href=\"#\">\n      <i class=\"glyphicon glyphicon-envelope glyphicon-fw\"></i>  <i class=\"glyphicon glyphicon-caret-down\"></i>\n    </a>\n    <ul class=\"dropdown-menu dropdown-messages\">\n      <li>\n        <a href=\"#\">\n          <div>\n            <strong>John Smith</strong>\n            <span class=\"pull-right text-muted\">\n              <em>Yesterday</em>\n            </span>\n          </div>\n          <div>Lorem ipsum dolor sit amet, consectetur adipiscing elit. Pellentesque eleifend...</div>\n        </a>\n      </li>\n      <li class=\"divider\"></li>\n      <li>\n        <a href=\"#\">\n          <div>\n            <strong>John Smith</strong>\n            <span class=\"pull-right text-muted\">\n              <em>Yesterday</em>\n            </span>\n          </div>\n          <div>Lorem ipsum dolor sit amet, consectetur adipiscing elit. Pellentesque eleifend...</div>\n        </a>\n      </li>\n      <li class=\"divider\"></li>\n      <li>\n        <a href=\"#\">\n          <div>\n            <strong>John Smith</strong>\n            <span class=\"pull-right text-muted\">\n              <em>Yesterday</em>\n            </span>\n          </div>\n          <div>Lorem ipsum dolor sit amet, consectetur adipiscing elit. Pellentesque eleifend...</div>\n        </a>\n      </li>\n      <li class=\"divider\"></li>\n      <li>\n        <a class=\"text-center\" href=\"#\">\n          <strong>Read All Messages</strong>\n          <i class=\"fa fa-angle-right\"></i>\n        </a>\n      </li>\n    </ul>\n    <!-- /.dropdown-messages -->\n  </li>\n  <!-- /.dropdown -->\n  <li class=\"dropdown\">\n    <a class=\"dropdown-toggle\" data-toggle=\"dropdown\" href=\"#\">\n      <i class=\"glyphicon glyphicon-tasks glyphicon-fw\"></i>  <i class=\"glyphicon glyphicon-caret-down\"></i>\n    </a>\n    <ul class=\"dropdown-menu dropdown-tasks\">\n      <li>\n        <a href=\"#\">\n          <div>\n            <p>\n              <strong>Task 1</strong>\n              <span class=\"pull-right text-muted\">40% Complete</span>\n            </p>\n            <div class=\"progress progress-striped active\">\n              <div class=\"progress-bar progress-bar-success\" role=\"progressbar\" aria-valuenow=\"40\" aria-valuemin=\"0\" aria-valuemax=\"100\" style=\"width: 40%\">\n                <span class=\"sr-only\">40% Complete (success)</span>\n              </div>\n            </div>\n          </div>\n        </a>\n      </li>\n      <li class=\"divider\"></li>\n      <li>\n        <a href=\"#\">\n          <div>\n            <p>\n              <strong>Task 2</strong>\n              <span class=\"pull-right text-muted\">20% Complete</span>\n            </p>\n            <div class=\"progress progress-striped active\">\n              <div class=\"progress-bar progress-bar-info\" role=\"progressbar\" aria-valuenow=\"20\" aria-valuemin=\"0\" aria-valuemax=\"100\" style=\"width: 20%\">\n                <span class=\"sr-only\">20% Complete</span>\n              </div>\n            </div>\n          </div>\n        </a>\n      </li>\n      <li class=\"divider\"></li>\n      <li>\n        <a href=\"#\">\n          <div>\n            <p>\n              <strong>Task 3</strong>\n              <span class=\"pull-right text-muted\">60% Complete</span>\n            </p>\n            <div class=\"progress progress-striped active\">\n              <div class=\"progress-bar progress-bar-warning\" role=\"progressbar\" aria-valuenow=\"60\" aria-valuemin=\"0\" aria-valuemax=\"100\" style=\"width: 60%\">\n                <span class=\"sr-only\">60% Complete (warning)</span>\n              </div>\n            </div>\n          </div>\n        </a>\n      </li>\n      <li class=\"divider\"></li>\n      <li>\n        <a href=\"#\">\n          <div>\n            <p>\n              <strong>Task 4</strong>\n              <span class=\"pull-right text-muted\">80% Complete</span>\n            </p>\n            <div class=\"progress progress-striped active\">\n              <div class=\"progress-bar progress-bar-danger\" role=\"progressbar\" aria-valuenow=\"80\" aria-valuemin=\"0\" aria-valuemax=\"100\" style=\"width: 80%\">\n                <span class=\"sr-only\">80% Complete (danger)</span>\n              </div>\n            </div>\n          </div>\n        </a>\n      </li>\n      <li class=\"divider\"></li>\n      <li>\n        <a class=\"text-center\" href=\"#\">\n          <strong>See All Tasks</strong>\n          <i class=\"glyphicon glyphicon-angle-right\"></i>\n        </a>\n      </li>\n    </ul>\n    <!-- /.dropdown-tasks -->\n  </li>\n  <!-- /.dropdown -->\n  <li class=\"dropdown\">\n    <a class=\"dropdown-toggle\" data-toggle=\"dropdown\" href=\"#\">\n      <i class=\"glyphicon glyphicon-bell glyphicon-fw\"></i>  <i class=\"glyphicon glyphicon-caret-down\"></i>\n    </a>\n    <ul class=\"dropdown-menu dropdown-alerts\">\n      <li>\n        <a href=\"#\">\n          <div>\n            <i class=\"glyphicon glyphicon-comment glyphicon-fw\"></i> New Comment\n            <span class=\"pull-right text-muted small\">4 minutes ago</span>\n          </div>\n        </a>\n      </li>\n      <li class=\"divider\"></li>\n      <li>\n        <a href=\"#\">\n          <div>\n            <i class=\"glyphicon glyphicon-twitter glyphicon-fw\"></i> 3 New Followers\n            <span class=\"pull-right text-muted small\">12 minutes ago</span>\n          </div>\n        </a>\n      </li>\n      <li class=\"divider\"></li>\n      <li>\n        <a href=\"#\">\n          <div>\n            <i class=\"glyphicon glyphicon-envelope glyphicon-fw\"></i> Message Sent\n            <span class=\"pull-right text-muted small\">4 minutes ago</span>\n          </div>\n        </a>\n      </li>\n      <li class=\"divider\"></li>\n      <li>\n        <a href=\"#\">\n          <div>\n            <i class=\"glyphicon glyphicon-tasks glyphicon-fw\"></i> New Task\n            <span class=\"pull-right text-muted small\">4 minutes ago</span>\n          </div>\n        </a>\n      </li>\n      <li class=\"divider\"></li>\n      <li>\n        <a href=\"#\">\n          <div>\n            <i class=\"glyphicon glyphicon-upload glyphicon-fw\"></i> Server Rebooted\n            <span class=\"pull-right text-muted small\">4 minutes ago</span>\n          </div>\n        </a>\n      </li>\n      <li class=\"divider\"></li>\n      <li>\n        <a class=\"text-center\" href=\"#\">\n          <strong>See All Alerts</strong>\n          <i class=\"glyphicon glyphicon-angle-right\"></i>\n        </a>\n      </li>\n    </ul>\n    <!-- /.dropdown-alerts -->\n  </li>\n  <!-- /.dropdown -->\n  <li class=\"dropdown\">\n    <a class=\"dropdown-toggle\" data-toggle=\"dropdown\" href=\"#\">\n      <i class=\"glyphicon glyphicon-user glyphicon-fw\"></i>  <i class=\"glyphicon glyphicon-caret-down\"></i>\n    </a>\n    <ul class=\"dropdown-menu dropdown-user\">\n      <li><a href=\"#\"><i class=\"glyphicon glyphicon-user glyphicon-fw\"></i> User Profile</a>\n      </li>\n      <li><a href=\"#\"><i class=\"glyphicon glyphicon-gear glyphicon-fw\"></i> Settings</a>\n      </li>\n      <li class=\"divider\"></li>\n      <li><a href=\"login.html\"><i class=\"glyphicon glyphicon-sign-out glyphicon-fw\"></i> Logout</a>\n      </li>\n    </ul>\n    <!-- /.dropdown-user -->\n  </li>\n  <!-- /.dropdown -->\n</ul>";
  },"useData":true});



this["JST"]["navbarRight"] = Handlebars.template({"compiler":[6,">= 2.0.0-beta.1"],"main":function(depth0,helpers,partials,data) {
  return "<ul class=\"nav navbar-top-links navbar-right\">\n    <li>\n        <a href=\"#/agencies\">\n            <i class=\"glyphicon glyphicon-road\"><span class=\"hidden-sm\"> Agencies</span></i>\n        </a>\n    </li>\n\n    <li>\n        <a href=\"#stops\">\n            <i class=\"glyphicon glyphicon-record\"><span class=\"hidden-sm\"> Stops</span></i>\n        </a>\n    </li>\n\n    <li>\n        <a href=\"#/routes\">\n            <i class=\"glyphicon glyphicon-road\"><span class=\"hidden-sm\"> Routes</span></i>\n        </a>\n    </li>\n\n    <li>\n        <a href=\"#/calendar\">\n            <i class=\"glyphicon glyphicon-calendar\"><span class=\"hidden-sm\"> Calendar</span></i>\n        </a>\n    </li>\n\n\n    <!-- /.dropdown -->\n    <li class=\"dropdown\">\n        <a class=\"dropdown-toggle\" data-toggle=\"dropdown\" href=\"#\">\n            <i class=\"glyphicon glyphicon-cog\"></i><span class=\"hidden-sm\"> Feed</span><i class=\"caret\"></i>\n        </a>\n        <ul class=\"dropdown-menu dropdown-user\">\n<!--             <li><a href=\"#\"><i class=\"glyphicon glyphicon-user glyphicon-fw\"></i> User Profile</a>\n            </li>\n            <li><a href=\"#\"><i class=\"glyphicon glyphicon-gear glyphicon-fw\"></i> Settings</a>\n            </li>\n            <li class=\"divider\"></li>\n            <li><a href=\"login.html\"><i class=\"glyphicon glyphicon-sign-out glyphicon-fw\"></i> Logout</a>\n            </li> -->\n            <li><a href=\"/api/feed/google_transit.zip\" target=\"_blank\"><i class=\"glyphicon glyphicon-download-alt\"></i> Download Feed</a>\n            </li>\n        </ul>\n        <!-- /.dropdown-user -->\n    </li>\n    <!-- /.dropdown -->\n    <!-- /.dropdown -->\n    <li class=\"dropdown\">\n        <a class=\"dropdown-toggle\" data-toggle=\"dropdown\" href=\"#\">\n          <i class=\"glyphicon glyphicon-user glyphicon-fw\"></i>  <i class=\"glyphicon glyphicon-caret-down\"></i>\n        </a>\n        <ul class=\"dropdown-menu dropdown-user\">\n          <li><a href=\"/auth/logout\"><i class=\"glyphicon glyphicon-sign-out glyphicon-fw\"></i> Logout</a>\n          </li>\n        </ul>\n        <!-- /.dropdown-user -->\n    </li>\n</ul>\n<!-- /.navbar-top-links -->\n";
},"useData":true});



this["JST"]["routes"] = Handlebars.template({"compiler":[6,">= 2.0.0-beta.1"],"main":function(depth0,helpers,partials,data) {
  return "<div class=\"col-md-4 panel-left\">\n<h4>Filters</h4>\n  <div class=\"row\">\n    <div class=\"col-md-12 routes-select\">\n    </div>\n  </div>\n  <div class=\"row\">\n    <div class=\"col-md-12 trips-select\">\n    </div>\n  </div>\n  <div class=\"shapes-toolbox\"></div>\n  <div class=\"sequence-toolbox\"></div>\n</div>\n\n<div class=\"col-md-8 panel-right\">\n  <div role=\"tabpanel\">\n\n    <!-- Nav tabs -->\n    <ul class=\"nav nav-tabs\" role=\"tablist\">\n      <li role=\"presentation\" class=\"active\"><a href=\"#map-tab\" aria-controls=\"map-tab\" role=\"tab\" data-toggle=\"tab\">Map</a></li>\n      <li role=\"presentation\"><a href=\"#sequence-tab\" aria-controls=\"sequence-tab\" role=\"tab\" data-toggle=\"tab\">Sequence times</a></li>\n      <li role=\"presentation\"><a href=\"#start-times-tab\" aria-controls=\"start-times-tab\" role=\"tab\" data-toggle=\"tab\">Start times</a></li>\n    </ul>\n\n    <!-- Tab panes -->\n    <div class=\"tab-content\">\n      <div role=\"tabpanel\" class=\"tab-pane active\" id=\"map-tab\">\n        <div id=\"map\" class=\"map-view\"></div>\n      </div>\n      <div role=\"tabpanel\" class=\"tab-pane\" id=\"sequence-tab\">\n        <div class=\"sequence-view\"></div>\n      </div>\n      <div role=\"tabpanel\" class=\"tab-pane\" id=\"start-times-tab\">\n        <div class=\"row voffset1\">\n          <div class=\"col-md-6\">\n            <div class=\"calendars-select-view\"></div>\n            <div class=\"calendars-tools-view\"></div>\n          </div>\n          <div class=\"col-md-6 start-times-view\"></div>\n        </div>\n      </div>\n    </div>\n\n  </div>\n\n</div>";
  },"useData":true});



this["JST"]["routesSelect"] = Handlebars.template({"1":function(depth0,helpers,partials,data) {
  var helper, functionType="function", helperMissing=helpers.helperMissing, escapeExpression=this.escapeExpression;
  return "          <option value=\""
    + escapeExpression(((helper = (helper = helpers.route_id || (depth0 != null ? depth0.route_id : depth0)) != null ? helper : helperMissing),(typeof helper === functionType ? helper.call(depth0, {"name":"route_id","hash":{},"data":data}) : helper)))
    + "\">"
    + escapeExpression(((helper = (helper = helpers.route_type || (depth0 != null ? depth0.route_type : depth0)) != null ? helper : helperMissing),(typeof helper === functionType ? helper.call(depth0, {"name":"route_type","hash":{},"data":data}) : helper)))
    + " "
    + escapeExpression(((helper = (helper = helpers.route_short_name || (depth0 != null ? depth0.route_short_name : depth0)) != null ? helper : helperMissing),(typeof helper === functionType ? helper.call(depth0, {"name":"route_short_name","hash":{},"data":data}) : helper)))
    + "</option>\n";
},"compiler":[6,">= 2.0.0-beta.1"],"main":function(depth0,helpers,partials,data) {
  var stack1, buffer = "<form class=\"form-horizontal\" role=\"form\">\n  <div class=\"form-group\">\n    <label for=\"route\" class=\"col-sm-2 control-label\">Route</label>\n    <div class=\"col-sm-8\">\n      <select class=\"form-control\" id=\"route\">\n        <option value=\"\"> -- </option>\n";
  stack1 = helpers.each.call(depth0, (depth0 != null ? depth0.routes : depth0), {"name":"each","hash":{},"fn":this.program(1, data),"inverse":this.noop,"data":data});
  if (stack1 != null) { buffer += stack1; }
  return buffer + "      </select>\n    </div>\n    <div class=\"col-sm-2\">\n      <div class=\"btn-group\">\n        <button class=\"btn btn-default dropdown-toggle\" type=\"button\" data-toggle=\"dropdown\">\n          <i class=\"glyphicon glyphicon-pencil\"></i>\n        </button>\n        <ul class=\"dropdown-menu dropdown-menu-right\" role=\"menu\" aria-labelledby=\"dropdownMenu1\">\n          <li class=\"js-add\" role=\"presentation\">\n            <a role=\"menuitem\" tabindex=\"-1\" href=\"#\"><i class=\"glyphicon glyphicon-plus\"></i> Add</a>\n          </li>\n          <li class=\"js-edit\" role=\"presentation\">\n            <a role=\"menuitem\" tabindex=\"-1\" href=\"#\" data-target=\"#routeEditData\" data-toggle=\"modal\">\n             <i class=\"glyphicon glyphicon-pencil\"></i> Edit\n            </a>\n          </li>\n          <li class=\"js-remove\" role=\"presentation\">\n            <a role=\"menuitem\" tabindex=\"-1\" href=\"#\"><i class=\"glyphicon glyphicon-trash\"></i> Delete</a>\n          </li>\n          <li role=\"presentation\" class=\"divider\"></li>\n          <li class=\"js-view-all disabled\"  role=\"presentation\">\n            <a role=\"menuitem\" tabindex=\"-1\" href=\"#\">View all</a>\n          </li>\n        </ul>\n      </div>\n    </div>\n  </div>\n</form>\n";
},"useData":true});



this["JST"]["schedule"] = Handlebars.template({"1":function(depth0,helpers,partials,data) {
  var helper, functionType="function", helperMissing=helpers.helperMissing, escapeExpression=this.escapeExpression;
  return "    <p>Desde: "
    + escapeExpression(((helper = (helper = helpers.desde || (depth0 != null ? depth0.desde : depth0)) != null ? helper : helperMissing),(typeof helper === functionType ? helper.call(depth0, {"name":"desde","hash":{},"data":data}) : helper)))
    + " hasta: "
    + escapeExpression(((helper = (helper = helpers.hasta || (depth0 != null ? depth0.hasta : depth0)) != null ? helper : helperMissing),(typeof helper === functionType ? helper.call(depth0, {"name":"hasta","hash":{},"data":data}) : helper)))
    + " cada "
    + escapeExpression(((helper = (helper = helpers.frecuencia || (depth0 != null ? depth0.frecuencia : depth0)) != null ? helper : helperMissing),(typeof helper === functionType ? helper.call(depth0, {"name":"frecuencia","hash":{},"data":data}) : helper)))
    + " minutos</p>\n";
},"compiler":[6,">= 2.0.0-beta.1"],"main":function(depth0,helpers,partials,data) {
  var stack1, buffer = "<div class=\"tabbable tabs-left\">\n  <ul class=\"nav nav-tabs\">\n  <li class=\"active\"><a href=\"#lav\" data-toggle=\"tab\">Lunes a Viernes</a></li>\n  <li><a href=\"#sabado\" data-toggle=\"tab\">Sábados</a></li>\n  <li><a href=\"#domingo\" data-toggle=\"tab\">Domingos y Feriados</a></li>\n  </ul>\n  <div class=\"tab-content\">\n  <div class=\"tab-pane active\" id=\"lav\">\n";
  stack1 = helpers.each.call(depth0, (depth0 != null ? depth0.lav : depth0), {"name":"each","hash":{},"fn":this.program(1, data),"inverse":this.noop,"data":data});
  if (stack1 != null) { buffer += stack1; }
  buffer += "  </div>\n  <div class=\"tab-pane\" id=\"sabado\">\n";
  stack1 = helpers.each.call(depth0, (depth0 != null ? depth0.sabado : depth0), {"name":"each","hash":{},"fn":this.program(1, data),"inverse":this.noop,"data":data});
  if (stack1 != null) { buffer += stack1; }
  buffer += "  </div>\n  <div class=\"tab-pane\" id=\"domingo\">\n";
  stack1 = helpers.each.call(depth0, (depth0 != null ? depth0.domingo : depth0), {"name":"each","hash":{},"fn":this.program(1, data),"inverse":this.noop,"data":data});
  if (stack1 != null) { buffer += stack1; }
  return buffer + "  </div>\n  </div>\n</div>";
},"useData":true});



this["JST"]["sequence"] = Handlebars.template({"1":function(depth0,helpers,partials,data) {
  var stack1, helper, functionType="function", helperMissing=helpers.helperMissing, escapeExpression=this.escapeExpression, lambda=this.lambda;
  return "		<tr data-stop-id=\""
    + escapeExpression(((helper = (helper = helpers.stop_id || (depth0 != null ? depth0.stop_id : depth0)) != null ? helper : helperMissing),(typeof helper === functionType ? helper.call(depth0, {"name":"stop_id","hash":{},"data":data}) : helper)))
    + "\" draggable=\"true\">\n			<td>"
    + escapeExpression(((helper = (helper = helpers.stop_sequence || (depth0 != null ? depth0.stop_sequence : depth0)) != null ? helper : helperMissing),(typeof helper === functionType ? helper.call(depth0, {"name":"stop_sequence","hash":{},"data":data}) : helper)))
    + "</td>\n			<td>"
    + escapeExpression(lambda(((stack1 = (depth0 != null ? depth0._stop : depth0)) != null ? stack1.stop_code : stack1), depth0))
    + "</td>\n			<td class=\"stop-time\" contenteditable=\"true\">"
    + escapeExpression(((helper = (helper = helpers.stop_time || (depth0 != null ? depth0.stop_time : depth0)) != null ? helper : helperMissing),(typeof helper === functionType ? helper.call(depth0, {"name":"stop_time","hash":{},"data":data}) : helper)))
    + "</td>\n			<td>"
    + escapeExpression(((helper = (helper = helpers.shape_dist_traveled || (depth0 != null ? depth0.shape_dist_traveled : depth0)) != null ? helper : helperMissing),(typeof helper === functionType ? helper.call(depth0, {"name":"shape_dist_traveled","hash":{},"data":data}) : helper)))
    + "</td>\n			<td>"
    + escapeExpression(((helper = (helper = helpers.speed || (depth0 != null ? depth0.speed : depth0)) != null ? helper : helperMissing),(typeof helper === functionType ? helper.call(depth0, {"name":"speed","hash":{},"data":data}) : helper)))
    + "</td>\n		</tr>\n";
},"compiler":[6,">= 2.0.0-beta.1"],"main":function(depth0,helpers,partials,data) {
  var stack1, buffer = "<div class=\"row voffset1\">\n  <div class=\"col-md-12\">\n	<table class=\"table table-hover table-condensed\">\n	<thead>\n		<tr>\n			<th>N</th><th>Stop Code</th><th>Time</th><th>Distance (km)</th><th>Speed (km/h)</th>\n		</tr>\n	</thead>\n	<tbody>\n";
  stack1 = helpers.each.call(depth0, depth0, {"name":"each","hash":{},"fn":this.program(1, data),"inverse":this.noop,"data":data});
  if (stack1 != null) { buffer += stack1; }
  return buffer + "	</tbody>\n	</table>\n  </div>\n</div>";
},"useData":true});



this["JST"]["sequenceToolbox"] = Handlebars.template({"compiler":[6,">= 2.0.0-beta.1"],"main":function(depth0,helpers,partials,data) {
  return "<h4>Trip Tools</h4>\n<div class=\"btn-toolbar\" role=\"toolbar\">\n  <div class=\"btn-group btn-group-sm\">\n    <button class=\"btn btn-default sortStops\">Sort</button>\n    <button class=\"btn btn-default offsetStops\">Align</button>\n    <button class=\"btn btn-default updateDist\">Update Distances</button>\n    <button class=\"btn btn-default interpolateTimes\">Interpolate Times</button>\n  </div>\n</div>\n\n<div class=\"row voffset1\">\n  <div class=\"col-md-12\">\n    <div class=\"btn-toolbar\" role=\"toolbar\">\n      <div class=\"btn-group btn-group-sm\">\n        <button class=\"btn btn-default prevStop\"><i class=\"glyphicon glyphicon-step-backward\"></i></button>\n        <button class=\"btn btn-default nextStop\"><i class=\"glyphicon glyphicon-step-forward\"></i></button>\n        <button class=\"btn btn-default removeStop\"><i class=\"glyphicon glyphicon-trash\"></i> Remove</button>\n        <button class=\"btn btn-default appendStop\"><i class=\"glyphicon glyphicon-chevron-down\"></i> Use</button>\n        <button class=\"btn btn-default btn-save\"><i class=\"glyphicon glyphicon-ok\"></i> Save</button>\n      </div>\n    </div>\n  </div>\n</div>\n\n<div class=\"row voffset1\">\n  <div class=\"col-md-12\">\n  <form class=\"form-inline\">\n    <div class=\"form-group\">\n      <label for=\"speed\">Set Speed</label>\n    <input name=\"speed\" type=\"number\" class=\"form-control speed\" placeholder=\"speed (km/h)\">\n    </div>\n    <button type=\"submit\" class=\"btn btn-default btn-speed\">Set</button>\n  </form>\n  </div>\n</div>\n\n<div class=\"row voffset1\">\n  <div class=\"col-md-12\">\n  <form class=\"form-inline\">\n    <div class=\"form-group\">\n      <label for=\"add-stops\">Add stops</label>\n    <input name=\"add-stops\" type=\"text\" class=\"form-control add-stops\" placeholder=\"id_1, id_2, ...\">\n    </div>\n    <button type=\"submit\" class=\"btn btn-default btn-add-stops\">Add</button>\n  </form>\n  </div>\n</div>\n";
  },"useData":true});



this["JST"]["shapesToolbox"] = Handlebars.template({"compiler":[6,">= 2.0.0-beta.1"],"main":function(depth0,helpers,partials,data) {
  return "<h4>Shape Tools</h4>\n<div class=\"btn-toolbar\" role=\"toolbar\">\n  <div class=\"btn-group btn-group-sm\">\n    <button class=\"btn btn-default create-shape\">\n      <i class=\"glyphicon glyphicon-plus\"></i> Create\n    </button>\n    <button class=\"btn btn-default reverseShape\">\n      <i class=\"glyphicon glyphicon-refresh\"></i> Reverse\n    </button>\n    <button class=\"btn btn-default editShape\">\n      <i class=\"glyphicon glyphicon-pencil\"></i> Edit\n    </button>\n    <button class=\"btn btn-default saveShape\">\n      <i class=\"glyphicon glyphicon-ok\"></i> Save\n    </button>\n    <button class=\"btn btn-default delete\">\n      <i class=\"glyphicon glyphicon-trash\"></i> Delete\n    </button>\n  </div>\n</div>";
  },"useData":true});



this["JST"]["startTimes"] = Handlebars.template({"1":function(depth0,helpers,partials,data) {
  return "<div class=\"alert alert-info\" role=\"alert\">There are unsaved changes</div>\n";
  },"3":function(depth0,helpers,partials,data) {
  return "<div class=\"alert alert-danger\" role=\"alert\">There are formating errors</div>\n";
  },"5":function(depth0,helpers,partials,data) {
  var stack1, helper, lambda=this.lambda, escapeExpression=this.escapeExpression, functionType="function", helperMissing=helpers.helperMissing, buffer = "    <tr data-index=\""
    + escapeExpression(lambda((data && data.index), depth0))
    + "\" class=\"";
  stack1 = helpers.unless.call(depth0, (depth0 != null ? depth0.isValid : depth0), {"name":"unless","hash":{},"fn":this.program(6, data),"inverse":this.noop,"data":data});
  if (stack1 != null) { buffer += stack1; }
  return buffer + "\">\n      <td><input class=\"form-control\" data-attr=\"start_time\" type=\"text\" value=\""
    + escapeExpression(((helper = (helper = helpers.start_time || (depth0 != null ? depth0.start_time : depth0)) != null ? helper : helperMissing),(typeof helper === functionType ? helper.call(depth0, {"name":"start_time","hash":{},"data":data}) : helper)))
    + "\"/></td>\n      <td><button class=\"btn btn-default btn-rm\"><span class=\"glyphicon glyphicon-remove\"></span></button></td>\n    </tr>\n";
},"6":function(depth0,helpers,partials,data) {
  return "danger";
  },"compiler":[6,">= 2.0.0-beta.1"],"main":function(depth0,helpers,partials,data) {
  var stack1, buffer = "";
  stack1 = helpers['if'].call(depth0, (depth0 != null ? depth0.isDirty : depth0), {"name":"if","hash":{},"fn":this.program(1, data),"inverse":this.noop,"data":data});
  if (stack1 != null) { buffer += stack1; }
  stack1 = helpers['if'].call(depth0, (depth0 != null ? depth0.hasErrors : depth0), {"name":"if","hash":{},"fn":this.program(3, data),"inverse":this.noop,"data":data});
  if (stack1 != null) { buffer += stack1; }
  buffer += "\n<table class=\"table table-hover table-condensed table-editable\">\n  <thead>\n    <tr>\n      <th class=\"col-sm-11\">Time</th>\n      <th class=\"col-sm-1\"></th>\n    </tr>\n  </thead>\n  <tbody>\n";
  stack1 = helpers.each.call(depth0, (depth0 != null ? depth0.models : depth0), {"name":"each","hash":{},"fn":this.program(5, data),"inverse":this.noop,"data":data});
  if (stack1 != null) { buffer += stack1; }
  return buffer + "  </tbody>\n</table>\n";
},"useData":true});



this["JST"]["stopData"] = Handlebars.template({"1":function(depth0,helpers,partials,data) {
  var stack1, helper, functionType="function", helperMissing=helpers.helperMissing, escapeExpression=this.escapeExpression, buffer = "        <li>Route "
    + escapeExpression(((helper = (helper = helpers.route_id || (depth0 != null ? depth0.route_id : depth0)) != null ? helper : helperMissing),(typeof helper === functionType ? helper.call(depth0, {"name":"route_id","hash":{},"data":data}) : helper)))
    + ", Trip to: "
    + escapeExpression(((helper = (helper = helpers.trip_headsign || (depth0 != null ? depth0.trip_headsign : depth0)) != null ? helper : helperMissing),(typeof helper === functionType ? helper.call(depth0, {"name":"trip_headsign","hash":{},"data":data}) : helper)))
    + ", ";
  stack1 = helpers['if'].call(depth0, (depth0 != null ? depth0.card_code : depth0), {"name":"if","hash":{},"fn":this.program(2, data),"inverse":this.noop,"data":data});
  if (stack1 != null) { buffer += stack1; }
  buffer += "\n            ";
  stack1 = ((helpers.if_eq || (depth0 && depth0.if_eq) || helperMissing).call(depth0, (depth0 != null ? depth0.direction_id : depth0), "0", {"name":"if_eq","hash":{},"fn":this.program(4, data),"inverse":this.program(6, data),"data":data}));
  if (stack1 != null) { buffer += stack1; }
  return buffer + "</li>\n";
},"2":function(depth0,helpers,partials,data) {
  var helper, functionType="function", helperMissing=helpers.helperMissing, escapeExpression=this.escapeExpression;
  return "("
    + escapeExpression(((helper = (helper = helpers.card_code || (depth0 != null ? depth0.card_code : depth0)) != null ? helper : helperMissing),(typeof helper === functionType ? helper.call(depth0, {"name":"card_code","hash":{},"data":data}) : helper)))
    + ")";
},"4":function(depth0,helpers,partials,data) {
  return "(ida)";
  },"6":function(depth0,helpers,partials,data) {
  return "(vuelta)";
  },"compiler":[6,">= 2.0.0-beta.1"],"main":function(depth0,helpers,partials,data) {
  var stack1, lambda=this.lambda, escapeExpression=this.escapeExpression, buffer = "<div class=\"row\">\n  <div class=\"col-sm-12\">\n  <dl class=\"dl-horizontal\">\n    <dt>Stop code</dt>\n    <dd>"
    + escapeExpression(lambda(((stack1 = (depth0 != null ? depth0.stop : depth0)) != null ? stack1.stop_code : stack1), depth0))
    + "</dd>\n    <dt>Nombre</dt>\n    <dd>"
    + escapeExpression(lambda(((stack1 = (depth0 != null ? depth0.stop : depth0)) != null ? stack1.stop_name : stack1), depth0))
    + "</dd>\n    <dt>Calle</dt>\n    <dd>"
    + escapeExpression(lambda(((stack1 = (depth0 != null ? depth0.stop : depth0)) != null ? stack1.stop_calle : stack1), depth0))
    + "</dd>\n    <dt>Numero</dt>\n    <dd>"
    + escapeExpression(lambda(((stack1 = (depth0 != null ? depth0.stop : depth0)) != null ? stack1.stop_numero : stack1), depth0))
    + "</dd>\n    <dt>Esquina</dt>\n    <dd>"
    + escapeExpression(lambda(((stack1 = (depth0 != null ? depth0.stop : depth0)) != null ? stack1.stop_esquina : stack1), depth0))
    + "</dd>\n    <dt>Entre</dt>\n    <dd>"
    + escapeExpression(lambda(((stack1 = (depth0 != null ? depth0.stop : depth0)) != null ? stack1.stop_entre : stack1), depth0))
    + "</dd>\n    <dt>Descripcion</dt>\n    <dd>"
    + escapeExpression(lambda(((stack1 = (depth0 != null ? depth0.stop : depth0)) != null ? stack1.stop_desc : stack1), depth0))
    + "</dd>\n    <dt>Latitud</dt>\n    <dd>"
    + escapeExpression(lambda(((stack1 = (depth0 != null ? depth0.stop : depth0)) != null ? stack1.stop_lat : stack1), depth0))
    + "</dd>\n    <dt>Longitud</dt>\n    <dd>"
    + escapeExpression(lambda(((stack1 = (depth0 != null ? depth0.stop : depth0)) != null ? stack1.stop_lon : stack1), depth0))
    + "</dd>\n  </dl>\n  </div>\n</div>\n<div class=\"row\">\n  <div class=\"col-md-12\">\n    <button class=\"btn btn-default show-trips\">Show Trips</button>\n    <ul>\n";
  stack1 = helpers.each.call(depth0, (depth0 != null ? depth0.trips : depth0), {"name":"each","hash":{},"fn":this.program(1, data),"inverse":this.noop,"data":data});
  if (stack1 != null) { buffer += stack1; }
  return buffer + "    </ul>\n  </div>\n</div>";
},"useData":true});



this["JST"]["stopToolbar"] = Handlebars.template({"compiler":[6,">= 2.0.0-beta.1"],"main":function(depth0,helpers,partials,data) {
  return "<div class=\"btn-toolbar\" role=\"toolbar\">\n  <div class=\"btn-group btn-group-md toolbar-edit\">\n    <button class=\"btn btn-default create-stop\"><i class=\"glyphicon glyphicon-plus\"></i> New</button>\n    <button class=\"btn btn-default edit-stop\"><i class=\"glyphicon glyphicon-pencil\"></i> Edit</button>\n    <button class=\"btn btn-default move-stop\"><i class=\"glyphicon glyphicon-move\"></i> Move</button>\n    <button class=\"btn btn-default rm-stop\"><i class=\"glyphicon glyphicon-trash\"></i> Delete</button>\n  </div>\n  <div class=\"btn-group btn-group-md toolbar-commit hidden\">\n    <button class=\"btn btn-default save-stop\"><i class=\"glyphicon glyphicon-save\"></i> Save</button>\n    <button class=\"btn btn-default edit-stop\"><i class=\"glyphicon glyphicon-pencil\"></i> Edit</button>\n    <button class=\"btn btn-default cancel-edit\"><i class=\"glyphicon glyphicon-remove\"></i> Cancel</button>\n  </div>\n</div>";
  },"useData":true});



this["JST"]["stops"] = Handlebars.template({"compiler":[6,">= 2.0.0-beta.1"],"main":function(depth0,helpers,partials,data) {
  return "<div class=\"col-md-4 panel-left\">\n  <div class=\"row\">\n    <div class=\"col-md-12 top-sp filter-view\"></div>\n  </div>\n  <div class=\"stop-toolbar-view\"></div>\n  <h4>Stop Data</h4>\n  <div class=\"stop-data-view\"></div>\n</div>\n<div class=\"col-md-8 panel-right\">\n  <div id=\"map\" class=\"map-view\"></div>\n</div>";
  },"useData":true});



this["JST"]["tripsSelect"] = Handlebars.template({"1":function(depth0,helpers,partials,data) {
  var stack1, helper, functionType="function", helperMissing=helpers.helperMissing, escapeExpression=this.escapeExpression, buffer = "          <option value=\""
    + escapeExpression(((helper = (helper = helpers.trip_id || (depth0 != null ? depth0.trip_id : depth0)) != null ? helper : helperMissing),(typeof helper === functionType ? helper.call(depth0, {"name":"trip_id","hash":{},"data":data}) : helper)))
    + "\">\n            ";
  stack1 = helpers['if'].call(depth0, (depth0 != null ? depth0.card_code : depth0), {"name":"if","hash":{},"fn":this.program(2, data),"inverse":this.noop,"data":data});
  if (stack1 != null) { buffer += stack1; }
  buffer += "\n            ";
  stack1 = ((helpers.if_eq || (depth0 && depth0.if_eq) || helperMissing).call(depth0, (depth0 != null ? depth0.direction_id : depth0), "0", {"name":"if_eq","hash":{},"fn":this.program(4, data),"inverse":this.program(6, data),"data":data}));
  if (stack1 != null) { buffer += stack1; }
  return buffer + "\n            To: "
    + escapeExpression(((helper = (helper = helpers.trip_headsign || (depth0 != null ? depth0.trip_headsign : depth0)) != null ? helper : helperMissing),(typeof helper === functionType ? helper.call(depth0, {"name":"trip_headsign","hash":{},"data":data}) : helper)))
    + "\n            </option>\n";
},"2":function(depth0,helpers,partials,data) {
  var helper, functionType="function", helperMissing=helpers.helperMissing, escapeExpression=this.escapeExpression;
  return "("
    + escapeExpression(((helper = (helper = helpers.card_code || (depth0 != null ? depth0.card_code : depth0)) != null ? helper : helperMissing),(typeof helper === functionType ? helper.call(depth0, {"name":"card_code","hash":{},"data":data}) : helper)))
    + ")";
},"4":function(depth0,helpers,partials,data) {
  return "(ida)";
  },"6":function(depth0,helpers,partials,data) {
  return "(vuelta)";
  },"compiler":[6,">= 2.0.0-beta.1"],"main":function(depth0,helpers,partials,data) {
  var stack1, buffer = "<form class=\"form-horizontal\" role=\"form\">\n  <div class=\"form-group\">\n    <label for=\"route\" class=\"col-sm-2 control-label\">Trip</label>\n    <div class=\"col-sm-8\">\n      <select class=\"form-control\">\n        <option value=\"\"> -- </option>\n";
  stack1 = helpers.each.call(depth0, (depth0 != null ? depth0.trips : depth0), {"name":"each","hash":{},"fn":this.program(1, data),"inverse":this.noop,"data":data});
  if (stack1 != null) { buffer += stack1; }
  return buffer + "      </select>\n    </div>\n    <div class=\"col-sm-2\">\n      <div class=\"btn-group\">\n        <button class=\"btn btn-default dropdown-toggle\" type=\"button\" data-toggle=\"dropdown\">\n          <i class=\"glyphicon glyphicon-pencil\"></i>\n        </button>\n        <ul class=\"dropdown-menu dropdown-menu-right\" role=\"menu\" aria-labelledby=\"dropdownMenu1\">\n          <li class=\"js-add\" role=\"presentation\">\n            <a role=\"menuitem\" tabindex=\"-1\" href=\"#\"><i class=\"glyphicon glyphicon-plus\"></i> Add</a>\n          </li>\n          <li class=\"js-edit\" role=\"presentation\">\n            <a role=\"menuitem\" tabindex=\"-1\" href=\"#\" data-target=\"#routeEditData\" data-toggle=\"modal\">\n             <i class=\"glyphicon glyphicon-pencil\"></i> Edit\n            </a>\n          </li>\n          <li class=\"js-remove\" role=\"presentation\">\n            <a role=\"menuitem\" tabindex=\"-1\" href=\"#\"><i class=\"glyphicon glyphicon-trash\"></i> Delete</a>\n          </li>\n          <li role=\"presentation\" class=\"divider\"></li>\n          <li class=\"js-view-all disabled\"  role=\"presentation\">\n            <a role=\"menuitem\" tabindex=\"-1\" href=\"#\">View all</a>\n          </li>\n        </ul>\n      </div>\n    </div>\n  </div>\n</form>\n";
},"useData":true});

return this["JST"];

});