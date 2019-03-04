/*
Original Author: Shengyao Lu
Creation date: Jan 25th, 2019
Contents of file:
	1. AJAX call to send signal from front-end to back-end
*/
var KEY_ENTER = 13;
var FRONT_END_MSG_RESPOND = 3;
var FRONT_END_MSG_TAKE_PHOTO = 2;
var TAKE_PHOTO_SUCCESS = "photo_success";
var LOGOUT_SUCCESS = "logout_success";
document.addEventListener('keydown', function(e) {
	if (e.keyCode == KEY_ENTER){
	  e.keypress = '1';
	  runAjax(FRONT_END_MSG_TAKE_PHOTO);
	}
});

function runAjax(REQUEST) {
	$.ajax({
		type: "post",
		url: "/",
		dataType: "json",
		data: {'request':REQUEST},
		success: function(result){
			if (result.mode == TAKE_PHOTO_SUCCESS){
				alert("A photo has been taken.\
				 We will implement a way for you to check it later!");
			}
			if (result.mode == LOGOUT_SUCCESS) {
				window.location.href="/";
			}
		}
	});
}

setInterval(readFace, 2000);
function readFace() {
    runAjax(FRONT_END_MSG_RESPOND);
}
