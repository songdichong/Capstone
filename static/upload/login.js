/*
Original Author: Dichong Song
Creation date: Jan 25th, 2019
Contents of file:
	1. AJAX call to send signal from front-end to back-end
*/
var username;
document.addEventListener('keydown', function(e) {
	if (e.keyCode == 113 || e.keyCode == 81){
	  e.keypress = '1';
	//   alert("pressed");
	  PHOTO = 1;
	  runAjax(1)
	}
});
function runAjax(signal) {
	$.ajax({
		type: "post",
		url: "/",
		dataType: "json",
		data: {'request':signal},
		success: function(result){
			username = result;
			window.location.href="/specialUserPage";   
		}
	});
}

