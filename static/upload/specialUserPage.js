document.addEventListener('keydown', function(e) {
	if (e.keyCode == 113 || e.keyCode == 81){
	  e.keypress = '1';
	  alert("pressed");
	  runAjax(1)
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