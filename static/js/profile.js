function refresh_L_left_panel_height(){
    $(".L_left_panel").height($(".filter_panel").height() + 30);
}

$(function() {
    $(".filter_box_header").on("click", function(event){
        if($(this).hasClass("clickable"))
            $(this).closest(".filter_obj").toggleClass("act");

        refresh_L_left_panel_height();
    });

    refresh_L_left_panel_height();
});

