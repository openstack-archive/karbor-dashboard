/*
 * jQuery Smaug Function
 */

(function ($) {

  /* add warning span */
  function add_warning_span(cur_node) {
    var warning_span = $(cur_node).has("span.help-block");
    if( warning_span.length == 0) {
      var warning_info = $("<span/>").addClass("help-block")
          .html("This field is required");
      cur_node.append(warning_info);
    }
    $(cur_node).closest(".form-group.required").addClass("has-error");
  }

  /* remove warning span */
  function remove_warning_span(cur_node) {
    var warning_spans = $(cur_node).has("span.help-block");
    if( warning_spans.length > 0) {
      warning_spans.each(function(){
        $(this).children("span").remove();
      });
    }
    $(cur_node).closest(".form-group.required").removeClass("has-error");
  }

  $.Smaug = {

    /* get the default resources parameters */
    getResourceDefaultParameters: function(provider, schemaname) {
      var parameters = {};
      if(provider != null) {
        if(provider.extended_info_schema != null) {
          var result = provider.extended_info_schema[schemaname];
          for(var r in result) {
            parameters[r] = {};
            var schema = result[r];
            if(schema!=null) {
              for(var p in schema.properties) {
                var property = schema.properties[p];
                if(property.hasOwnProperty("default")) {
                  parameters[r][p] = property.default;
                }
              }
            }
          }
        }
      }
      return parameters;
    },

    /* check html control required */
    check_required: function(div_id){
      var flag = true;
      var required_node = div_id.find(".form-group.required").find(".form-control");
      for(var i = 0; i<required_node.length; i++) {
        var cur_node = required_node[i];
        var parent_node = $(cur_node).closest("div");
        var node_value = eval(cur_node).value;
        if(node_value == "" || node_value == null)
        {
          add_warning_span(parent_node);
          flag = false;
        }
        else
        {
          remove_warning_span(parent_node);
        }
      }
      return flag;
    }
  };
})(jQuery);
