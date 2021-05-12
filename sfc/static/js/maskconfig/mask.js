
// create mask form
jQuery.fn.filterByText = function(scan_model_input, selectSingleMatch) {
    return this.each(function() {
        var select = this;
        var options = [];
        $(select).find('option').each(function() {
            options.push({value: $(this).val(), text: $(this).text()});
        });
        $(select).data('options', options);
        $(scan_model_input).bind('change keyup', function() {
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
    $('#searchID').filterByText($('#scan_model_input'), true);
});

function getModel(sel) {
//        alert(sel.options[sel.selectedIndex].text);
    document.getElementById("scan_model_input").value = sel.options[sel.selectedIndex].text;
  }

var input = document.getElementById("scan_model_input");
input.addEventListener("keyup", function(event) {
  if (event.keyCode === 13) {
   event.preventDefault();
   document.getElementById("model_button").click();
  }
});

// create manufacture form
jQuery.fn.filterByText = function(scan_material_input, selectSingleMatch) {
    return this.each(function() {
        var select = this;
        var options = [];
        $(select).find('option').each(function() {
            options.push({value: $(this).val(), text: $(this).text()});
        });
        $(select).data('options', options);
        $(scan_material_input).bind('change keyup', function() {
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
    $('#searchID_material').filterByText($('#scan_material_input'), true);
});

function getMaterial(sel) {
//        alert(sel.options[sel.selectedIndex].text);
    document.getElementById("scan_material_input").value = sel.options[sel.selectedIndex].text;
  }

var input_material = document.getElementById("scan_material_input");
input_material.addEventListener("keyup", function(event) {
  if (event.keyCode === 13) {
   event.preventDefault();
   document.getElementById("model_button").click();
  }
});
