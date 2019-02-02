$(function() {	
		//定时请求刷新
		setInterval(runAjax,10000);	
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

