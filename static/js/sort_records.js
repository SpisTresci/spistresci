function sort_records_alg(_this, by, rev){
    $.fn.reverse = [].reverse;
    var records = $(_this).closest(".records_panel").find(".record");
    var records_cpy=records.clone();
    records_cpy.sort(by);
    if(rev){records_cpy.reverse();}
    for(var i=0; i<records.size(); i++){
        $(records[i]).replaceWith(records_cpy[i]);
    }
}

function by_service(a, b){
    var aname = $(a).find(".service_logo_box img").attr("alt").toLowerCase();
    var bname = $(b).find(".service_logo_box img").attr("alt").toLowerCase();
    return (aname<bname)?-1:(aname>bname)?1:0;
}

function by_formats(a, b){
    var aname = parseInt($(a).find(".record_formats").attr('data-no'));
    var bname = parseInt($(b).find(".record_formats").attr('data-no'));
    return (aname<bname)?-1:(aname>bname)?1:0;
}

function by_price(a, b){
    var aname = parseFloat($(a).find(".record_price .value").text());
    var bname = parseFloat($(b).find(".record_price .value").text());
    return (aname<bname)?-1:(aname>bname)?1:0;
}

function sort_records(){
    $('.sortable.service').each(function(){
        $(this).on("click", function(){
            $(this).toggleClass("act");
            sort_records_alg(this, by_service, !$(this).hasClass("act"));
        });
    });
    $('.sortable.formats').each(function(){
        $(this).on("click", function(){
            $(this).toggleClass("act");
            sort_records_alg(this, by_formats, $(this).hasClass("act"));
        });
    });
    $('.sortable.price').each(function(){
        $(this).on("click", function(){
            $(this).toggleClass("act");
            sort_records_alg(this, by_price, !$(this).hasClass("act"));
        });
        $(this).click();
    });
}