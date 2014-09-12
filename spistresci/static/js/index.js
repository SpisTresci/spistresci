function onResultsReady() {
    $(".track_button").on("click", function(event){
        var id = $(this).attr("data-track-form-id");
        get_track_form(id);
        event.stopPropagation();
    });
    $("#track_form_container").on("click", function(event){event.stopPropagation();});
}

$(document).ready(function(){

    $('html').click(function() {
        turn_off_spotlight();
    });

    $(".ib_text1").dotdotdot();
});
