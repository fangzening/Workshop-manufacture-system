	$(".edit-save-1").hover(function () {
            $(this).attr("id", "#blue");
         });

         	$("#blue").hover(function() {
    		$(this).toggleClass("edit-save-1");
    	});




 var saveBotton1 = document.getElementsByClassName("save-button-1");
  var editSave1 = document.getElementsByClassName("edit-save-1");
  var saveBotton2 = document.getElementsByClassName("save-button-2");
  var editSave2 = document.getElementsByClassName("edit-save-2");
  var saveBotton3 = document.getElementsByClassName("save-button-3");
  var editSave3 = document.getElementsByClassName("edit-save-3");




  function showButton(x) {
  document.getElementById('save-button-1').style.display = "block";
  }

  function hideButton(x) {
  document.getElementById('save-button-1').style.display = "none";
  }



  document.getElementById("edit-save-1").addEventListener("mouseover", mouseOver1);
  document.getElementById("edit-save-1").onmouseout = function() {mouseOut1()};
  document.getElementById("edit-save-2").addEventListener("mouseover", mouseOver2);
  document.getElementById("edit-save-2").onmouseout = function() {mouseOut2()};
  document.getElementById("edit-save-3").addEventListener("mouseover", mouseOver3);
  document.getElementById("edit-save-3").onmouseout = function() {mouseOut3()};


  editSave1[0].addEventListener("mouseover", mouseOver1);
  editSave1[0].onmouseout = function() {mouseOut1()};


  function mouseOver1() {
  saveBotton1[0].style.display = "block";
  }
  function mouseOut1() {
  saveBotton1[0].style.display = "none";
    }

    function mouseOver2() {
  saveBotton2[0].style.display = "block";
  }
  function mouseOut2() {
  saveBotton2[0].style.display = "none";
    }

    function mouseOver3() {
   saveBotton3[0].style.display = "block";
  }
  function mouseOut3() {
  saveBotton3[0].style.display = "none";
    }


 function myFunction() {
  var x = document.getElementById("save-button-2");
  if (x.style.display === "none") {
    x.style.display = "block";
  } else {
    x.style.display = "none";
  }
}

function myFunction1() {
var x = document.getElementById("save-button-1");
if (x.style.display === "none") {
x.style.display = "block";
} else {
x.style.display = "none";
}
}