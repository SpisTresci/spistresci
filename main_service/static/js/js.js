var zip_tmp="";
function s_zip(){
  if(zip_tmp!="hide"){
    document.getElementById('s_left').className='s_left s_zip';
    document.getElementById('s_right').className='s_right s_right2';
    zip_tmp="hide";
  }
  else{
    document.getElementById('s_left').className='s_left';
    document.getElementById('s_right').className='s_right';
    zip_tmp="";
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
    tmp_sub[num]="hide";
  }
  else{
    document.getElementById('sub'+num).style.display="block";
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


var li_sub=[];
function li(num){
  if(li_sub[num]!="hide"){
    document.getElementById('li'+num).className='act';
    li_sub[num]="hide";
  }
  else{
    document.getElementById('li'+num).className='';
    li_sub[num]="";
  }
  return false;
}

var listbook=[];
function list_book(num){
  if(listbook[num]!="show"){
    document.getElementById('list_book'+num).style.display="block";
    listbook[num]="show";
  }
  else{
    document.getElementById('list_book'+num).style.display="none";
    listbook[num]="";
  }
  return false;
}








