document.getElementById("makeFav").addEventListener("click", function(){
    if (document.getElementById("makeFav").name==1){
      document.getElementById("makeFav").src="/static/Appimages/Empty-Heart.png";
      document.getElementById("makeFav").name="2";
    }
    else{
    document.getElementById("makeFav").src="/static/Appimages/RedHeart.png";
    var id=document.getElementById("book").value
    document.getElementById("makeFav").name="1";
    $.ajax({
    url:'/library/hello/'+id,
    success: function(data) {
        alert(data);
    },
    error: function(data) {
     alert("error")
    }
});
}

});
// 


$(function() {
        $('#read').click(function(){
          $.post("/library/read",{id:document.getElementById("book").value},
            function(data) {
              alert(data);
            });
        });
      });
$(function() {
        $('#read').click(function(){
          $.post("/library/favCat",{id:document.getElementById("book").value},
            function(data) {
              alert(data);
            });
        });
      });
$(function() {
        $('.star').click(function(){
          $(this).addClass('on rating');
          $(this).prevAll().addClass('on rating');
          $(this).nextAll().removeClass('on rating');
          $(this).parent().addClass('rated');
          var rate = $(this).siblings().add(this).filter('.rating').length
          $.post("/library/rate",{rate:rate,id:document.getElementById("book").value},
            function(data) {
              alert(data);
            });
        });
      });

      $(function() {
        $('.star').hover(
          function(){
            $(this).addClass('on');
            $(this).prevAll().addClass('on');
            $(this).nextAll().removeClass('on');
          },
          function(){
            $(this).siblings().add(this).removeClass('on');
            $(this).siblings().add(this).filter('.rating').addClass('on');
          }
        );
      });
