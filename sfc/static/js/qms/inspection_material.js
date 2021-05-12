// #############################
jQuery.fn.filterByText = function(MaterialQuery, selectSingleMatch) {
    return this.each(function() {
        var select = this;
        var options = [];
        $(select).find('option').each(function() {
            options.push({value: $(this).val(), text: $(this).text()});
        });
        $(select).data('options', options);
        $(MaterialQuery).bind('change keyup', function() {
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
    $('#searchMaterialQuery').filterByText($('#MaterialQuery'), true);
});

function getMaterialQuery(sel) {
//        alert(sel.options[sel.selectedIndex].text);
    document.getElementById("MaterialQuery").value = sel.options[sel.selectedIndex].text;
  }

var input = document.getElementById("MaterialQuery");
input.addEventListener("keyup", function(event) {
  if (event.keyCode === 13) {
   event.preventDefault();
   document.getElementById("goMenu").click();
  }
});




var input = document.getElementById("ManufactureQuery");
input.addEventListener("keyup", function(event) {
  if (event.keyCode === 13) {
   event.preventDefault();
   document.getElementById("goMenu").click();
  }
});

function getManufactureInfo(sel) {
//        alert(sel.options[sel.selectedIndex].text);
    document.getElementById("ManufactureInfo").value = sel.options[sel.selectedIndex].text;
  }


//############################################
