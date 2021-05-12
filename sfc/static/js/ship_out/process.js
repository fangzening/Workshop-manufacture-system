

function Process() {
//    confirm("Confirm process?");
    console.log('hello Json');
    var csrftoken = jQuery("[name=csrfmiddlewaretoken]").val();
    var salesorder = document.getElementById("salesorder1").value;
    var username = document.getElementById("username").value;
    var palletlist = document.getElementById("pallet_array").value;
    var pString = String(palletlist);
    var pArray = pString.split(" ");
    var newPalletList = Array(palletlist);
    console.log(pArray);

    var skuno = document.getElementById("sku").value;
    var qty = document.getElementById("sn-string-test-sum").value;
    var $table = $('#data-table'),
            rows = [],
            header = [];
        $table.find("thead th").each(function () {
            header.push($(this).html());
        });
        $table.find("tbody tr").each(function () {
            var row = {};
            $(this).find("td").each(function (i) {
                var key = header[i],
                    value = $(this).html();
                row[key] = value;
            });
            rows.push(row);
        });
        var k = JSON.stringify(rows);
        console.log(k);
         console.log(username);

    $.ajax({
            type: "POST",
            url: "/shipping/wip/shipout/process/",
            data: {
                'salesorder': salesorder,
                'palletlist': k,
                'username': username,

                'sku': skuno,
                'qty': qty,
                'csrfmiddlewaretoken': csrftoken
            },
            dataType: 'json',
            error: function() {
                 document.getElementById('process-popup').style.display = 'none';
                 document.getElementById('count-number1').style.display = 'none';


                 document.getElementById('bottomSection').innerHTML =
                 '<div id="myModal" class="modal-log-shipout message-box-bottom"><div class="modal-content-error">'
                 + '<div class="warning-modal-body"><p>API connection Failed.</p></div></div></div>';
                 // document.getElementById('shortage').innerHTML = '<div id="myModal" class="modal-keypart" style="padding-top: 0"><div class="modal-content"  style="width: 100%;"><span class="close" data-dismiss="modal" style="z-index: 100; top: 10px;"></span><div class="warning-modal-body"><p>API connection Failed.</p></div></div><button style="display: none;" id="myBtn">Open Modal</button></div>';
            },
            success: function (Response) {
            console.log(Response);
            //var JsonObject = result['json_object'];
            //document.getElementById('shortage').innerHTML = '<div id="myModal" class="modal-keypart" style="padding-top: 0"><div class="modal-content"  style="width: 100%;"><span class="close" data-dismiss="modal" style="z-index: 100; top: 10px;"></span><div class="warning-modal-body"><p>' + k + '</p></div></div><button style="display: none;" id="myBtn">Open Modal</button></div>';
            //var errorCode = result['json_object'];
            window.location.href = '/shipping/wip/ship_out/success/';
//           if ( errorCode == 00  )
//             window.location.replace("/shipping/wip/ship_out/success/");
//             else if( errorCode != 00 )
//             document.getElementById('shortage').innerHTML = '<div id="myModal" class="modal-keypart" style="padding-top: 0"><div class="modal-content"  style="width: 100%;"><span class="close" data-dismiss="modal" style="z-index: 100; top: 10px;"></span><div class="warning-modal-body"><p>Failed.</p></div></div><button style="display: none;" id="myBtn">Open Modal</button></div>';

         }
        });
};
function Test(){
    console.log('test');
    document.getElementById('testtest').innerText = "hello";
};