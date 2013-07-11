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

function mark_format(subgroup, item){
  var elem = $('#filter_format_li_'+subgroup+'_'+item)[0];
  elem.className=(elem.className.indexOf("act") !== -1)?'':'act';
  $.post('/set_filter/format/'+elem.children[0].innerHTML+'/'+elem.className+'/');
  return false;
}

function mark_price(id){
  var elem = document.getElementById('filter_' + id);
  $.post('/set_filter/price/'+id+'/'+elem.value.toString()+'/');
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
    $.post('/clear_filter/format/');
  return false;
}

function filter_price_clear(){
    $('input[id^="filter_price_"]').each(function(index, value) {value.value='';})
    $.post('/clear_filter/price/');
  return false;
}

function filter(){
  elem = document.getElementById('id_q');
  query=elem.value;

  window.open('?q='+query, '_self');
  return false;
}
