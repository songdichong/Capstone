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
var KEY_ENTER = 13;
var FRONT_END_MSG_RESPOND = 3;
var FRONT_END_MSG_REISTER = 1;
var LOGIN_FAIL = "login_fail";
var LOGIN_SUCCESS = "login_success";
var REGISTER_SUCCESS = "register_success";
var UPDATES_SUCCESS = "update_success";
document.addEventListener('keydown', function(e) {
	if (e.keyCode == KEY_F2 || e.keyCode == KEY_Q){
	  runAjax(FRONT_END_MSG_REISTER);
	  clearInterval(keeppost);
	}
	else if(e.keyCode == KEY_ENTER){
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
				setTimeout(function(){ alert("User cannot be recognized.\n Please register first!");}, 3000);
			}
			if (result.mode ==  REGISTER_SUCCESS){
				username = result.username;
				setTimeout(function(){ alert("register success\n Your username is:"+username); }, 3000);
			}
			if (result.mode == UPDATES_SUCCESS){
				username = result.username;
				setTimeout(function(){ alert("update success\n Your new information is:" + username);}, 3000);
			}
			
			if (result.mode == LOGIN_SUCCESS) {
				username = result.username;
				useremail = result.email;//Yue add
				userpreference = result.preference;//Yue add

				console.log(username);
				window.location.href="/specialUserPage?/"+username+"/"+useremail+"/"+userpreference;
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

var keeppost = setInterval(readFace, 2000);
function readFace() {
    runAjax(FRONT_END_MSG_RESPOND);
}
