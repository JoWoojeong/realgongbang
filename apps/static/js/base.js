$(document).ready(function () {
	var count = 0;
	$("#add_process").click(function(){
		count ++;
		$("#process").append("<div><input type  = 'file' name = 'process_photo_"+count+"'><input type = 'text' name = 'process_discript_"+count+"'></div>");
		$("#count").val(count);
	});

	var count2 = 0;
	$("#add_inspire").click(function(){
		count2 ++;
		$("#inspire").append("<div><input type  = 'file' name = 'inspire_photo_"+count2+"'></div>");
		$("#count2").val(count2);
	});
	  
});