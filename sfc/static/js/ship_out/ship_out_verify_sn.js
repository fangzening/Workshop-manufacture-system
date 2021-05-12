var main = {
   ValidateSN: function (sn, token) {
        error_section = $("#errorSection");
        console.log("error test 1 " + sn);
        error_section.children().remove();
        msg = '<div id="myModal" class="modal-log message-box-bottom"><div class="modal-content-error bottom-message">';
        msgEnd = "</div></div>";

        var found = 0;
        $('#pallet_table tbody tr').each(function () {
            console.log("En el Loop" + sn);
            console.log($(this).find('td').eq(2).text());
            if ($(this).find('td').eq(2).text() == sn) {
                  console.log($(this).find('td').eq(2).text() + "mas adentro " + sn);
                  $(this).css('background', '#222');
                  $(this).css('color', '#fff');
                  $('#count-number1').html('');


                  found = 1;
            }else if($(this).find('td').eq(2).text() != sn){
             //$('#count-number1').html('<div id="myModal" class="modal-shipout" style=""><div class="modal-content"  style="width: 100%;"><div class="warning-modal-body"><p>The SN does not exist in this pallet.</p></div></div><button style="display: none;" id="myBtn">Open Modal</button></div>');

            }
        });


        if (found == 0) {
            console.log("Error pallet no es igual" + sn);
            msg += "<p>SerialNumber " + sn + " not found</p>" + msgEnd;
            error_section.append(msg);
           // $('#count-number1').html('<div id="myModal" class="modal-shipout" style=""><div class="modal-content"  style="width: 100%;"><div class="warning-modal-body"><p>The SN does not exist in this pallet.</p></div></div><button style="display: none;" id="myBtn">Open Modal</button></div>');
            return 0;
        }
        else {
//            var pallet_rows = $('#pallet_table tbody tr').length;
//            let total_tr = $("#total_pallet_qty tbody");
//            tmpl = "";
//            total_tr.children().remove();
//            tmpl += "<tr><td>" + pallet_rows + "</td></tr>";
//            tot_table.append(tmpl);
            tot_table = $("tr[style='background: rgb(34, 34, 34); color: rgb(255, 255, 255);']").length;

//            tot_table = $('#scanned_pallet_qty tr:nth-child(1) td:nth-child(1)').text();
            palqty = $('#total_pallet_qty tr:nth-child(1) td:nth-child(1)').text();
            currentIntab = $('#salesoorder_detail_tab tr:nth-child(3) td:nth-child(3)').text();

            currentqty = parseInt(tot_table / 2);
//            currentqty = tot_table - 1;
            new_total = (currentqty);

            $('#scanned_pallet_qty tr:nth-child(1) td:nth-child(1)').text(currentqty);

            if ((parseInt(palqty, 10) > 0 && parseInt(new_total, 10) > 0) && parseInt(palqty, 10) == parseInt(new_total, 10)) {
                error_section.children().remove();

                msg = "";
                msg = '<div id="myModal" class="modal-log message-box-bottom"><div class="modal-content-success bottom-message">';
                msg += '<span class="close" data-dismiss="modal" style="z-index: 100;">×</span>';
                msg += '<div class="warning-modal-body">';
                msg += '<p class="card-title">All the SNs have need verified, Please save the pallet to the list.</p>';
                msg += "</div></div></div>";
               $('#btnGetCount').css('display', 'block');
               $('#count-number1').html('<div id="myModal" class="modal-keypart" style="padding-top: 0"><div class="modal-content-success"  style="width: 100%;"><span class="close" data-dismiss="modal" style="z-index: 100; top: 10px;"></span><div class="warning-modal-body"><p>All the SN(s) have been verified.</p></div></div><button style="display: none;" id="myBtn">Open Modal</button></div>');

                error_section.append(msg);
            }
            if((parseInt(palqty, 10)) > (parseInt(currentIntab, 10))){
              $('#count-number1').html('<div id="myModal" class="modal-keypart" style="padding-top: 0"><div class="modal-content"  style="width: 100%;"><span class="close" data-dismiss="modal" style="z-index: 100; top: 10px;"></span><div class="warning-modal-body"><p>The total amount exceeds the request qty.</p></div></div><button style="display: none;" id="myBtn">Open Modal</button></div>');
//              $('#btnGetCount').css('display', 'none');
            }
        }


        $.ajax({
            type: "POST",
            url: "/shipping/wip/shipout/validate_sn/",
            data: {
                'serialnumber': sn,

                'csrfmiddlewaretoken': token
            },
            dataType: 'json',
            success: function (result) {
                console.log("Begin: success from Truck Load");
                console.log(result);
                console.log(result);
                var n = result["error"];

                console.log(n);
            },
            error: function (e) {
                console.log(e);
            }

        });

    },


}

//   counting and push to the pallet list
var data = new Array();
var SKUdata = new Array();

var palletSKU1 = document.getElementById('display-sku').innerText = palletSKU;
var getPalletSKU = document.getElementsByClassName('get_pallet_sku').innerText;



function push_data_to_list(){

  var rowCount = document.getElementById("pallet_table").rows.length;
  var rowNewCount = parseInt(rowCount, 10) - 1;
  document.getElementById('total_row').innerHTML = rowNewCount;
  var palletSKU = document.getElementById('pallet_sku').innerText;
  document.getElementById('show-current-sku').style.display = "block";
  document.getElementById('total_pallet_qty').style.display = "block";
  document.getElementById('scanned_pallet_qty').style.display = "block";
  document.getElementById('table_list_info').style.display = "block";
//  document.getElementById('hidden-space').style.display = "none";

  var fromTableSku = document.getElementById('get_pallet_sku').innerHTML;
  document.getElementById('sku').value = fromTableSku;
  var currentSku = document.getElementById('sku').value;
  var inputTabSKU =  document.getElementById("sku_filter_detail").value;
  var skuNo = inputTabSKU + '-sku';
  var skuNoString = String(skuNo);
  document.getElementById(skuNoString).innerHTML = currentSku;
  var TotalPallet = document.getElementById('total_row').innerHTML;
  var TotalPallet = parseInt(TotalPallet);
  var TotalScan = document.getElementById('total_scan').innerHTML;
  var TotalScan = parseInt(TotalScan);
  if(TotalPallet == TotalScan){
  document.getElementById('btnGetCount').style.display = "block";
  }else{
  document.getElementById('btnGetCount').style.display = "none";
  }
  var SKUListStr = document.getElementById('SKU-list').innerText;
  document.getElementById('count-number1').innerText = '';

}


