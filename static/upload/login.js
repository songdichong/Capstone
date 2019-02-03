/*
Original Author: Dichong Song
Creation date: Jan 25th, 2019
Contents of file:
	1. AJAX call to send signal from front-end to back-end
*/
$(function() {
		//ask for updating after 5 ms
		setInterval(runAjax,5000);
});
var username;
function runAjax() {
	$.ajax({
		type: "post",
		url: "/",
		dataType: "json",
		data: {'request':0},
		success: function(result){
			username = result;
			window.location.href="/specialUserPage";   
		}
	});
}

