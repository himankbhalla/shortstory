$(document).ready(function(){

function getCookie(name) {
    var cookieValue = null;
    if (document.cookie && document.cookie != '') {
        var cookies = document.cookie.split(';');
        for (var i = 0; i < cookies.length; i++) {
            var cookie = jQuery.trim(cookies[i]);
            // Does this cookie string begin with the name we want?
            if (cookie.substring(0, name.length + 1) == (name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
}
var csrftoken = getCookie('csrftoken');


$('.close').click(function(){
$('.commentinput input').val('');
});
function deletestory(storyID){
$.ajax({
  type:"POST",
  url:"/delete_story/",
  data:{"story":storyID},
  success: function(){
  $("#story-box-" + storyID).hide();
  },
  headers:{
  'X-CSRFToken' :csrftoken
  }
});
return false;

}

function deletecomment(commentID){
$.ajax({
  type:"POST",
  url:"/delcomment/",
  data:{"comment":commentID},
  success: function(){
  $("#comment-box-" + commentID).hide();
  },
  headers:{
  'X-CSRFToken' :csrftoken
  }
});
return false;
}
$(document).on('click',"#storyformbutton",function(){
$('#addstoryform').toggleClass('hid');
$('#placeholder').toggleClass('displace_neg');

});
$(document).on('click',"#storyformmob",function(){
$('#addstoryform').toggleClass('hid');
$('#addstoryform').toggleClass('displace_neg_correct');
$('#placeholder').toggleClass('displace_mob_neg');

});

$(document).on('click',"button.delete-story",function(){

var storyID=parseInt(this.id.split("-")[2]);
console.log(storyID);

return deletestory(storyID);

})

$(document).on('click',"button.delete-comment",function(){

var commentID=parseInt(this.id.split("-")[2]);
console.log(commentID);

return deletecomment(commentID);

})


function storyvote(storyID){
$.ajax({
  type:"POST",
  url:"/vote_story/",
  data:{"story":storyID},
  success: function(result){

    $('#vote-story-' + storyID).addClass('btn-primary');
    $('#heart-story-' + storyID).removeClass('emptyheart');
      $('#heart-story-' + storyID).addClass('filledheart');
      $('#like-hid-' + storyID + '> span.likes.first' ).addClass('hid');
      $('#like-hid-' + storyID + '> span.likes.last').removeClass('hid'); 
        
    },
  headers:{
  'X-CSRFToken' :csrftoken
  }
});
return false;

}
function storybook(storyID){
$.ajax({
  type:"POST",
  url:"/book_story/",
  data:{"story":storyID},
  success: function(result){
    console.log(result);
    $('#bookbutton-story-' + storyID).addClass('btn-primary');
    $('#book-story-' + storyID).removeClass('emptybook');
      $('#book-story-' + storyID).addClass('filledbook');
       $('#book-hid-' + storyID + '> span.book.first' ).addClass('hid');
      $('#book-hid-' + storyID + '> span.book.last').removeClass('hid');

    },
  headers:{
  'X-CSRFToken' :csrftoken
  }
});
return false;

}
$(document).on('click',"button.votestory",function(){
var storyID=parseInt(this.id.split("-")[2]);
console.log(storyID);

return storyvote(storyID);

})
$(document).on('click',"button.report",function(){
var storyID=parseInt(this.id.split("-")[2]);
console.log(storyID);
$(".framed input:first-child").val(""+storyID);
$(".framed input:nth-child(2)").val("" + csrftoken);
//$('#form-report-' + storyID).removeClass('framed');
$('#form-report-' + storyID).slideToggle("slow");

})
$(document).on('click',"button.bookstory",function(){
var storyID=parseInt(this.id.split("-")[2]);
console.log(storyID);

return storybook(storyID);

})



});

