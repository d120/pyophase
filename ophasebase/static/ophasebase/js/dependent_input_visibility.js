function dependent_input_visibility(a, b){
  _dependent_input_visibility_inner(a, b);
  $('#'+a).click(function(){
    _dependent_input_visibility_inner(a, b);
  })
}
function _dependent_input_visibility_inner(a, b){
  if($('#'+a).is(':checked')){$('#'+b).parent().show();
    $('#'+b).prop('required',true);
    $('#'+a).parent().parent().addClass('superquestion');
    $('#'+b).parent().addClass('subquestion');}
  else {$('#'+b).val('');
    $('input:checkbox[id^="'+b+'"]:checked').each(function(){
      $(this).removeAttr('checked');})
    $('#'+b).removeAttr('required');
    $('#'+b).parent().hide();
    $('#'+a).parent().parent().removeClass('superquestion');
    $('#'+b).parent().removeClass('subquestion');}
}

function dependent_multi_checkbox_active(a, b) {
  var checkboxes = $("#"+a).find("input[type='checkbox']");
  toggle_visibility_enabled_disabled(checkboxes.is(":checked"), b);

  checkboxes.click(function() {
     toggle_visibility_enabled_disabled(checkboxes.is(":checked"), b);
  });
}

function toggle_visibility_enabled_disabled(targetState, id) {
  var toggledElement = $("#"+id);
  var toggledParent = toggledElement.parent();

  toggledElement.attr("disabled", !targetState);
  if(targetState){
    toggledParent.show();
    toggledElement.prop('required',true);
  }
  else {
    toggledParent.hide();
    toggledElement.removeAttr('required');
    toggledElement.val('')
  }
}
