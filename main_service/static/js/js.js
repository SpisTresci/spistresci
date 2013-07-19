function setFilter(id, val, name) {
    if($(id).length > 0){
        if (val){
            $(id).val(val);
        }else{
            $(id).remove();
        }
    } else {
        if (val){
            $("<input>").attr({"type":"hidden","value":val,"name":name}).appendTo(".search_box");
        }
    }
}

function collectFilters(){
    var formats = []
    $(".filter_format.act").find("a").each(function() { formats.push($.trim($(this).text()))});
    setFilter("#id_formats", formats.join(','), "formats");

    var services = []
    $(".filter_service.act").find("a").each(function() { services.push($.trim($(this).text()))});
    setFilter("#id_services", services.join(','), "services");

    setFilter("#id_price_gte", $("#filter_price_from").val(), "from");
    setFilter("#id_price_lte", $("#filter_price_to").val(), "to");
}

function clearFilter(){
    var filter=$(this).closest(".s_left_box");
    filter.find('input[class^="filter_"]').val("");
    filter.find('li[class^="filter_"]').removeClass("act");
}

function s_zip(){
      $(".s_left").toggleClass("s_zip");
      $(".s_right").toggleClass("s_right2");
}

function prepareRecords(){
    $(".search_list_item").each(function(){
        var records_count = $(this).data("records-count");
        var height = 35 + records_count * 136;
        $(this).find(".search_drop").css({"marginTop":"-"+height+"px"});
    });
}

function toggleRecords(){
    var product = $(this).closest(".search_list_item");
    var records_count = product.data("records-count");
    var height = 35 + records_count * 136 + (product.find(".sd_format_filtered_out").length > 0?25:0);

    if(product.hasClass("act")){
        product.find(".search_drop").css({"marginTop":"-"+height+"px"});
        product.find(".search_drop2").css({"height":"0px"});
    } else {
        product.find(".search_drop").css({"marginTop":"0px"});
        product.find(".search_drop2").css({"height":height+"px"});
    }
    product.toggleClass("act");
    product.find(".search_drop_hide_btn").toggleClass("act");
}

$(document).ready(function (){
    prepareRecords();
    $(".s_left_cat, .filter_format, .filter_service").on("click", function(event){ $(this).toggleClass("act"); event.stopPropagation(); });
    $(".search_drop_hide_btn, .search_drop_upper_hide_btn, .product_details").on("click", toggleRecords);
    $(".s_left_blue").on("click", function(event){ $(this).closest(".s_left_box").toggleClass("act");});
    $("#id_submit").on("click", collectFilters);
    $(".filter_button").on("click", function(){ $("#id_submit").click();});
    $(".filter_clear_button").on("click", clearFilter);
    $(".s_arrow_zip").on("click", s_zip);

    $(".s_left_cat_arrow").on("click", function(){
        $(this).toggleClass("s_left_cat_arrow2");
        $(this).closest(".s_left_hide").find("ul").toggleClass("hide_ul");
    });


});

