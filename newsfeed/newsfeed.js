var newsString = ['Here are the latest news','Yue Ma','Hello','World'];
var newsCounter = 0;
setInterval(myTimer, 1500);

function myTimer() {
    if(newsCounter<newsString.length-1){
        newsCounter+=1;
    }
    else{
        newsCounter=0;
    }
    document.getElementById("newsTitle").innerHTML = newsString[newsCounter];
}