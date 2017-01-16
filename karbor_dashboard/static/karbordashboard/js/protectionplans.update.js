/*  Copyright (c) 2016 Huawei, Inc.

    Licensed under the Apache License, Version 2.0 (the "License"); you may
    not use this file except in compliance with the License. You may obtain
    a copy of the License at

         http://www.apache.org/licenses/LICENSE-2.0

    Unless required by applicable law or agreed to in writing, software
    distributed under the License is distributed on an "AS IS" BASIS, WITHOUT
    WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. See the
    License for the specific language governing permissions and limitations
    under the License.
*/

/* set the children check */
function setChecked(node, isChecked) {
  if(isChecked) {
    node.row.find("input[type=checkbox]").prop("checked", true);
  }
  else {
    node.row.find("input[type=checkbox]").removeAttr("checked");
  }
  for(var i = 0; i<node.children.length;i++) {
    var resourceChild = node.children[i];
    setChecked(resourceChild, isChecked);
  }
}

/* set the choose resources */
function setProtectedResource() {
  var resources = [];
  var cbResources = $(".cbresource:checked");
  var provider = getProvider($("select[name='provider_id']").val());
  var parameters = $.Karbor.getResourceDefaultParameters(provider, "options_schema");
  if(cbResources != null) {
    cbResources.each(function() {
      var cbResource = $(this);
      var resource = {};
      resource.id = cbResource.closest("tr").attr("resource-id");
      resource.type = cbResource.closest("td").next().find("span").html();
      resource.name = cbResource.closest("span").nextAll("span.spanresource").eq(0).html();
      resources.push(resource);

      var parameterbtn = cbResource.closest("tr").find(".editparameters");
      var userdata = parameterbtn.data("userdata");
      if(userdata!=null) {
        parameters[resource.type + "#" + resource.id] = userdata;
      }
    });
  }
  $(".resources").val(angular.toJson(resources));
  $(".parameters").val(angular.toJson(parameters));
}

horizon.protectionplans_update = {
  /* init create plan dialog */
  init: function(){
    /* init resource tree */
    $("#protectionplanUpdateResource").treetable({ expandable: true });

    /* init plan resources*/
    (function(){
      plan = $.parseJSON($(".plan").val());
      if(plan.resources != null){
        resources = plan.resources
        $(resources).each(function() {
          resource_id = this.id
          node = $("#protectionplanUpdateResource").find("tr[resource-id='"+ resource_id +"']");
          node.find("input[type=checkbox]").prop("checked", true);
        });
      }
    })();

    /* init protection provider */
    (function() {
      provider = $.parseJSON($(".provider").val());
      $("#protectionplanUpdateResource").find("input[resourcetype]").data("schema", null);
      $("#protectionplanUpdateResource").find("input[resourcetype]").data("userdata", null);
      if(provider != null) {
        if(provider.extended_info_schema != null) {
          var result = provider.extended_info_schema['options_schema'];
          for(var r in result) {
            $("#protectionplanUpdateResource").find("input[resourcetype='" + r + "']").data("schema", result[r]);
            $("#protectionplanUpdateResource").find("input[resourcetype='" + r + "']").data("userdata", null);
          }
        }
      }
    })();

    /* live resource check event */
    $(document).on('click', ".cbresource", function() {
      var tr = $(this).closest("tr");
      var node = $("#protectionplanUpdateResource").treetable("node", tr.attr("data-tt-id"));
      setChecked(node, $(this).is(":checked"));
    });

    /* live resource parameters event */
    $(document).on('click',".editparameters", function() {
      var schema = $(this).data("schema");
      var userdata = $(this).data("userdata");
      var resourceid = $(this).closest("tr").attr("resource-id");
      if(schema != null) {
        var exist_ui_dialogs = $("body").has(".ui-dialog");
        if(exist_ui_dialogs.length == 0){
          var dialog_data = $.Karbor.createDialog(schema, userdata, resourceid);
          $.Karbor.openDialog(dialog_data, "#parametersdialog", "div.dialog_wrapper");
        }
      }
    });

    /* bind parameters dialog save button event */
    $(document).on('click', "#parametersdialog .btn.btn-primary", function() {
      var flag = $.Karbor.check_required($("#parametersdialog"));
      if(flag) {
        var resourceid = $("#parametersdialog .modal-body").attr("resourceid");
        var form_controls = $("#parametersdialog .modal-body .form-control");
        var userdata = $.Karbor.getDynamicValue(form_controls);
        $("#protectionplanUpdateResource").find("tr[resource-id='" + resourceid + "']")
                                          .find(".editparameters")
                                          .data("userdata", userdata);
        $.Karbor.closeDialog("#parametersdialog");
      }
    });

    /* bind create button event */
    $(".btn-primary.save").bind("click", function() {
      setProtectedResource();
      return true;
    });

    /* bind parameters dialog cancel button event */
    $(document).on('click', "#parametersdialog .btn.cancel", function() {
      $.Karbor.closeDialog("#parametersdialog");
    });

    /* bind parameters dialog close button event */
    $(document).on('click', "#parametersdialog a.close", function() {
      $.Karbor.closeDialog("#parametersdialog");
    });
    
  }
};
