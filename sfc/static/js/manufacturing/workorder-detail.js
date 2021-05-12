 var model = document.getElementsByClassName("model-detail");
 var model = document.getElementById("{{ workorder.pk }}");
 var btn = document.getElementById("myBtn");
 var span = document.getElementsByClassName("close")[0];
 btn.onclick = function() {
      modal.style.display = "block";
  }

 span.onclick = function() {
       modal.style.display = "none";
  }


  window.onclick = function(event) {
       if (event.target == modal) {
modal.style.display = "none";
 }
}