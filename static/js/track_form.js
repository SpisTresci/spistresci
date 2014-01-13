function send_form(form_id){
    var data = $(form_id).serialize(true);
    Dajaxice.spistresci.post_track_form(Dajax.process, {'form': data});
}

function get_track_form(book_id){
    Dajaxice.spistresci.get_track_form(Dajax.process, {'book_id': book_id, 'callback':'set_x_callback'});
}

function set_x_callback(book_id){
    $('#x_' + (book_id).toString()).on("click",function(){
        turn_off_spotlight();
    });

    var element = $('#track_form_container');
    element.on("click", function(event){event.stopPropagation();});
    element.addClass("dialog_style1");
    $("html").attr("data-active-track-form-id", book_id);
    element.spotlight({animate:false, onShow:function(){}});
}

function turn_off_spotlight(){
   //var book_id = $("html").attr("data-active-track-form-id");
   //if (typeof book_id !== 'undefined' && book_id !== false) {
       var spotlight = $('#spotlight');
       var element = $('#track_form_container');
       spotlight.css('opacity', '0');
       //if(currentPos == 'static') element.css('position', 'static');
       element.css('z-index', '1');
       element.removeClass("dialog_style1");
       element.empty();
   //}
}
