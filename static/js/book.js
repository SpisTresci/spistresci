function onReady()
{
 $("#book_description").on("click", $("#show_description"), function(event){
  $("#book_description").load("../../description/"+$("#book_container").data("book-id")) ;
 });

 $(document).scroll(function(e) {
   if($(this).scrollTop() > 120){
     $(".s_index_top_bg").addClass("sticky");
   }
   else{
     $(".s_index_top_bg").removeClass("sticky");
   }
 });
}

$(document).ready(onReady)
