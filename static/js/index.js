function onResultsReady() {
    $(".track_button").on("click", function(event){
        var id = $(this).attr("data-track-form-id");
        get_track_form(id);
        event.stopPropagation();
    });
}

$(document).ready(function(){
    $("#search_results_1").load("/qb/?q=+&orderby=random", onResultsReady);
    $("#search_results_2").load("/qn/?q=+&orderby=random", onResultsReady);
    $("#search_results_3").load("/qp/?q=+&orderby=random", onResultsReady);

    $('html').click(function() {
        turn_off_spotlight();
    });
});
