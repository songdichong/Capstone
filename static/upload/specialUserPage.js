/*
Original Author: Shengyao Lu
Creation date: Jan 25th, 2019
Contents of file:
	1. AJAX call to send signal from front-end to back-end
*/
document.addEventListener('keydown', function(e) {
	if (e.keyCode == 13){
	  e.keypress = '1';
	  runAjax(2)
	}
});
function runAjax(REQUEST) {
	$.ajax({
		type: "post",
		url: "/",
		dataType: "json",
		data: {'request':REQUEST},
		success: function(result){
			username = result;  
		}
	});
}