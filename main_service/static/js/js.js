function toggleFormatFilter(){
    $(this).toggleClass("act");
}

function setFilter(id, val, name) {
    if (val){if($(id)){$(id).val(val);}else{$("<input>").attr({"type":"hidden","value":val,"name":name}).appendTo(".search_box");}} else {if($(id)){$(id).remove();}}
}

function collectFilters(){
    var formats = []
    $(".filter_format.act").find("a").each(function() { formats.push($.trim($(this).text()))});

    setFilter("#id_formats", formats.join(','), "formats");
    setFilter("#id_price_gte", $("#filter_price_from").val(), "from");
    setFilter("#id_price_lte", $("#filter_price_to").val(), "to");
}

$(document).ready(function (){
    $(".filter_format").on("click", toggleFormatFilter);
    $("#id_submit").on("click", collectFilters);
    $(".filter_button").on("click", function(){ $("#id_submit").click();});
});

function s_zip(){
  if(document.getElementById('s_left').className.indexOf("s_zip") !== -1){
    document.getElementById('s_left').className='s_left';
    document.getElementById('s_right').className='s_right';
    $.post('/hide_menu/0/');
    zip_tmp="";
  }
  else{
    document.getElementById('s_left').className='s_left s_zip';
    document.getElementById('s_right').className='s_right s_right2';
    $.post('/hide_menu/1/');
  }

  return false;
}

var tmp=[];
function s_blue(num){
  if(tmp[num]!="hide"){
    document.getElementById('blue'+num).className='s_left_box';
    tmp[num]="hide";
  }
  else{
    document.getElementById('blue'+num).className='s_left_box act';
    tmp[num]="";
  }
  return false;
}

var tmp_sub=[];
function sub(num){
  if(tmp_sub[num]!="hide"){
    document.getElementById('sub'+num).style.display="none";
    document.getElementById('menu_arrow'+num).className="s_left_cat_arrow s_left_cat_arrow2";
    tmp_sub[num]="hide";
  }
  else{
    document.getElementById('sub'+num).style.display="block";
    document.getElementById('menu_arrow'+num).className="s_left_cat_arrow ";
    tmp_sub[num]="";
  }
  return false;
}

var btn1=[];
function btn(num){
  if(btn1[num]!="hide"){
    document.getElementById('btn'+num).className='s_left_cat act';
    btn1[num]="hide";
  }
  else{
    document.getElementById('btn'+num).className='s_left_cat';
    btn1[num]="";
  }
  return false;
}

var listbook=[];
function list_book(id, count_link, filter_info){

  var height_link=35+count_link*136 + (filter_info?25:0);

  if(listbook[id]!="show"){
    document.getElementById('list_book'+id).style.marginTop="0px";
    document.getElementById('list_book_2_'+id).style.height=height_link+"px";

    document.getElementById('hide'+id).className='search_drop_hide_btn2';
    listbook[id]="show";
  }
  else{

    document.getElementById('list_book'+id).style.marginTop="-"+height_link+"px";
    document.getElementById('list_book_2_'+id).style.height="0px";

    document.getElementById('hide'+id).className='search_drop_hide_btn';
    listbook[id]="";
  }
  return false;
}

function filter_format_clear(){
    $('li[id^="filter_format_li"]').each(function(index, value) {value.className='';})
  return false;
}

function filter_price_clear(){
    $('input[id^="filter_price_"]').each(function(index, value) {value.value='';})
  return false;
}
