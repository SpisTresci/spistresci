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

    var as = $(".sort_by.active_sort");
    if (!as.hasClass("default")){
        dic["orderby"]=as.attr("data-sort-type");
    }
    return dic;
}

function refreshLinks(link, page){
    refreshPaginationLinks(link)
    refreshURL(link, page);
}

function refreshPaginationLinks(link){
    var bottom_pagination = $(".page .pagination");
    $(".L_top_panel .pagination").replaceWith(bottom_pagination.clone());

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
    var filter=$(this).closest(".filter_box");
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
    var product = $(this).closest('.search_list_book');
    var records = product.find('.records_panel_wrapper').first();

    if(product.hasClass("act")){
        product.removeClass("act");
        product.removeClass("act2");
        records.animate({"marginTop":records.data("no-act-margin")}, 1000, "swing", function(){
            records.css({"display":"none", "marginTop":0});
        });

    } else {
        product.addClass("act");
        var puller_h = -parseInt($(".puller_footer").css("margin-top"), 10) - 1;
        var switcher_up_h = parseInt($(".records_toogle_switcher").css("height"), 10)-puller_h;
        var records_h = (product.parent().data("records-count") * 131 - 1 )+ switcher_up_h + puller_h + 40;

        records.data("no-act-margin", -(records_h+puller_h));
        records.css({"height": records_h, "display":"block", "marginTop":records.data("no-act-margin")});
        records.animate({"marginTop":-switcher_up_h}, 1000, "swing", function(){
            product.addClass("act2");
        });

        product.find('.records_toogle_switcher.down').first().removeClass("onhover");
    }
}

function hideRecords(){
    var product = $(this).closest('.search_list_book');
    var records = product.find('.records_panel_wrapper').first();

    if(product.hasClass("act")){
        product.removeClass("act");
        product.removeClass("act2");
        records.animate({"marginTop":records.data("no-act-margin")}, 1000, "easeInBack", function(){
            records.css({"display":"none", "marginTop":0});
        });
    }
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

function refresh_L_left_panel_height(){
    $(".L_left_panel").height($(".filter_panel").height() + 50);
}

function refresh_active_sort(){
    var p = $(".sortboxwrapper");
    var as = p.find(".sort_by.active_sort");
    var asd = $(".active_sort_desc");
    asd.text(as.hasClass("default")?"":as.text());
}

function onReady(){
    $(".filter_formats, .filter_services").on("click", function(event){
        $(this).toggleClass("act");
        event.stopPropagation();
        rebuildResults();
    });

    /*$("#login").on("click", function(event){
        $(".loginform").toggleClass("act");
        event.preventDefault();
        event.stopPropagation();
    });*/

    refresh_active_sort();
    $(".sortbox").on("click", function(event){
        var p = $(".sortboxwrapper");
        p.toggleClass("active");

        var asd = $(".active_sort_desc");
        if (p.hasClass("active")){
            asd.text("według");
        }else{
            asd.text(p.find(".sort_by.active_sort").text());
        }
    });

    $(".sortboxwrapper").on("click", function(event){
        event.stopPropagation();
    });

    $(".sort_by").on("click", function(event){
        var p = $(".sortboxwrapper");
        var as = p.find(".sort_by.active_sort");
        if ($(this)[0] != as[0]){
            as.toggleClass("active_sort");
            $(this).toggleClass("active_sort");
            p.removeClass("active");
            refresh_active_sort();
            rebuildResults();
        }
    });

    $('html').click(function() {
        //close_popups();
        var p = $(".sortboxwrapper");
        p.removeClass("active");
        refresh_active_sort();
    });

    $(".filter_section_header").on("click", function(event){
        var p = $(this)

        if(p.closest(".filter_box").find("li.act").length == p.closest(".filter_box").find("li").length){
            p.addClass("act_group");
        } else if(p.closest(".filter_box").find("li.act").length == 0){
            p.removeClass("act_group");
        }

        p.toggleClass("act_group");
        p.closest(".filter_section").find("li").each(function(event){
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

    $(".filter_box_header").on("click", function(event){
        $(this).closest(".filter_obj").toggleClass("act");
        refresh_L_left_panel_height();
    });

    $(".filter_clear_button").on("click", clearFilter);
    $(".s_arrow_zip").on("click", s_zip);

    $(".filter_section_arrow").on("click", function(){
        $(this).toggleClass("filter_section_arrow2");
        $(this).closest(".filter_section").find("ul").toggleClass("hide_ul");
    });

    $('#search_box_form').submit(function(event){
        event.preventDefault();
        rebuildResults();
    });

    jQuery.ajaxSetup({
        beforeSend: function() {
            $('.main_container').addClass("loading");
        },
        complete: function(){
            $('.main_container').removeClass("loading");
        },
        success: function() {}
    });

    $(document).scroll(function(e) {
        if($(this).scrollTop() > 120){
            $(".s_index_top_bg").addClass("sticky");
        }
        else{
            $(".s_index_top_bg").removeClass("sticky");
        }
    });

    $.getScript("/static/js/sort_records.js", function(){
        sort_records();
    });

    refresh_L_left_panel_height();
    onResultsReady();
}

function onResultsReady() {
    prepareRecords();

    $(".p_center").on("click", toggleRecords);
    $('.records_toogle_switcher.down').on("click", hideRecords);

    $(".p_center").hover(
        function(){
            var product = $(this).closest('.search_list_book');
            if(!product.hasClass("act")){
                var switcher = product.find('.records_toogle_switcher.down').first();
                switcher.addClass("onhover");
            }
        },
        function(){
            var product = $(this).closest('.search_list_book');
            if(!product.hasClass("act")){
                var switcher = product.find('.records_toogle_switcher.down').first();
                switcher.removeClass("onhover");
            }
        }
    );

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

    if (typeof(sort_records) == "function"){
        sort_records();
    }

}


$(document).ready(onReady);
