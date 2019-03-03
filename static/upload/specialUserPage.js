/*
Original Author: Shengyao Lu
Creation date: Jan 25th, 2019
Contents of file:
	1. AJAX call to send signal from front-end to back-end
*/
var KEY_ENTER = 13;
document.addEventListener('keydown', function(e) {
	if (e.keyCode == KEY_ENTER){
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
