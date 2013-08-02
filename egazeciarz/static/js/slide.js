// Slide and toggles
// Right Accordion Script

// Right Accordion Script
jQuery(document).ready(function(){
	
	jQuery('.moduletable-slide .moduleTitle>h3').each(function(index){
		
		var jQuerythis=jQuery(this);
		var jQuerycheckElement=jQuerythis.parent().next('div.jbslideContent');
		var jQueryslideID=jQuerycheckElement.attr('id');
		
		if(jQuery.cookie(jQueryslideID)=='close'){
			jQuery(jQuerycheckElement).hide();
			jQuerythis.addClass('close')}
			
			else{jQuerythis.addClass('open')}
			
			jQuerythis.click(function(){
				checkCookie(jQuerycheckElement,jQuerythis,jQueryslideID)})
			});
		});
				
		function checkCookie(jQuerycheckElement,jQuerythis,jQueryslideID){
			if(jQuerycheckElement.is(':hidden')){
				jQuerycheckElement.slideDown("fast");
				jQuerythis.removeClass('close');
				jQuerythis.addClass('open');
				cookieValue='open';
				jQuery.cookie(jQueryslideID,cookieValue)}
				
			else{
				jQuerycheckElement.slideUp();
			cookieValue='close';jQuerythis.removeClass('open');
			jQuerythis.addClass('close');
			jQuery.cookie(jQueryslideID,cookieValue)}}