$(function() {
        $('#FavCat').click(function(){
            var id =$('#category').val();
            if($(this).attr('name')==1){
                $('#FavCat').attr('name',"2")
          $.post("/favCat",{id:id},
            function(data) {
              alert(data);
            });}
          else
          {
            $('#FavCat').attr('name',"1")
             $.post("/deleteRead",{id:id},
            function(data) {
              alert(data);
            });
          }

        });
      });