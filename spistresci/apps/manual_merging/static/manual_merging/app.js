function loadPage() {
	$.ajax({
		url: "take/",
		success: function(html) {
			$("body").append(html);
			$(".books").unbind("click");
                        $(".books").on("click", ".same_books", function(){
				window.number++;
				loadPage();
                                $(this).closest(".books").slideUp(300);
                        });
                        $(".books").on("click", ".not_same_books", function(){
                                window.number++;
                                loadPage();
                                $(this).closest(".books").slideUp(300);
                        });
			if($(".selected").size() < 1) {
				$(".compare").first().addClass("selected");
			}
		}
	});
}

function cmnPrev() {
	$(".selected").prev().addClass("selected");
	$(".selected").last().removeClass("selected");
}

function cmnNext() {
    $(".selected").next().addClass("selected");
    $(".selected").first().removeClass("selected");
}

function preventDefault(e) {
  e = e || window.event;
  if (e.preventDefault)
      e.preventDefault();
  e.returnValue = false;  
}

function keydown(e) {
    if (e.keyCode == "40") {
        preventDefault(e);
	if($(".selected").next().size() != 0) {
        	cmnNext();
        	target = $(".selected");
        	$("body, html").animate({"scrollTop":target.offset().top}, 250);
        	return;
	}
    }
    if (e.keyCode == "38") {
        preventDefault(e);
	if($(".selected").prev().size() != 0) {
        	target = $(".selected");
        	$("body, html").animate({"scrollTop":target.offset().top-490}, 250);
        	cmnPrev();
	}
        return;
    }
	if(e.keyCode == "13") {
		$(".selected").closest(".compare").animate({"background-color":"green", "opacity":"0.5"});
        	cmnNext();
        	target = $(".selected");
        	$("body, html").animate({"scrollTop":target.offset().top}, 250);
		return;
	}
	if(e.keyCode == "88") {
		$(".selected").closest(".compare").animate({"background-color":"red", "opacity":"0.5"});
        	cmnNext();
        	target = $(".selected");
        	$("body, html").animate({"scrollTop":target.offset().top}, 250);
		return;
	}
	if(e.keyCode == "191") {
		$(".selected").closest(".compare").animate({"background-color":"blue", "opacity":"0.5"});
        	cmnNext();
        	target = $(".selected");
        	$("body, html").animate({"scrollTop":target.offset().top}, 250);
		return;
	}
}

$(document).ready(function(){
	for (window.number = 0; window.number < 10; window.number++) {
		loadPage();
	}
	window.number--;				//prawdopodobnie tego fora z takim iterowaniem i na koncu dekrementacja iteratora powinienem napisac w jakis inny, ladniejszy sposob. jesli wiesz jak, to daj znac :)

	$(window).scroll(function() {
		if($(document).height() - $(document).scrollTop() < 1000) {
			window.number++;
			loadPage();
		}
	});
	document.onkeydown = keydown;
});
