document.addEventListener('keydown', function(e) {
	if (e.keyCode == 13){
	  e.keypress = '1';
	  alert("pressed");
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