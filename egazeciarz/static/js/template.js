	jQuery(document).ready(function(){
			// Create the dropdown base
jQuery("<select />").appendTo("#mobilemenu");
var mobileMenuTitle = jQuery("#mobilemenu").attr("title");
// Create default option "Go to..."
jQuery("<option />", {
   "selected": "selected",
   "value"   : "",
   "text"    : mobileMenuTitle
}).appendTo("#mobilemenu select");

// Populate dropdown with menu items
jQuery("#nav ul.menu>li>a, #nav ul.menu>li>span.mainlevel,#nav ul.menu>li>span.separator").each(function() {
 var el = jQuery(this);
 jQuery("<option />", {
     "value"   : el.attr("href"),
     "text"    : el.text()
     
 }).appendTo("#mobilemenu select");
getSubMenu(el);
});

function getSubMenu(el){
	var subMenu = jQuery('~ ul>li>a',el);
	var tab = "- ";
	if (!(subMenu.length === 0)){
		subMenu.each(function(){
			var sel = jQuery(this);
			var nodeval = tab + sel.text();
			 jQuery("<option />", {
			     "value"   : sel.attr("href"),
			     "text"    : nodeval

			 }).appendTo("#mobilemenu select");
			getSubMenu(sel);
		});
	}
}
 // To make dropdown actually work
          // To make more unobtrusive: http://css-tricks.com/4064-unobtrusive-page-changer/
      jQuery("#mobilemenu select").change(function() {
        window.location = jQuery(this).find("option:selected").val();
      });
			
	});