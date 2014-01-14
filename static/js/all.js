function shake_input_placeholder(){
    var tag = "#id_q";
    var data_shake = $(tag).attr("data-shake");
    $(tag).attr("data-shaked", data_shake*2+1);
    var f = function(){
        var s = $(tag).attr("data-shaked")
        if(s > 0 ){
            $(tag).attr("data-shaked", s-1);
            $(tag).animate({'padding-left': 6*(s%2) + 17} , 90, "easeInOutQuint", s>0?f:None);
        }
    };
    $(tag).animate({'padding-left': 20}, 90, "easeInOutQuint", f);
}

$(document).ready(function(){
    $( "#search_form" ).submit(function(event) {
      $("#id_q").val($.trim($("#id_q").val()));

      if($("#id_q").val()==""){
        shake_input_placeholder();
        event.preventDefault();
      }
    });

    $('#search_btn').click(function() {
        $("#id_q").val($.trim($("#id_q").val()));

        if($("#id_q").val()==""){
            shake_input_placeholder();
        }else{
            document.forms['search_form'].submit();
        }
    });
});
