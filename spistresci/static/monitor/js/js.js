var timer = null;

$(document).ready(function(){
    $("#new_update").on("click", function(event){
        $(".new_update").toggle();
    });
    $("#all").on("click", function(event){
        $("#all").toggleClass("checked");
        $(".update_checkbox").prop("checked", $("#all").hasClass("checked"));
    });

    setTimer(timer);

    $("#autorefresh").on("click", function(){
        clearTimeout(timer);
        setTimer(timer)
    });
});

function setTimer(){
    if($("#autorefresh").prop("checked")){
        timer = setTimeout(function () {
            location.reload();
        },10000);

    }
}