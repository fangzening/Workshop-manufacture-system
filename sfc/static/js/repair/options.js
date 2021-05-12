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
  $('#select').filterByText($('#repaircode'), true);
});


jQuery.fn.filterByText = function(outpn, selectSingleMatch) {
  return this.each(function() {
      var select = this;
      var options = [];
      $(select).find('option').each(function() {
          options.push({value: $(this).val(), text: $(this).text()});
      });
      $(select).data('options', options);
      $(outpn).bind('change keyup', function() {
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
  $('#selectout').filterByText($('#outpn'), true);
});


function getRepairCode(sel) {
  var x = document.getElementById("select").value;
  var replacement = document.getElementById("replacement");
  document.getElementById("repair").innerHTML = x;
  // // document.getElementById("replacement-repair-code").value = document.getElementById("repaircode").value ;
  // // replacement.style.display = "none";
  document.getElementById("repaired_description").focus();
  let isReplacement = Number(document.getElementById('is-replacement').value);
  document.getElementById('repair-unit').style.display="block";
  if (!isReplacement){
    // document.getElementById('showReplacement').style.display = "none";
    HideReplacement();
    document.getElementById('repair-select').style.display="none";
  }else{
    Replacement();
    // document.getElementById('form-replace-part').style.display = ""
  }
  // let isReplacement = document.getElementById('repair-' + 0);
}


function getOutPart(sel) {
  var x = document.getElementById("selectout").value;
  //  var outPart = document.getElementById("replacement-out-part").value;
  //  var outPartCSN = document.getElementById("replacement-outcsn").value;
  var replacement = document.getElementById("csn");
  var replacement = document.getElementById("csn-info");
  document.getElementById("repaircsn").innerHTML = x;
  document.getElementById("replacement-out-part").value = document.getElementById("outpn").value ;
  document.getElementById("replacement-repair-code").value = document.getElementById("repaircode").value ;
  replacement.style.display = "block";
  var outPart = document.getElementById("replacement-out-part").value;
  //  var outPartCSN = document.getElementById("replacement-outcsn").value;
  // var outPart = document.getElementById("replacementOutPart").value;
  // var outPartCSN = document.getElementById("replacementOutcsn").value;
  document.getElementById('outputOutPartNo').value = outPart;
  //document.getElementById('outputOutPartCSN').value = outPartCSN;


  for (var i = 0; i <keyparts.length; i++){
  // look for the entry with a matching `code` value
  if (keyparts[i].part_no == ''){
    // we found it
    // obj[i].name is the matched result
}
}

}

function getOutPartOption(sel) {
//        alert(sel.options[sel.selectedIndex].text);
      document.getElementById("outpn").value = sel.options[sel.selectedIndex].text;
    }

// function getOption() {
//  var x = document.getElementById("select").value;
//  var input = document.getElementById("repaircode");
//  document.getElementById("repaircode").value = "Johnny Bravo";
//  input.value = x;
//}

function getOption(sel) {
//        alert(sel.options[sel.selectedIndex].text);
      document.getElementById("repaircode").value = sel.options[sel.selectedIndex].text;
    }



function Replacement() {
var x = document.getElementById("replacement");
var showRe = document.getElementById('showReplacement');
var hideRe = document.getElementById('hideReplacement');

if (x.style.display === "block") {
  var inPN = document.getElementById("in-pn").value;
  document.getElementById("divText").value = inPN;
  x.style.display = "none";
  hideRe.style.display = "none"
  showRe.style.display = "block"
} else {
  var inPN = document.getElementById("in-pn").value;
  document.getElementById("divText").value = inPN;
  x.style.display = "block";
  hideRe.style.display = "block"
  showRe.style.display = "none"
}

let outcsn = document.getElementById('replacement-outcsn').value;
document.getElementById('outputOutPartCSN').value = outputOutPartCSN;
//  var opt;
//  var sel = document.getElementById('select');
//  var el = document.getElementById('replacement-repair-code');
//        for ( var i = 0, len = sel.options.length; i < len; i++ ) {
//            opt = sel.options[i];
//            if ( opt.selected === true ) {
//                break;
//            }
//        }
//        return opt;
//  document.getElementById('showTxt')=
//        // access text property of selected option
//        el.value = sel.options[sel.selectedIndex].text;

}

function HideReplacement() {
var x = document.getElementById("replacement");
var showRe = document.getElementById('showReplacement');
var hideRe = document.getElementById('hideReplacement');

if (x.style.display === "none") {
//    var inPN = document.getElementById("in-pn").value;
//    document.getElementById("divText").innerHTML = inPN;
  x.style.display = "block";
  hideRe.style.display = "block"
  showRe.style.display = "none"
} else {
//    var inPN = document.getElementById("in-pn").value;
//    document.getElementById("divText").innerHTML = inPN;
  x.style.display = "none";
  hideRe.style.display = "none"
  showRe.style.display = "block"
}
}

function replacePart(event){
// let replacePartBtn = document.getElementById('btn-replace-part');

// let failure_sequence = document.getElementById('failure_sequence');
// let repaired_code = document.getElementById('repaired_code');
// let repaired_code = document.getElementById('repaired_code').value;
// let repaired_description = document.getElementById('repaired_description').value; 
// let replacement = document.getElementById('replacement').value;
let repaired_code = document.getElementById('replacement-repair-code').value;
// let repaired_description = "Desc";
let out_part_no = document.getElementById('replacement-out-part').value;
let out_part_sn = document.getElementById('replacement-out-sn').value;
let in_part_no = document.getElementById('replacement-in-part').value;
let in_part_sn = document.getElementById('replacement-in-sn').value;
let template = document.getElementsByName('template')[0].value;
let route_id = document.getElementsByName('route')[0].value;
let station_id = document.getElementsByName('station')[0].value;
let model = document.getElementsByName('model')[0].value;
let failure_sequence = document.getElementsByName('failure_sequence')[0].value;
let serial_number  = document.getElementsByName('serial_number')[0].value;
let csrf = document.getElementsByName('csrfmiddlewaretoken')[0].value;

var data = {
  'csrf': csrf,
  'serial_number': serial_number,
  'out_part_no': out_part_no,
  'out_part_sn': out_part_sn,
  'part': in_part_no,
  'kp_serialnumber': in_part_sn,
  'template':template,
  'route_id': route_id,
  'station_id': station_id,
  'model': model,
  'failure_sequence': failure_sequence,
  'repaired_code': repaired_code,
  // 'repaired_description': repaired_description
}

data = JSON.stringify(data);

var xhttp = new XMLHttpRequest();
xhttp.onreadystatechange = function() {
  if (this.readyState == 4 && this.status == 200) {
    document.getElementById('outputOutPartCSN').value = out_part_sn;
    document.getElementById('outputOutPartCSN').value = out_part_sn;
    document.getElementsByClassName('repair-input-into')[8].innerHTML = in_part_no;
    document.getElementsByClassName('repair-input-into')[9].innerHTML = in_part_sn;
    
    alert(this.responseText);
  }
};
// http://127.0.0.1:8000
xhttp.open("POST", "replace-part", true);
xhttp.setRequestHeader("X-CSRFToken", csrf);
xhttp.send(data);


// $.ajax({
//   type: "POST",
//   url: 'replace-part',
//   data: {
//   'csrf': csrf,
//   'serial_number': serial_number,
//   'out_part_no': out_part_no,
//   'out_part_sn': out_part_sn,
//   'in_part_no': in_part_no,
//   'in_part_sn': in_part_sn,
//   'template':template,
//   'route_id': route_id,
//   'station_id': station_id,
//   'model': model,
//   'failure_sequence': failure_sequence,
//   'repaired_code': repaired_code,
//   'repaired_description': repaired_description
//   },
// success: function(result) {
//   console.log("Success");
//     console.log("HELLOOOOO");
//   //       if ( typeof result == "object"){
//   //           if (!result.length > 0){
//   //                 showError("There are no serial numbers for this workorder.")
//   //                 return
//   //           }
//   //           printWorkorder(result, selected_label_type, no_of_copies);
//   //       }else{
//   //           showError(result);
//   //       }
//   // }
// }
// });
}
