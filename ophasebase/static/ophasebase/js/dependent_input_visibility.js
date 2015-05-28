function dependent_input_visibility(a, b){
  _dependent_input_visibility_inner(a, b);
  $('#'+a).click(function(){
    _dependent_input_visibility_inner(a, b);
  })
}
function _dependent_input_visibility_inner(a, b){
  if($('#'+a).is(':checked')){$('#'+b).parent().show();
    $('#'+b).prop('required',true);}
  else {$('#'+b).val('');
    $('input:checkbox[id^="'+b+'"]:checked').each(function(){
      $(this).removeAttr('checked');})
    $('#'+b).removeAttr('required');
    $('#'+b).parent().hide();}
}

function dependent_two_input_visibility(a,b,c){
  _dependent_two_input_visibility_inner(a,b,c);
  $('#'+a).click(function(){
    _dependent_two_input_visibility_inner(a,b,c);
  })
  $('#'+b).click(function(){
    _dependent_two_input_visibility_inner(a,b,c);
  })
}

function _dependent_two_input_visibility_inner(d,e,f){
  a='#'+d;b='#'+e;c='#'+f;
  if($(a).is(':checked') || $(b).is(':checked')){$(c).parent().show();
  $(c).prop('required',true);}
  else {$(c).val('');
  $(c).removeAttr('required');
  $('input:checkbox[id^="'+f+'"]:checked').each(function(){
      $(this).removeAttr('checked');});$(c).parent().hide();}
}
