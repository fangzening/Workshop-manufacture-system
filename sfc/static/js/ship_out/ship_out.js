
function closeAllSelect(elmnt) {

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
    $('#id_salesorder').filterByText($('#repaircode'), true);
});

function getTest(sel) {
//        alert(sel.options[sel.selectedIndex].text);
    document.getElementById("repaircode").value = sel.options[sel.selectedIndex].text;
  }

var input = document.getElementById("repaircode");
input.addEventListener("keyup", function(event) {
  if (event.keyCode === 13) {
   event.preventDefault();
   document.getElementById("so_button").click();
  }
});

// scan so ####################################################

jQuery.fn.filterByText = function(salesorder, selectSingleMatch) {
    return this.each(function() {
        var select = this;
        var options = [];
        $(select).find('option').each(function() {
            options.push({value: $(this).val(), text: $(this).text()});
        });
        $(select).data('options', options);
        $(salesorder).bind('change keyup', function() {
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
    $('#id_id_salesorder').filterByText($('#salesorder'), true);
});

function getSO(sel) {
//        alert(sel.options[sel.selectedIndex].text);
    document.getElementById("salesorder").value = sel.options[sel.selectedIndex].text;
  }

var input = document.getElementById("salesorder");
input.addEventListener("keyup", function(event) {
  if (event.keyCode === 13) {
   event.preventDefault();
   document.getElementById("so_button").click();
  }
});
// test bug ###################################################
jQuery.fn.filterByText = function(salesorder, selectSingleMatch) {
    return this.each(function() {
        var select = this;
        var options = [];
        $(select).find('option').each(function() {
            options.push({value: $(this).val(), text: $(this).text()});
        });
        $(select).data('options', options);
        $(salesorder).bind('change keyup', function() {
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
    $('#test_select').filterByText($('#salesorder'), true);
});

function getTest(sel) {
//        alert(sel.options[sel.selectedIndex].text);
    document.getElementById("salesorder").value = sel.options[sel.selectedIndex].text;
  }

var input = document.getElementById("salesorder");
input.addEventListener("keyup", function(event) {
  if (event.keyCode === 13) {
   event.preventDefault();
   document.getElementById("go").click();
  }
});

// scan pallet #################################################

jQuery.fn.filterByText = function(scan_pallet_input, selectSingleMatch) {
    return this.each(function() {
        var select = this;
        var options = [];
        $(select).find('option').each(function() {
            options.push({value: $(this).val(), text: $(this).text()});
        });
        $(select).data('options', options);
        $(scan_pallet_input).bind('change keyup', function() {
            var options = $(select).empty().data('options');
            var search = $.trim($(this).val());
            var regex = new RegExp(search,"gi");

            $.each(options, function(i) {
                var option = options[i];
                if(option.text.match(regex) !== null) {
                    $(select).append(
                       $('<option>').text(option.text).val(option.value)
                    );
                }else{
                  $("body").css("background", "orange");
                }
            });
            if (selectSingleMatch === true && $(select).children().length === 1) {
                $(select).children().get(0).selected = true;
            }else{
            $("body").css("background", "orange");

            }
        });
    });
};

$(function() {
    $('#id_scan_pallet').filterByText($('#scan_pallet_input'), true);
});

function getPalletTableB(sel) {
//        alert(sel.options[sel.selectedIndex].text);
    document.getElementById("scan_pallet_input").value = sel.options[sel.selectedIndex].text;
    var option = document.getElementById("id_scan_pallet").value
    if(option){
    }else{
    document.getElementById("count-number1").innerHTML = '<div id="myModal" class="modal-keypart" style="padding-top: 0"><div class="modal-content"  style="width: 100%;"><span class="close" data-dismiss="modal" style="z-index: 100; top: 10px;"></span><div class="warning-modal-body"><p>The Pallet does not exist. </p></div></div><button style="display: none;" id="myBtn">Open Modal</button></div>';
    }
  }

var input = document.getElementById("scan_pallet_input");
input.addEventListener("keyup", function(event) {
  if (event.keyCode === 13) {
   event.preventDefault();
   document.getElementById("pallet_button").click();
  }
});
//######################### scan SN #############################################
jQuery.fn.filterByText = function(t1, selectSingleMatch) {
    return this.each(function() {
        var select = this;
        var options = [];
        $(select).find('option').each(function() {
            options.push({value: $(this).val(), text: $(this).text()});
        });
        $(select).data('options', options);
        $(t1).bind('change keyup', function() {
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
    $('#id_scan_sn').filterByText($('#t1'), true);
});
function getPalletTableC(sel) {
//        alert(sel.options[sel.selectedIndex].text);
    document.getElementById("t1").value = sel.options[sel.selectedIndex].text;
  }



//var input = document.getElementById("t1");
//input.addEventListener("keyup", function(event) {
//  if (event.keyCode === 13) {
//   event.preventDefault();
//   document.getElementById("highlight").click();
//  }
//});


//######################### scan SN inside the Pallet menu #############################################
jQuery.fn.filterByText = function(sn_in_pallet, selectSingleMatch) {
    return this.each(function() {
        var select = this;
        var options = [];
        $(select).find('option').each(function() {
            options.push({value: $(this).val(), text: $(this).text()});
        });
        $(select).data('options', options);
        $(sn_in_pallet).bind('change keyup', function() {
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
    $('#id_scan_sn_in_pallet').filterByText($('#sn_in_pallet'), true);
});
function getPalletTableD(sel) {
//        alert(sel.options[sel.selectedIndex].text);
    document.getElementById("sn_in_pallet").value = sel.options[sel.selectedIndex].text;
  }



var input = document.getElementById("sn_in_pallet");
input.addEventListener("keyup", function(event) {
  if (event.keyCode === 13) {
   event.preventDefault();
   document.getElementById("highlight_inside").click();
  }
});


// ####################### sku no #############################
 function getSkuDetail() {
    var input, filter, ul, li, a, i, txtValue;
    input = document.getElementById("sku_filter_detail");
    filter = input.value.toUpperCase();
    ul = document.getElementById("sku_ul");
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
//################## jquery




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
    $('#select').filterByText($('#pallet_id'), true);
});


function getOption(sel) {
//        alert(sel.options[sel.selectedIndex].text);
    document.getElementById("repaircode").value = sel.options[sel.selectedIndex].text;
  }


$(document).ready(function(){
    $("#repaircode").keyup(function(){
        // Getting the current value of textarea
        var currentText = $(this).val();
        $(document).ready(function(){
          $('#repaircode').click(function(){
          $('input[name="so_input"]').val(currentText);
           });
        });

        // Setting the Div content
        $(".output").text(currentText);
        $('input[type=text].serial_number').val(currentText);
        $('#serial_number').attr('value', currentText )
    });
});








