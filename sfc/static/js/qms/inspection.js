
      function showMRBResult(selectObj) {
        var selectIndex=selectObj.selectedIndex;
        var selectValue=selectObj.options[selectIndex].text;

        if(selectValue=="Accept"){
           content1 = '';
           content2 = '';

        }
        else if(selectValue=="Selected"){
           content1 = '<table class="table table-striped table-bordered table-sm  table-pallet"  style="margin:0; padding: 0;">';
           content1 += '<thead> <tr class="table-header"><th>Material Number</th><th>Pass Qty</th><th>Remark</th> <th>Creator</th></tr> </thead>';
           content1 += '<tbody><tr><td>data</td><td></td><td></td><td></td></tr></tbody></table>';

           content2 = '<table class="table table-striped table-bordered table-sm table-pallet"  style="margin:0; padding: 0;">';
           content2 += '<thead> <tr class="table-header"><th>Material Number</th><th>Pass Qty</th><th>Remark</th> <th>Creator</th></tr> </thead>';
           content2 += '<tbody><tr><td>data11</td><td></td><td></td><td></td></tr></tbody></table>';
        }else if (selectValue == "Reject") {
           content1 = '';
           content2 = '';
        }
       showMRB1.innerHTML=content1;
       showMRB2.innerHTML=content2;
      }


// #############################

jQuery.fn.filterByText = function(query_input, selectSingleMatch) {
    return this.each(function() {
        var select = this;
        var options = [];
        $(select).find('option').each(function() {
            options.push({value: $(this).val(), text: $(this).text()});
        });
        $(select).data('options', options);
        $(query_input).bind('change keyup', function() {
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
    $('#searchQuery').filterByText($('#query_input'), true);
});

function getQuery(sel) {
//        alert(sel.options[sel.selectedIndex].text);
    document.getElementById("query_input").value = sel.options[sel.selectedIndex].text;
  }

var input = document.getElementById("query_input");
input.addEventListener("keyup", function(event) {
  if (event.keyCode === 13) {
   event.preventDefault();
   document.getElementById("goMenu").click();
  }
});

// UL ########################################################################
function getSelectedModule() {
    var input, filter, ul, li, a, i, txtValue;
    input = document.getElementById("module-menu");
    filter = input.value.toUpperCase();
    ul = document.getElementById("ModuleInfo");
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

function getMaterialMaster() {
    var input, filter, ul, li, a, i, txtValue;
    input = document.getElementById("MaterialQuery");
    filter = input.value.toUpperCase();
    ul = document.getElementById("MaterialMasterInfo");
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


function getManufactureInfo() {
    var input, filter, ul, li, a, i, txtValue;
    input = document.getElementById("ManufactureQuery");
    filter = input.value.toUpperCase();
    ul = document.getElementById("ManufactureInfo");
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

function getMRB() {
    var input, filter, ul, li, a, i, txtValue;
    input = document.getElementById("MRBQuery");
    filter = input.value.toUpperCase();
    ul = document.getElementById("MRBInfo");
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




// #############################

function queryInspectionForm() {
    //add refresh
    var material_code = document.getElementById('query_input').value;
    document.getElementById('inspection_form_textbox').value = material_code;
    $.ajax({
        type: 'GET',
        data : {'material_number' : material_code},
        url: "http://127.0.0.1:8000/qms/getInspectionFormData/",
        success: function (response) {
            var form_status = response.status;
            document.getElementById('inspection_form_textbox').value = response.inspection_form;
            document.getElementById('part_number_textbox').value = response.part_number;
            document.getElementById('mtrl_qty_textbox').value = response.material_qty;
            document.getElementById('pass_qty_textbox').value = response.passed_qty;
            document.getElementById('status_textbox').value = response.status;
            document.getElementById('inspector_textbox').value = response.inspector;

            for (var temp in response.inspection_detail) {
                var table = document.getElementById('inspection_detail_table');
                var rowCnt = table.rows.length;
                var row = table.insertRow(rowCnt);
                var line_name = row.insertCell(0);
                var inspection_item = row.insertCell(1);
                var inspection_level = row.insertCell(2);
                var aql = row.insertCell(3);
                var tool = row.insertCell(4);
                var standard = row.insertCell(5);


                var sampling_number = row.insertCell(6);
                sampling_number.id = 'sampling_number_' + temp;
                var inspection_result = row.insertCell(7);
                inspection_result.id = 'inspection_result_' + temp;

                if (form_status == 'finished') {
                    sampling_number.innerHTML = response.inspection_detail[temp]['sampling_no'];
                    inspection_result.innerHTML = response.inspection_detail[temp]['inspection_result'];
                }
                else {
                    document.getElementById('sampling_number_' + temp).contentEditable = 'true';
                    document.getElementById('inspection_result_' + temp).contentEditable = 'true';
                }

                line_name.innerHTML = temp;
                inspection_item.innerHTML = response.inspection_detail[temp]['inspection_parameter'];
                inspection_level.innerHTML = response.inspection_detail[temp]['inspection_level'];
                aql.innerHTML = response.inspection_detail[temp]['aql'];
                tool.innerHTML = response.inspection_detail[temp]['inspection_tool'];
                standard = response.inspection_detail[temp]['inspection_standard'];
            }
        },
    });
}


function takeInspectionResult() {
    var table = document.getElementById('inspection_detail_table');
    var res_dict = {};
    res_dict['inspection_form'] = document.getElementById('inspection_form_textbox').value;
    var res_list = [];
    for (var r = 1, n = table.rows.length; r < n; r++) {
        res_dict['inspection_form'] = document.getElementById('inspection_form_textbox').value;
        res_dict['ins_params'] = table.rows[r].cells[1].innerHTML;
        res_dict['sampling_number'] = table.rows[r].cells[6].innerHTML;
        res_dict['result'] = table.rows[r].cells[7].innerHTML;
        if (table.rows[r].cells[7].innerHTML == "FAIL") {
            document.getElementById('status_textbox').value = 'Failed';
        }
    $.ajax({
        type: 'GET',
        data: res_dict,
        url: 'http://127.0.0.1:8000/qms/inspection_form/update/'
    })
    }

}

