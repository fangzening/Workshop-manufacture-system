
var main = {
    ValidateDN: function (deliveyrNumber, token) {
        $.ajax({
            type: "POST",
            url: "",
            data: {
                'dn': deliveyrNumber,
                'csrfmiddlewaretoken': token
            },
            dataType: 'json',
            success: function (DN_VALUE) {
                // let pallet_data = $("#pallet_div");
                // let pallet_table = $("#pallet_validation tbody");
                let dn_table = $("#dn_information tbody");

                let template = "";

                var returnedData = JSON.parse(DN_VALUE);

                dn_table.children().remove();

                for (let i = 0; i < returnedData.dn_table.length; i++) {
                    template += "<tr>";
                    template += "<td>" + returnedData.dn_table[i].pal_qty + "</td>";
                    template += "<td>" + returnedData.dn_table[i].cutomer_po + "</td><td>" + returnedData.dn_table[i].salesorder + "</td>";
                    template += "<td>" + returnedData.dn_table[i].so_qty + "</td><td>" + returnedData.dn_table[i].ship_qty + "</td>";
                    template += "</tr>";
                }
                dn_table.append(template);


            },
            error: function (response) {
                // alert the error if any error occured
                //alert(response["responseJSON"]["error"]);
            }

        });
    },
    GetPalletDN: function (deliveyrNumber, token) {
        $.ajax({
            type: "POST",
            url: "/shipping/wip/truckload/getpallet/",
            data: {
                'dn': deliveyrNumber,
                'csrfmiddlewaretoken': token
            },
            dataType: 'json',
            success: function (pallet_table) {
                var returnedData = JSON.parse(pallet_table);
                var errorMessage = "";

                let error_section = $("#errorSection");

                error_section.children().remove();
                var valDN = 0;

                var tmp_pall_rows = $('#pallet_validation tbody tr').length;

                if (tmp_pall_rows > 0) {
                    const dn2 = $("#dn_select_list :selected").val();
                    $('#pallet_validation tbody tr').each(function () {
                        if ($(this).find('td').eq(1).text() == dn2) {
                            valDN = 1;
                            errorMessage = "Delivery Number selected is already in Pallet List."
                        }
                        if ($(this).find('td').eq(0).text() != $('#dn_information tr:nth-child(1) td:nth-child(2)').text()) {
                            valDN = 1;
                            errorMessage = "Cannot process Delivery Numbers from different PO."
                        }
                    });
                }

                if (valDN != 0) {
                    console.log("error");
                    var msg = "";
                    msg = '<div id="myModal" class="modal-log message-box-bottom"><div class="modal-content-success">';
                    msg += '<span class="close" data-dismiss="modal" style="z-index: 100;">×</span>';
                    msg += '<div class="warning-modal-body">';
                    msg += '<p class="card-title"><strong>Error: </strong>' + errorMessage + '.</p>';
                    msg += "</div></div></div>";

                    error_section.append(msg);

                }
                else {
                    let pl_table = $("#pallet_validation tbody");
                    let tmpl = "";

                    for (let i = 0; i < returnedData.pallet_table.length; i++) {
                        tmpl += "<tr><td>" + returnedData.pallet_table[i].po + "</td><td>" + returnedData.pallet_table[i].dn_id + "</td><td>" + returnedData.pallet_table[i].pallet_id + "</td></tr>";
                    }
                    pl_table.append(tmpl);

                    var pallet_rows = $('#pallet_validation tbody tr').length;

                    let tot_table = $("#total_pallet_qty tbody");
                    tmpl = "";
                    tot_table.children().remove();
                    tmpl += "<tr><td>" + pallet_rows + "</td></tr>";
                    tot_table.append(tmpl);
                }

            },
            error: function (pallet_table) {
                console.log("error" + pallet_table);
            }

        });
    },
    ValidatePallet: function (pallet) {
        error_section = $("#errorSection");
        console.log("En funcion 1" + pallet);
        error_section.children().remove();
        msg = '<div id="myModal" class="modal-log message-box-bottom" style=""><div class="modal-content-error">';
        msgEnd = "</div></div>";
        var found = 0;
        var tot_table = "";
        var palqty = "";
        var currentqty = 0;
        var new_total = 0;

        $('#pallet_validation tbody tr').each(function () {
            console.log("En el Loop" + pallet);
            if ($(this).find('td').eq(2).text() == pallet) {
                console.log($(this).find('td').eq(2).text() + "mas adentro" + pallet);
                $(this).css('background', '#222');
                $(this).css('color', '#fff');
                $(this).find('td').eq(3).text("X");
                found = 1;
            }
        });

        if (found == 0) {
            console.log("Error pallet no es igual" + pallet);
            msg += "<p>Pallet " + pallet + " not found</p>" + msgEnd;
            error_section.append(msg);
            return 0;
        }
        else {
//            tot_table = $('#scanned_pallet_qty tr:nth-child(1) td:nth-child(1)').text();
            tot_table = $("tr[style='background: rgb(34, 34, 34); color: rgb(255, 255, 255);']").length;
            palqty = $('#total_pallet_qty tr:nth-child(1) td:nth-child(1)').text();

//            currentqty = parseInt(tot_table, 10);
            currentqty = parseInt(tot_table);
            new_total = (currentqty);
//            new_total = (currentqty + 1);


            $('#scanned_pallet_qty tr:nth-child(1) td:nth-child(1)').text(currentqty);

            if ((parseInt(palqty, 10) > 0 && parseInt(new_total, 10) > 0) && parseInt(palqty, 10) == parseInt(new_total, 10)) {
                error_section.children().remove();

                msg = "";
                msg = '<div id="myModal" class="modal-log message-box-bottom"><div class="modal-content-success">';
                msg += '<span class="close" data-dismiss="modal" style="z-index: 100;">×</span>';
                msg += '<div class="warning-modal-body">';
                msg += '<p class="card-title">All Pallets have been verified, please proceed with Truck Load.</p>';
                msg += "</div></div></div>";

                error_section.append(msg);
            }
        }

    },
    SaveTruckLoad: function (token) {
        console.log("savetruckload function");
        var total_pallet = parseInt($('#total_pallet_qty tr:nth-child(1) td:nth-child(1)').text(), 10);
        var scanned_pallet = parseInt($('#scanned_pallet_qty tr:nth-child(1) td:nth-child(1)').text(), 10);
        var container_number = $.trim($("#container_number").val());
        var seal_number = $.trim($("#seal_number").val());

        let error_section = $("#errorSection");
        error_section.children().remove();
        var msg = '<div id="myModal" class="modal-log message-box-bottom"><div class="modal-content-error">';
        var msgEnd = "</div></div>";

        if (total_pallet == 0) {
            msg += "<p>Please add a Delivery Number from the list.</p>" + msgEnd;
            error_section.append(msg);
            return 0;
        }

        if (scanned_pallet == 0) {
            msg += "<p>Any pallet has been scanned yet.</p>" + msgEnd;
            error_section.append(msg);
            return 0;
        }

        if (total_pallet != scanned_pallet) {
            msg += "<p>All Pallets must be verified.</p>" + msgEnd;
            error_section.append(msg);
            return 0;
        }
        if (container_number.length == 0) {
            msg += "<p>Container Number must not be blank.</p>" + msgEnd;
            error_section.append(msg);
            return 0;
        }
        if (seal_number.length == 0) {
            msg += "<p>Seal Number must not be blank.</p>" + msgEnd;
            error_section.append(msg);
            return 0;
        }

        var $table = $('#pallet_validation'),
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

        $.ajax({
            type: "POST",
            url: "/shipping/wip/truckload/savetruckload/",
            data: {
                'dn': k,
                'container': container_number,
                'seal': seal_number,
                'csrfmiddlewaretoken': token
            },
            dataType: 'json',
            success: function (result) {
                console.log("Begin: success from Truck Load");
                console.log(result);
                var n = result["error"];

                console.log(n.length);

                if (n.length > 0) {
                    console.log("longitud mayor");
                    msg += result["error"] + msgEnd;
                    error_section.append(msg);
                } else {
                    console.log("longitud 0");
                    msg = "";
                    msg = '<div id="myModal" class="modal-log message-box-bottom"><div class="modal-content-success">';
                    msg += '<span class="close" data-dismiss="modal" style="z-index: 100;">×</span>';
                    msg += '<div class="warning-modal-body">';
                    msg += '<p class="card-title">Truck Load Process has finisshed succesfully. Printing BOL Document</p>';
                    msg += "</div></div></div>";

                    error_section.append(msg);
                }
                console.log("End: success from Truck Load");
            },
            error: function (e) {
                console.log(e);
            }

        });

    }
}