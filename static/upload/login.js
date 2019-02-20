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
	  runAjax(1)
	}
	else if(e.keyCode == 83){
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
			username = result;
			console.log('frontEnd');
			console.log(username)

			window.location.href="/specialUserPage";
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
