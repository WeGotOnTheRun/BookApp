$(function() {
        $('#FavCat').click(function(){
          $.post("/favCat",{id:document.getElementById("category").value},
            function(data) {
              alert(data);
            });
        });
      });
