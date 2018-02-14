$(function() {
        $('#FavCat').click(function(){
          $.post("/library/favCat",{id:document.getElementById("category").value},
            function(data) {
              alert(data);
            });
        });
      });
