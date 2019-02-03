var newsString = '';
var newsCounter = 0;
var NewsTitle = 'CBC';
$.getJSON( "../static/upload/newsfeed/news.json", function( data ) {
    newsString = data;

});
setInterval(myTimer, 2000);
setInterval(newsUpdateTime, 1800000);
function myTimer() {

    if(newsCounter<newsString.length-1){
        newsCounter+=1;
    }
    else{
        newsCounter=0;
    }
    var currentNews = newsString[newsCounter];
    if(typeof(currentNews)!=='undefined' && currentNews.indexOf(NewsTitle)<0 ){
        document.getElementById("newsTitle").innerHTML = newsString[newsCounter];

    }
}

function newsUpdateTime() {

    $.getJSON( "../static/upload/newsfeed/news.json", function( data ) {
        newsString = data;

    });

}