/*
Original Author: Dichong Song
Creation date: Jan 25th, 2019
Contents of file:
	1. AJAX call to send signal from front-end to back-end
	2. If login success, jumps to specialuserpage; otherwise, alert not correct
*/
var username;
var KEY_F2 = 113;
var KEY_Q = 81;
var KEY_S = 83;
var LOGIN_FAIL = "login_fail";
var LOGIN_SUCCESS = "login_success";
document.addEventListener('keydown', function(e) {
	if (e.keyCode == KEY_F2 || e.keyCode == KEY_Q){
	  runAjax(1)
	}
	else if(e.keyCode == KEY_S){
		document.getElementById('id01').style.display='block';
	}
});

function runAjax(REQUEST) {
	$.ajax({
		type: "post",
		url: "/",
		dataType: "json",
		data: {'request':REQUEST},
		success: function(result){
			if (result.mode == LOGIN_FAIL){
				alert("user not correct");
			}
			if (result.mode == LOGIN_SUCCESS) {
				username = result.username;
				console.log(username);
				window.location.href="/specialUserPage";
			}
		}
	});
}
// Get the modal
var modal = document.getElementById('id01');

// When the user clicks anywhere outside of the modal, close it
window.onclick = function(event) {
    if (event.target == modal) {
        modal.style.display = "none";
    }
}

setInterval(readFace, 2000);
function readFace() {
    runAjax(3)
}
