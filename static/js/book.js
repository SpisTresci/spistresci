function set_click(){
}

function onReady()
{
 /*
 $("#description").on("click", $("#show_description"), function(event){
  $("description").load("../../description/"+$("#book_container").data("book-id")) ;
 });
 */

 $(document).scroll(function(e) {
   if($(this).scrollTop() > 120){
     $(".s_index_top_bg").addClass("sticky");
   }
   else{
     $(".s_index_top_bg").removeClass("sticky");
   }
 });

/*
 $('#filter_switcher').on("click", function(event){
     $(".filter_panel").toggle();
 });
*/
  $.getScript("/static/js/sort_records.js", function(){
    sort_records();
  });

  var id = $("#title").attr("data-book-id");
  get_track_form_static(id, 'set_click');

}

$(document).ready(onReady);
