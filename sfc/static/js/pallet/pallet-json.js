// ### Ajax ######
var main = {


   ValidateSN: function (sn, token) {
        error_section = $("#errorSection");
        console.log("error test 1 " + sn);
        error_section.children().remove();
        msg = '<div id="myModal" class="modal-log message-box-bottom"><div class="modal-content-error bottom-message">';
        msgEnd = "</div></div>";
        var result = "";
        var pallet_id = document.getElementById("pallet_id_input").value;
        var result = false;
        var last_sku = document.getElementById("last_sku").value;
        var first_sku = document.getElementById("first_sku").value;
        var x = document.getElementById("last_sku").value;
        var y = document.getElementById("first_sku").value;
        var last_sn = document.getElementById("last_sn").value;



        $.ajax({
            type: "POST",
            url: "/shipping/wip/palletize/validate-sn/",
            data: {
                'serialnumber': sn,
                'pallet_id': pallet_id,
                'first_sku': first_sku,
                'last_sku': last_sku,
                'last_sn': last_sn,


                'csrfmiddlewaretoken': token
            },
            dataType: 'json',
            success: function (data, status) {



                console.log("validate SN");
                var n = result["stat"];

                if (data['stat'] == "not_exist") {
                $('#json_message').html('<div id="myModal" class="modal-log message-box-bottom" style="padding-top: 0;"><div class="modal-content-error"><span class="close" data-dismiss="modal" style="z-index: 100;">×</span><div class="warning-modal-body"><p>SN: <strong>'+ sn +'</strong> does not exist.</p></div><button style="display: none;" id="myBtn">Open Modal</button></div>');
                return false;
                }





                else if(data['stat'] == "sku_not_matched"){
                $('#json_message').html('<div id="myModal" class="modal-log message-box-bottom" style="padding-top: 0;"><div class="modal-content-error"><span class="close" data-dismiss="modal" style="z-index: 100;">×</span><div class="warning-modal-body"><p>SKU does not match.</p></div><button style="display: none;" id="myBtn">Open Modal</button></div>');
                return false;
                }

                else if(data['stat'] == "is_shipped"){
                $('#json_message').html('<div id="myModal" class="modal-log message-box-bottom" style="padding-top: 0;"><div class="modal-content-error"><span class="close" data-dismiss="modal" style="z-index: 100;">×</span><div class="warning-modal-body"><p>SN: <strong>'+ sn +'</strong> is shipped.</p></div><button style="display: none;" id="myBtn">Open Modal</button></div>');
                return false;
                }

                else if(data['stat'] == "sn_not_completed"){
                $('#json_message').html('<div id="myModal" class="modal-log message-box-bottom" style="padding-top: 0;"><div class="modal-content-error"><span class="close" data-dismiss="modal" style="z-index: 100;">×</span><div class="warning-modal-body"><p>SN: <strong>'+ sn +'</strong> is not completed.</p></div><button style="display: none;" id="myBtn">Open Modal</button></div>');
                return false;
                }





                else if (data['stat'] == "in_repair") {
                $('#json_message').html('<div id="myModal" class="modal-log message-box-bottom" style="padding-top: 0;"><div class="modal-content-error"><span class="close" data-dismiss="modal" style="z-index: 100;">×</span><div class="warning-modal-body"><p>SN: <strong>'+ sn +'</strong> is in Repair station.</p></div><button style="display: none;" id="myBtn">Open Modal</button></div>');
                return false;
                }

                else if (data['stat'] == "in_use") {
                $('#json_message').html('<div id="myModal" class="modal-log message-box-bottom" style="padding-top: 0;"><div class="modal-content-error"><span class="close" data-dismiss="modal" style="z-index: 100;">×</span><div class="warning-modal-body"><p>SN: <strong>'+ sn +'</strong> is in used.</p></div><button style="display: none;" id="myBtn">Open Modal</button></div>');
                return false;
                }

                else if (data['stat'] == "po_not_exist") {
                $('#json_message').html('<div id="myModal" class="modal-log message-box-bottom" style="padding-top: 0;"><div class="modal-content-error"><span class="close" data-dismiss="modal" style="z-index: 100;">×</span><div class="warning-modal-body"><p>SN: <strong>'+ sn +'</strong> does not exist in git table. </p></div><button style="display: none;" id="myBtn">Open Modal</button></div>');
                return false;
                }

//                else if(data['stat'] == "does_not_have_po"){
//                $('#json_message').html('<div id="myModal" class="modal-log message-box-bottom" style="padding-top: 0;"><div class="modal-content-error"><span class="close" data-dismiss="modal" style="z-index: 100;">×</span><div class="warning-modal-body">SN: <strong>'+ sn +'</strong> does not have a po.</div><button style="display: none;" id="myBtn">Open Modal</button></div>');
//                return false;
//                }

//                else if(data['stat'] == "po_not_matched"){
//                $('#json_message').html('<div id="myModal" class="modal-log message-box-bottom" style="padding-top: 0;"><div class="modal-content-error"><span class="close" data-dismiss="modal" style="z-index: 100;">×</span><div class="warning-modal-body"><p>PO does not match.</p></div><button style="display: none;" id="myBtn">Open Modal</button></div>');
//                return false;
//                }

                else if( data['stat'] = "all_validated"){
                const sn = document.getElementById("serialnumber_json").value;
                var csrftoken = jQuery("[name=csrfmiddlewaretoken]").val();
                main.SaveSN(sn, csrftoken);
                }


                console.log('data status');
                 if(x === y){


                }else{
                 $('#json_message').html('<div id="myModal" class="modal-log message-box-bottom" style="padding-top: 0;"><div class="modal-content-error"><span class="close" data-dismiss="modal" style="z-index: 100;">×</span><div class="warning-modal-body"><p>SKU does not match.</p></div><button style="display: none;" id="myBtn">Open Modal</button></div>');
                }


            },
            error: function (e) {
                console.log(e);
            }

        });
        return result;
    },

    SaveSN: function (sn, token) {
//        var serialnumber = document.getElementById("serialnumber_json").value;
        var pallet_id = document.getElementById("pallet_id_input").value;
        var creator = document.getElementById("creator").value;
        var updater = document.getElementById("updater_input").value;

        var current_qty = document.getElementById("current_qty").value;
        var status = document.getElementById("status").value;
        var full = document.getElementById("full").value;
        var full_date = document.getElementById("full_date").value;
        var wh_id = document.getElementById("wh_id").value;
        var height = document.getElementById("height").value;
        var length = document.getElementById("length").value;
        var width = document.getElementById("width").value;
        var weight = document.getElementById("weight").value;
        var gross_weight = document.getElementById("gross_weight").value;
        var net_weight = document.getElementById("net_weight").value;
        var volume_weight = document.getElementById("volume_weight").value;
        var x = document.getElementById("last_sku").value;
        var y = document.getElementById("first_sku").value;
        var last_sn = document.getElementById("last_sn").value;


        $.ajax({
            type: "POST",
            url: "/shipping/wip/palletize/add-sn/",
            data: {
                'serialnumber': sn,
                'pallet_id': pallet_id,
                'creator': creator,
                'updater': updater,
//                'row_id': row_id,
                'csrfmiddlewaretoken': token,

                'current_qty': current_qty,
                'status': status,
                'full': full,
                'full_date': full_date,
                'wh_id': wh_id,
                'height': height,
                'length': length,
                'width': width,
                'weight': weight,
                'gross_weight': gross_weight,
                'net_weight': net_weight,
                'volume_weight': volume_weight
            },

            dataType: 'json',

            success: function (pallet_table) {

                console.log("Begin: about to save SN");
                document.getElementById("serialnumber_json").value = "";
                $('#json_message').html('');
                $('#compare').html('');
                $('#myModal').html('');

                let pal_table =  $('#update-pallet tbody');
                let template = "";
                var returnedData = JSON.parse(pallet_table);
                console.log(returnedData);
//                $('#update-pallet').html(response)
                pal_table.children().remove();
                for (let i = 0; i < returnedData.pallet_table.length; i++) {
                    template += "<tr id='row" + returnedData.pallet_table[i].serial_number +  "'>";
                     template += "<td>" + returnedData.pallet_table[i].serial_number + "</td>";
                     template += "<td>" + returnedData.pallet_table[i].sku + "</td>";
                     template += '<td>';
                     template += ' <button id="' + returnedData.pallet_table[i].serial_number + '"class="icon-text"><img style="width: 22px; margin-left: 3px;" src="/static/svg/delete.svg" alt="icon">';
                     template += '<span>Remove</span></button></form></td>';
                     template += "</tr>";
                }
                console.log(template);
                console.log('test after template');
                pal_table.append(template);
                 var palletID = document.getElementById("pallet_id_input").value;
                var palletQty = document.getElementById(palletID).innerText;
                var palletQty = parseInt(palletQty)+ 1;
                $('#' + palletID).text(palletQty);

                $(document).ready(function(){
                  $('#update-pallet button').click(function(){
                  var csrftoken = jQuery("[name=csrfmiddlewaretoken]").val();
                      const sn = $(this).attr('id');
                        console.log('delete test');

                        main.DeleteSN(sn, csrftoken);
                            var palletID = document.getElementById("pallet_id_input").value;
                            var palletQty = document.getElementById(palletID).innerText;
                            var palletQty = parseInt(palletQty)- 1;
                            $('#' + palletID).text(palletQty);

                  var rowID = this.id;
                   $('#row'+ rowID).remove();
                   });
                });

//                var rows = $('#update-pallet row');
//                rows.hide();
//                $('.row-data:last-child').after(rows);
//                rows.fadeIn("slow");

            },
            error: function (e) {
                console.log(e);
            }

        });
        console.log(sn, token);

    },


    DeleteSN: function (sn, token) {

        var pallet_id = document.getElementById("pallet_id_input").value;
        var updater = document.getElementById("updater_input").value;
        var serialnumber = document.getElementById("serialnumber_json").value;
        var last_sn = document.getElementById("last_sn").value;
//        var current_qty = document.getElementById("current_qty").value;
        console.log('deleting beginning');
        $.ajax({
            url: "/shipping/wip/palletize/delete-sn/",
            type: "POST",
            dataType: "json",
//                beforeSend: function (xhr) {
//                    xhr.setRequestHeader("X-CSRFToken", '{{ csrf_token }}');
//                },
            data: {
            'serialnumber': sn,
            'pallet_id': pallet_id,
            'updater': updater,

            'csrfmiddlewaretoken': token
        },
            success: function (pallet_table) {
                console.log('deleting row');
                let pal_table =  $('#update-pallet tbody');
                let template = "";
//                var returnedData = JSON.parse(pallet_table);
//                pal_table.children().remove();
//                for (let i = 0; i < returnedData.pallet_table.length; i--) {
//                template += "<tr id='row" + returnedData.pallet_table[i].serial_number +  "'>";
//                template += "<td>" + returnedData.pallet_table[i].serial_number + "</td>";
//                template += "<td>" + returnedData.pallet_table[i].sku + "</td>";
//                template += '<td>';
////                    template += '{% csrf_token %}';
////                    template += ' <input type="hidden" name="pallet_id" class="form-control" value="pallet_id "><input type="hidden" name="updater" class="form-control" value="{{ user.get_username }}"><input type="hidden" name="creator" class="form-control" value="{{ pallet.creator }}"></form>';
//                template += ' <button id="' + returnedData.pallet_table[i].serial_number + '"class="icon-text"><img style="width: 22px; margin-left: 3px;" src="/static/svg/delete.svg" alt="icon">';
//                template += '<span>Remove</span></button></form></td>';
//                template += "</tr>";
//                console.log('deleting row end');
//            }
            $(document).ready(function(){
              $('#update-pallet button').click(function(){
              var rowID = this.id;
               $('#row'+ rowID).remove();
                var palletID = document.getElementById("pallet_id_input").value;
                var palletQty = document.getElementById(palletID).innerText;
                var palletQty = parseInt(palletQty)- 1;
                $('#' + palletID).text(palletQty);
               });
            });

            },
            error: function () {
                console.log('delete failed');
            }
        });
      },

}