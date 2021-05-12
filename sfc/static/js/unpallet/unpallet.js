// scan so ####################################################

jQuery.fn.filterByText = function(scan_pallet, selectSingleMatch) {
    return this.each(function() {
        var select = this;
        var options = [];
        $(select).find('option').each(function() {
            options.push({value: $(this).val(), text: $(this).text()});
        });
        $(select).data('options', options);
        $(scan_pallet).bind('change keyup', function() {
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
    $('#test_select').filterByText($('#scan_pallet'), true);
});

function getPallet(sel) {
//        alert(sel.options[sel.selectedIndex].text);
    document.getElementById("scan_pallet").value = sel.options[sel.selectedIndex].text;
  }

var input = document.getElementById("scan_pallet");
input.addEventListener("keyup", function(event) {
  if (event.keyCode === 13) {
   event.preventDefault();
   document.getElementById("go").click();
  }
});



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
