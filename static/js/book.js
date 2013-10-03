function onReady()
{
 $("#book_description").on("click", $("#show_description"), function(event){
  $("#book_description").load("../../description/"+$("#book_container").data("book-id")) ;
 });
}

$(document).ready(onReady)
