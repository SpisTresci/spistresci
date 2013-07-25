function collectFilters(){
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
    return dic;
}

function refreshLinks(link, page){
    refreshPaginationLinks(link)
    refreshURL(link, page);
}

function refreshPaginationLinks(link){
    $(".pageLink").each(function(){
        $(this).attr("href", "?"+link+"&page="+$(this).attr("data-p"));
    });

    $("input.pageLink").each(function(){
        $(this).val($(this).attr("data-p"));
    });
}

function refreshURL(urlPath, page){
    document.title = $("#id_q").val() + " - SpisTresci.pl";
    if(page != 1 && page !== 'undefined'){
        urlPath+="&page="+page;
    }
    window.history.replaceState("object or string", document.title, "?"+urlPath);
}

function loadResults(link, fun){
    $("#search_results").load("../q/?"+link, fun);
}

function clearFilter(){
    var filter=$(this).closest(".s_left_box");
    filter.find('input[class^="filter_"]').val("");
    filter.find('li[class^="filter_"]').removeClass("act");
    rebuildResults();
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
  return function (event) {
    var context = this, args = arguments;
    clearTimeout(timer);
    timer = setTimeout(function () {
      fn.apply(context, args);
    }, event.keyCode==13?0:delay);
  };
}

function rebuildResults(page){
    var dic = collectFilters();
    dic["q"] = $("#id_q").val();
    dic["page"] = typeof page !== 'undefined' ? page : 1;
    var link = $.param(dic);

    loadResults(link, onResultsReady);
}

function onReady(){
    $(".filter_formats, .filter_services").on("click", function(event){
        $(this).toggleClass("act");
        event.stopPropagation();
        rebuildResults();
    });

    $(".s_left_cat").on("click", function(event){
        var p = $(this)

        if(p.closest(".s_left_hide").find("li.act").length == p.closest(".s_left_hide").find("li").length){
            p.addClass("act_group");
        } else if(p.closest(".s_left_hide").find("li.act").length == 0){
            p.removeClass("act_group");
        }

        p.toggleClass("act_group");
        p.closest(".s_left_hide").find("li").each(function(event){
            if (p.hasClass("act_group")){
                $(this).addClass("act");
            }else{
                $(this).removeClass("act");
            }
        });
        rebuildResults();
    });

    $("#filter_price_from, #filter_price_to").keyup(debounce(function(){
        rebuildResults();
    }, 600));

    $(".s_left_blue").on("click", function(event){ $(this).closest(".s_left_box").toggleClass("act");});

    $(".filter_clear_button").on("click", clearFilter);
    $(".s_arrow_zip").on("click", s_zip);

    $(".s_left_cat_arrow").on("click", function(){
        $(this).toggleClass("s_left_cat_arrow2");
        $(this).closest(".s_left_hide").find("ul").toggleClass("hide_ul");
    });

    $('form').submit(function(event){
        event.preventDefault();
        rebuildResults();
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

    onResultsReady();
}

function onResultsReady() {
    prepareRecords();

    $(".search_drop_hide_btn, .search_drop_upper_hide_btn, .product_details").on("click", toggleRecords);

    $("input.pageLink").keyup(debounce(function(){
        rebuildResults($(this).val());
    }, 600));

    if($(".page_active_number").length > 0){
        var dic = collectFilters();
        dic["q"] = $("#id_q").val();

        var link = $.param(dic);
        var page = $(".page_active_number").attr("data-p");
        refreshLinks(link, page);
    }
}

$(document).ready(onReady);
