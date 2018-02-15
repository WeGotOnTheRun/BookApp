$(function() {
        $('#makeFav').click(function(){
            var id =$('#book').val();
            console.log($(this).attr('name')==1);
            if($(this).attr('name')==1){
                $('#makeFav').attr('name',"2")
                $('#makeFav').attr('src',"/static/Appimages/Empty-Heart.png")
                console.log("oiojoiji");
          $.post("/delFav",{id:id},
            function(data) {
              alert(data);
            });}
          else
          {
            console.log("hj");
            $('#makeFav').attr('name',"1")
            $('#makeFav').attr('src',"/static/Appimages/RedHeart.png")
             $.post("/favourite",{id:id},
            function(data) {
              alert(data);
            });
          }

        });
      });

$(function() {
        $('#read').click(function(){
            var id =$('#book').val();
            console.log($(this).attr('name')=="1")
            if($(this).attr('name')==1){
                $('#read').attr('name',"2")
          $.post("/read",{id:id},
            function(data) {
              alert(data);
            });}
          else
          {
            $('#read').attr('name',"1")
             $.post("/deleteRead",{id:id},
            function(data) {
              alert(data);
            });
          }

        });
      });

$(function() {
        $('.star').click(function(){
          $(this).addClass('on rating');
          $(this).prevAll().addClass('on rating');
          $(this).nextAll().removeClass('on rating');
          $(this).parent().addClass('rated');
          var rate = $(this).siblings().add(this).filter('.rating').length
          $.post("/rate",{rate:rate,id:document.getElementById("book").value},
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
