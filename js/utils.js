$(function(){
	$(".hide").hide();
	$(".details h2 a.dashed").toggle(
		function(){
			$(this).parent("h2").siblings("div.hide").slideDown("fast");
		},
		function(){
			$(this).parent("h2").siblings("div.hide").slideUp("fast");
		}
	);
	
	// Простейшая защита email от ботов, inaccessible
	$(".email").each(function(){
		var e = $(this).attr("href") + "@" + $(this).text();
		$(this).text(e);
		$(this).attr("href", "mailto:" + e);
	});
});

