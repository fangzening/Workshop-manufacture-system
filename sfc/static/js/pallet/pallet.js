
function closeAllSelect(elmnt) {
  /*a function that will close all select boxes in the document,
  except the current select box:*/
  var x, y, i, xl, yl, arrNo = [];
  x = document.getElementsByClassName("select-items-pallet");
  y = document.getElementsByClassName("select-selected-pallet");
  xl = x.length;
  yl = y.length;
  for (i = 0; i < yl; i++) {
    if (elmnt == y[i]) {
      arrNo.push(i)
    } else {
      y[i].classList.remove("select-arrow-active");
    }
  }
  for (i = 0; i < xl; i++) {
    if (arrNo.indexOf(i)) {
      x[i].classList.add("select-hide-pallet");
    }
  }
}
/*if the user clicks anywhere outside the select box,
then close all select boxes:*/
document.addEventListener("click", closeAllSelect);



jQuery.fn.filterByText = function(repaircode, selectSingleMatch) {
    return this.each(function() {
        var select = this;
        var options = [];
        $(select).find('option').each(function() {
            options.push({value: $(this).val(), text: $(this).text()});
        });
        $(select).data('options', options);
        $(repaircode).bind('change keyup', function() {
            var options = $(select).empty().data('options');
            var search = $.trim($(this).val());
            var regex = new RegExp(search,"gi");

            $.each(options, function(i) {
                var option = options[i];
                if(option.text.match(regex) !== null) {
                    $(select).append(
                       $('<option>').text(option.text).val(option.value)
                    );
                }
            });
            if (selectSingleMatch === true && $(select).children().length === 1) {
                $(select).children().get(0).selected = true;
            }
        });
    });
};

$(function() {
    $('#id_serial_number').filterByText($('#repaircode'), true);
});

function getOption(sel) {
//        alert(sel.options[sel.selectedIndex].text);
    document.getElementById("repaircode").value = sel.options[sel.selectedIndex].text;
  }


//function getRepairCode(sel) {
//  var x = document.getElementById("id_serial_number").value;
//  var replacement = document.getElementById("replacement");
//  document.getElementById("repair").innerHTML = x;
//  document.getElementById("replacement-repair-code").value = document.getElementById("repaircode").value ;
//  replacement.style.display = "none";
//
//}


jQuery.fn.filterByText = function(pallet_id, selectSingleMatch) {
    return this.each(function() {
        var select = this;
        var options = [];
        $(select).find('option').each(function() {
            options.push({value: $(this).val(), text: $(this).text()});
        });
        $(select).data('options', options);
        $(pallet_id).bind('change keyup', function() {
            var options = $(select).empty().data('options');
            var search = $.trim($(this).val());
            var regex = new RegExp(search,"gi");

            $.each(options, function(i) {
                var option = options[i];
                if(option.text.match(regex) !== null) {
                    $(select).append(
                       $('<option onclick="getPalletInfo()" >').text(option.text).val(option.value)
                    );
                }
            });
            if (selectSingleMatch === true && $(select).children().length === 1) {
                $(select).children().get(0).selected = true;
            }
        });
    });
};

$(function() {
    $('#select').filterByText($('#pallet_id'), true);
});



function getPalletInfo(sel) {
  var x = document.getElementById("select").value;
  var replacement = document.getElementById("replacement");
  document.getElementById("pallet-info").innerHTML = x;
  document.getElementById("replacement-repair-code").value = document.getElementById("pallet_id").value ;
  replacement.style.display = "none";

}


  function getOption(sel) {
//        alert(sel.options[sel.selectedIndex].text);
        document.getElementById("repaircode").value = sel.options[sel.selectedIndex].text;
      }
function ShowNew() {



var x = document.getElementById("create_pallet_id");
var y = document.getElementById("open_input");
  if (x.style.display === "block") {
  x.style.display = "block";
  y.style.display = "block";

 } else {
  x.style.display = "block";
  y.style.display = "block";

 }

}

function GenerateID() {

var chars = "0123456789abcdefghiklmnopqrstuvwxyz";
var string_length = 8;
var randomstring = '';
for (var i=0; i<string_length; i++) {
		var rnum = Math.floor(Math.random() * chars.length);
		randomstring += chars.substring(rnum,rnum+1);
	}
	document.create.pallet_id.value = 'P_' + randomstring;
//    document.create.pallet_id.value = 'pallet_002';

}

function ShowDimensions() {
  var x = document.getElementById("dimensions");
  var y = document.getElementById("open-pallet");
  var openAvailable = document.getElementById("open-available-pallet");
  var closePallet = document.getElementById("close-pallet");
  var generatePalletId = document.getElementById("generate-id");
  var saveDimension = document.getElementById("save-dimension");


  if (x.style.display === "block") {
  x.style.display = "block";
  saveDimension.style.display = "none";

//  closePallet.display = "block";
//  generatePalletId = "block";
  y.style.display = "block";
  openAvailable.style.display = "block";

 } else {
  x.style.display = "block";
  saveDimension.style.display = "none";

//  closePallet.display = "none";
//  generatePalletId = "none";
  y.style.display = "block";
  openAvailable.style.display = "block";
 }

  }



function getPalletDetail() {
    var input, filter, ul, li, a, i, txtValue;
    input = document.getElementById("pallet_id");
    filter = input.value.toUpperCase();
    ul = document.getElementById("myUL");
    li = ul.getElementsByTagName("li");
    for (i = 0; i < li.length; i++) {
        a = li[i].getElementsByTagName("a")[0];
        txtValue = a.textContent || a.innerText;
        if (txtValue.toUpperCase().indexOf(filter) > -1) {
            li[i].style.display = "";
        } else {
            li[i].style.display = "none";
        }
    }
}


function getPalletClosedDetail() {
    var input, filter, ul, li, a, i, txtValue;
    input = document.getElementById("closed_pallet_id");
    filter = input.value.toUpperCase();
    ul = document.getElementById("closedPalletInfo");
    li = ul.getElementsByTagName("li");
    for (i = 0; i < li.length; i++) {
        a = li[i].getElementsByTagName("a")[0];
        txtValue = a.textContent || a.innerText;
        if (txtValue.toUpperCase().indexOf(filter) > -1) {
            li[i].style.display = "";
        } else {
            li[i].style.display = "none";
        }
    }
}

function getNotInPalletDetail() {
    var input, filter, ul, li, a, i, txtValue;
    input = document.getElementById("not_in_pallet");
    filter = input.value.toUpperCase();
    ul = document.getElementById("NotInPalletInfo");
    li = ul.getElementsByTagName("li");
    for (i = 0; i < li.length; i++) {
        a = li[i].getElementsByTagName("a")[0];
        txtValue = a.textContent || a.innerText;
        if (txtValue.toUpperCase().indexOf(filter) > -1) {
            li[i].style.display = "";
        } else {
            li[i].style.display = "none";
        }
    }
}



$(document).ready(function(){
    $("#repaircode").keyup(function(){
        // Getting the current value of textarea
        var currentText = $(this).val();
        $(document).ready(function(){
          $('#repaircode').click(function(){
          $('input[name="serialnumber"]').val(currentText);
           });
        });

        // Setting the Div content
        $(".output").text(currentText);
        $('input[type=text].serial_number').val(currentText);
        $('#serial_number').attr('value', currentText )
    });
});




function ShowResult() {
var x = document.getElementById("last_sku").value;
var y = document.getElementById("first_sku").value;
  if (x === y) {
  document.getElementById('compare').innerHTML = "";

 } else {
 document.getElementById('compare').innerHTML = "different";


 }
 }



var x = document.getElementById("last_sku").value;
var y = document.getElementById("first_sku").value;
//var skuInput = document.getElementById('sn_model').innerHTML;
 if (x === y) {
  document.getElementById('compare').innerHTML = "";

 } else {
// document.getElementById('compare').innerHTML = ' <div id="myModal" class="modal-pallet"><div class="modal-content-pallet">'+
//                               '  <span class="close" data-dismiss="modal" style="z-index: 100;">×</span> '+
//                               ' <div class="warning-modal-body"> <p>Please make sure using the same Sku.</p></div>'+
//                               ' </div>  <button style="display: none;" id="myBtn">Open Modal</button></div>';
// var NewSKU = String(skuInput);
// var SKUtab = document.getElementById(NewSKU).value;
// if(x == SKUtab){
// document.getElementById(NewSKU).style.background ='#222';
//document.getElementById(NewSKU).style.color ='#fff';
// }
//document.getElementsByClassName('highlight').style.background = 'red';
//document.getElementById("last_sku").style.background ='#222';
//document.getElementById("last_sku").style.color ='#fff';
 }



 function highlightDuplicates() {

	 $('#myTable .tbody tr').each(function(index1){
      var row = $(this)
      var row_val1 = row.find("td:nth-last-child(1) input").val()
      var row_val2 = row.find("td:nth-last-child(2) input").val()
      $('#myTable .tbody tr').each(function(index2){

         var compare_row = $(this)
         var compare_row_val1 = compare_row.find("td:nth-child(1) input").val()
         var compare_row_val2 = compare_row.find("td:nth-child(2) input").val()

         if(index1!=index2 && row_val1==compare_row_val1 && row_val2==compare_row_val2){

            row.addClass('duplicate')
            compare_row.addClass('duplicate')
         }
      })
   })

   if($('tr.duplicate').length>0){
      alert('Duplicates found')
   }
 }


 $(document).ready(function() {
        var tableRows = $("#sortable tbody tr"),
            // we know exactly how large to make it, so don't use []
            htmlStrings = new Array(tableRows.length),
            i, j, current, comparing;

        for (i = 0; i < tableRows.length; i++) {
            current = htmlStrings[i];
            // get each innerHTML just once
            if (!current) {
                current = {
                    html: tableRows.get(i).innerHTML,
                    isDup: false
                };
                htmlStrings[i] = current;
            }

            // if we already know it's a dup, so we're done
            if (current.isDup) { continue; }

            // start j at i+1 since we've already looked at the previous i rows
            for (j = i + 1; j < tableRows.length; j++) {
                // could stay DRY and put this into a function;
                // doing so may decrease performance (not benchmarked)
                comparing = htmlStrings[j];
                if (!comparing) {
                    comparing = {
                        html: tableRows.get(j).innerHTML,
                        isDup: false
                    };
                    htmlStrings[j] = comparing;
                }

                if (comparing.isDup) { continue; }

                // It comes to this: we must actually compare now.
                if (current.html === comparing.html) {
                    current.isDup = true;
                    comparing.isDup = true;

                    // mark it
                    tableRows.eq(j).css('backgroundColor', 'red');
                }
            }

            if (current.isDup) {
                // mark it
                tableRows.eq(i).css('backgroundColor', 'red');
            }

        }
    });



