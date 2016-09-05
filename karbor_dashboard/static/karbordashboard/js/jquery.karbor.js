/*
 * jQuery Karbor Function
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

   /* create dynamic field */
  function createDynamicField(schema, userdata, modal_body) {
    if(schema!=null) {
      for(var p in schema.properties) {
        var property = schema.properties[p];
        /* confirm whether the field is required */
        var required = false;
        if($.inArray(p, schema.required) >= 0) {
          required = true;
        }

        /* form group */
        var form_group = $("<div/>").addClass("form-group");
        if(required) {
          form_group.addClass("required");
        }

        /* control label */
        var control_label = $("<label/>").addClass("control-label")
                                         .attr("for", "id_"+p)
                                         .html(property.title);
        if(required) {
          control_label.addClass("required");
        }
        form_group.append(control_label);

        /* icon required */
        if(required) {
          var icon_required = $("<span/>").addClass("hz-icon-required")
                                           .addClass("fa")
                                           .addClass("fa-asterisk");
          form_group.append(icon_required);
        }

        /* help icon */
        if(property.hasOwnProperty("description")) {
          var help_icon = $("<span/>").addClass("help-icon")
                                      .attr("data-toggle", "tooltip")
                                      .attr("data-placement", "top")
                                      .attr("title", "")
                                      .attr("data-original-title", property.description);
          var question_circle = $("<span/>").addClass("fa")
                                            .addClass("fa-question-circle");
          help_icon.append(question_circle);
          form_group.append(help_icon);
        }

        /* control wrapper */
        var control_wrapper = $("<div/>");

        if(property.hasOwnProperty("eumn")) {
          //drop down list
          var dropdownlist_control = $("<select/>");
          dropdownlist_control.addClass("form-control");
          dropdownlist_control.attr("id", "id_"+p);
          dropdownlist_control.attr("name", p);

          //get drop down list options
          for(option in property.enum) {
            var option_control = $("<option/>").attr('value', property.enum[option])
                                               .html(property.enum[option]);
            dropdownlist_control.append(option_control);
          }

          //default value
          if(property.hasOwnProperty("default")) {
            if(property.default != null) {
              dropdownlist_control.val(property.default);
            }
          }

          //user value
          if(userdata != null) {
            if(userdata.hasOwnProperty(p)) {
              dropdownlist_control.val(userdata[p]);
            }
          }
          control_wrapper.append(dropdownlist_control);
        }
        else {
          switch(property.type) {
            case "string": {
              //text box
              var text_control = $("<input type='text'/>");
              text_control.addClass("form-control");
              text_control.attr("id", "id_"+p);
              text_control.attr("name", p);

              //default value
              if(property.hasOwnProperty("default")) {
                if(property.default != null) {
                  text_control.val(property.default);
                }
              }

              //user value
              if(userdata != null) {
                if(userdata.hasOwnProperty(p)) {
                  text_control.val(userdata[p]);
                }
              }
              control_wrapper.append(text_control);
              break;
            }
            case "boolean": {
              //check box
              var checkbox_control = $("<input type='checkbox'/>");
              checkbox_control.addClass("form-control");
              checkbox_control.attr("id", "id_"+p);
              checkbox_control.attr("name", p);

              //default value
              if(property.hasOwnProperty("default")) {
                if(property.default&&eval(property.default)) {
                  checkbox_control.attr("checked",true);
                }
              }

              //user value
              if(userdata != null) {
                if(userdata.hasOwnProperty(p)) {
                  if(userdata[p]) {
                    checkbox_control.attr("checked", true);
                  }
                  else {
                    checkbox_control.removeAttr("checked");
                  }
                }
              }
              control_wrapper.append(checkbox_control);
              break;
            }
            default: {
              break;
            }
          }
        }

        /* add control to body */
        form_group.append(control_wrapper);
        modal_body.append(form_group);
      }
    }
  }

  $.Karbor = {

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
    },

    /* Get dynamic field value */
    getDynamicValue: function(form_controls) {
      var data = null;
      if(form_controls!=null&&form_controls.length>0) {
        data = {};
        for(var i = 0; i<form_controls.length; i++) {
          var form_control = $(form_controls[i]);
          if(form_control!=null) {
            var form_control_name = form_control.attr("name");
            if(form_control.is("input[type='text']")) {
              data[form_control_name] = form_control.val();
            }
            else if(form_control.is("input[type='checkbox']")) {
             data[form_control_name] = (form_control.is(":checked") ? true : false);
            }
            else if(form_control.is("select")) {
              data[form_control_name] = form_control.val();
            }
            else {
              continue;
            }
          }
        }
      }
      return data;
    },

    /* create parameters dialog */
    createDialog(schema, userdata, resourceid) {
      var modal = $("<div/>").attr("id", "parametersdialog").addClass("modal");
      var modal_dialog = $("<div/>").addClass("modal-dialog");
      var modal_content = $("<div/>").addClass("modal-content");

      //modal header
      var modal_header = $("<div/>").addClass("modal-header");
      modal_header.append("<a class='close' data-dismiss='modal'>&times;</a>");
      modal_header.append("<h3 class='modal-title'>"
                       +(schema.title || "Edit Parameters")
                       +"</h3>");

      //modal body
      var modal_body = $("<div/>").addClass("modal-body").attr("resourceid", resourceid);
      createDynamicField(schema, userdata, modal_body);

      //modal footer
      var modal_footer = $("<div/>").addClass("modal-footer");
      var cancel = $("<a/>").attr("href", "#")
                         .addClass("btn")
                         .addClass("btn-default")
                         .addClass("cancel")
                         .attr("data-dismiss", "modal")
                         .html("Cancel");
      var save = $("<a/>").attr("href", "#")
                         .attr("type", "submit")
                         .addClass("btn")
                         .addClass("btn-primary")
                         .html("Save");
      modal_footer.append(cancel);
      modal_footer.append(save);

      //append children
      modal_content.append(modal_header);
      modal_content.append(modal_body);
      modal_content.append(modal_footer);

      modal_dialog.append(modal_content);
      modal.append(modal_dialog);
      return modal;
    },

    /* open parameters dialog */
    openDialog: function(dialog_data,dialog_element,dialog_parent) {
      $(dialog_parent).append(dialog_data);
      $(dialog_element).dialog({
        autoOpen: true,
        modal: true,
        open: function(event, ui) {
          $(dialog_element + " .modal-content").draggable({handle: ".modal-header"});
        },
        close: function(event, ui) {
          $(dialog_element).dialog('destroy');
          $(dialog_parent).empty();
        }
      });
    },

    /* close parameters dialog */
    closeDialog: function(dialog_element) {
      $(dialog_element).dialog("close");
    }
  };
})(jQuery);
