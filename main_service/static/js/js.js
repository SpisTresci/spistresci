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

function rebuildLinks(){
    var dic = {};
    $('li[class^="filter_"]').each(function(){
        var filter_name = $(this).attr('class').split(' ').filter(function(element, index, array){return element.substring(0, 7) == 'filter_';})[0].substring(7);

        if ($(this).hasClass("act")){
            var atr = $(this).attr("data-q");
            if (filter_name in dic){
               dic[filter_name]+= ","+atr;
            }else{
               dic[filter_name]=atr;
            }
        }
    });

    $('input[class^="filter_"]').each(function(){
        var filter_name = $(this).attr('class').split(' ').filter(function(element, index, array){return element.substring(0, 7) == 'filter_';})[0].substring(7);
        if($(this).val()){
            dic[$(this).attr("data-q")]=$(this).val()
        }
    });

    var link = $.param(dic);
    $("#id_q").attr("data-q", link);

    dic["q"]=$("#id_q").val();
    link = $.param(dic);

    $(".pageLink").each(function(){
        if($(this).attr("data-q")){
            link+="&page="+$(this).attr("data-p");
        }
        $(this).attr("href", link);
    });
}

function reloadResults(){
    var q=$("#id_q").attr("data-q");
    var href = '?q='+ $("#id_q").val() + (q?"&"+q:"");

    $("#search_results").load("../q/"+href, function(){
        $(".search_drop_hide_btn, .search_drop_upper_hide_btn, .product_details").on("click", toggleRecords);
    });

    refreshURL(href);
}

function refreshURL(urlPath){
    document.title = $("#id_q").val() + " - SpisTresci.pl";
    window.history.replaceState("object or string", document.title, urlPath);
}


function collectFilters(){
    var formats = []
    $(".filter_formats.act").find("a").each(function() { formats.push($(this).data("q"))});
    setFilter("#id_formats", formats.join(','), "formats");

    var services = []
    $(".filter_services.act").find("a").each(function() { services.push($(this).data("q"))});
    setFilter("#id_services", services.join(','), "services");

    setFilter("#id_price_gte", $("#filter_price_from").val(), "from");
    setFilter("#id_price_lte", $("#filter_price_to").val(), "to");
}

function clearFilter(){
    rebuildLinks();
    var filter=$(this).closest(".s_left_box");
    filter.find('input[class^="filter_"]').val("");
    filter.find('li[class^="filter_"]').removeClass("act");
    reloadResults();
}

function s_zip(){
      $(".s_left").toggleClass("s_zip");
      $(".s_right").toggleClass("s_right2");
}

function prepareRecords(){
    $(".search_list_item").each(function(){
        var records_count = $(this).attr("data-records-count");
        var height = 35 + records_count * 136;
        $(this).find(".search_drop").css({"marginTop":"-"+height+"px"});
    });
}

function toggleRecords(){
    var product = $(this).closest(".search_list_item");
    var records_count = product.attr("data-records-count");
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

function debounce(fn, delay) {
  var timer = null;
  return function () {
    var context = this, args = arguments;
    clearTimeout(timer);
    timer = setTimeout(function () {
      fn.apply(context, args);
    }, delay);
  };
}

$(document).ready(function (){
    prepareRecords();
    $(".s_left_cat, .filter_formats, .filter_services").on("click", function(event){ $(this).toggleClass("act"); event.stopPropagation(); rebuildLinks();reloadResults();});
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

    $("#filter_price_from, #filter_price_to").keyup(debounce(function (event) {
        rebuildLinks();
        reloadResults();
        //$("#id_submit").click();
    }, 1000));

    rebuildLinks();
    $('form').submit(function(){
        var q=$("#id_q").attr("data-q")
        var href = '?q='+ $("#id_q").val() + (q?"&"+q:"");
        location.href = href
    });

    jQuery.ajaxSetup({
        beforeSend: function() {
            $('#s_right').addClass("loading");
        },
        complete: function(){
            $('#s_right').removeClass("loading");
        },
        success: function() {}
    });
});

