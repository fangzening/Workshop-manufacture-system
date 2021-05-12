document.addEventListener("DOMContentLoaded", function(){

     setup();
     var selected_device;
     var devices = [];
     function setup()
     {
          /*
           * First get get the default device from BrowserPrint
           * Discovering other devices may take longer to complete.
          */
          BrowserPrint.getDefaultDevice("printer", function(device)
                    {
                         selected_device = device;
                         devices.push(device);
                         // DOM Manipulation is used only if we want to show a list of printers for the user to select
                          /*
                          var html_select = document.getElementById("selected_device");
                          var option = document.createElement("option");
                          option.text = device.name;
                          html_select.add(option);
                          */
                         //Discover other devices
                         BrowserPrint.getLocalDevices(function(device_list){
                              for(var i = 0; i < device_list.length; i++)
                              {
                                   var device = device_list[i];
                                   if(!selected_device || device.uid != selected_device.uid)
                                   {
                                        devices.push(device);
                                        /*
                                         var option = document.createElement("option");
                                         option.text = device.name;
                                         option.value = device.uid;
                                         html_select.add(option);
                                        */
                                   }
                              }
 
                         }, function(){
                               showError("An error occured when getting local printers.");
                          //     alert("An error occured when getting local printers.")
                          }, "printer");
 
                    }, function(error){
                         showError("There was an error. Please make sure a printer is installed on this computer. " + error);
                    })
     }
 
     function getConfig(){
          BrowserPrint.getApplicationConfiguration(function(config){
               console.log(JSON.stringify(config))
          }, function(error){
               console.log(JSON.stringify(new BrowserPrint.ApplicationConfiguration()));
          })
     }
 
     function writeToSelectedPrinter(dataToWrite)
     {
           selected_device.send(dataToWrite, undefined, errorCallback);
     }
 
     var readCallback = function(readData) {
          if(readData === undefined || readData === null || readData === "")
          {
               showError("There was no response from the selected printer.");
          }
          else
          {
               showError("Something went bad: " + readData);
          }
     }
 
     var errorCallback = function(errorMessage){
          showError("Something went bad: " + errorMessage);
     }
 
     function readFromSelectedPrinter()
     {
          selected_device.read(readCallback, errorCallback);
     }
 
     function getDeviceCallback(deviceList)
     {
          console.log("Devices: \n" + JSON.stringify(deviceList, null, 4))
     }
 
     function printGroup(labels){
 
           for (label of labels){
                writeToSelectedPrinter(label);
           }
      }
 
      function showError(error){
           // $('#printer-error-modal > .modal-dialog > .modal-content').text(error);
           // $('#printer-error-modal').modal('toggle');
           alert(error);
      }

      let btn_print_ssn = document.getElementById('btn-print-ssn');
      if (btn_print_ssn != null){
          btn_print_ssn.onclick = function(){
               let dropdown_id = "#label-type-ssn";
               let label_type_dropdown = this.parentNode.parentNode.querySelector(dropdown_id);
               let selected_label_type = label_type_dropdown.options[label_type_dropdown.selectedIndex].value;

               if (selected_label_type == '' || selected_label_type == undefined){
                    label_type_dropdown.style.borderColor = 'red';               
                    showError("You must select a label type.");
                    return
               }

               let ssn = this.parentNode.parentNode.querySelector("#ssn");

               let no_of_copies_id = "#no-of-copies";
               let no_of_copies_element = this.parentNode.parentNode.querySelector(no_of_copies_id);

               if (!Number(no_of_copies_element.value) > 0){
                    no_of_copies_element.style.borderColor = 'red';
                    showError("Number of copies must be set.");
                    return
               }

               let no_of_copies = no_of_copies_element.value;

               printWorkorder([ssn.innerHTML], selected_label_type, no_of_copies);
          
          }
      }

 
      let print_buttons = document.getElementsByClassName('btn-print');
      
      for(var i = 0; i < print_buttons.length; i++) {
          var btn = print_buttons[i];
          btn.onclick = function() {
 
               let workorder = this.parentNode.parentNode.id;
 
 
               let dropdown_id = "#label-type-select-" + workorder;
               let label_type_dropdown = this.parentNode.parentNode.querySelector(dropdown_id);
               let selected_label_type = label_type_dropdown.options[label_type_dropdown.selectedIndex].value;
               // console.log(selected_label_type);
               //check if a label type has been selected              
               if (selected_label_type == '' || selected_label_type == undefined){
                    label_type_dropdown.style.borderColor = 'red';               
                    showError("You must select a label type.");
                    return
               }
 
               let no_of_copies_id = "#no-of-copies-" + workorder;
               let no_of_copies_element = this.parentNode.parentNode.querySelector(no_of_copies_id);
  
               if (!Number(no_of_copies_element.value) > 0){
                    no_of_copies_element.style.borderColor = 'red';
                    showError("Number of copies must be set.");
                    return
               }
 
               let no_of_copies = no_of_copies_element.value;
               
 
               $.ajax({
                    type: "GET",
                    url: 'get-serial-numbers',
                    data: {
                     'workorder': workorder
                     },
                success: function(result) {
                          if ( typeof result == "object"){
                               if (!result.length > 0){
                                    showError("There are no serial numbers for this workorder.")
                                    return
                               }
                               printWorkorder(result, selected_label_type, no_of_copies);
                          }else{
                               showError(result);
                          }
                     }
                });
 
 
          }
      }
 
      function printWorkorder(serial_numbers, selected_label_type, no_of_copies){
           let sn_to_print = [];
           let zpl = document.getElementById(selected_label_type).value;
           let sns = create_labels(serial_numbers, zpl);

           for (let sn of sns){
                for (let i = 1; i <= no_of_copies; i++) {               
                     sn_to_print.push(sn);                    
                }
           }
 
           printGroup(sn_to_print);
      }
      
     /*
          ASSY 6
     */

     let btn_print_asset_tag = document.getElementById('btn-print-asset-tag');
     if (btn_print_asset_tag != null){
          btn_print_asset_tag.onclick = function() {

          let serial_number = document.getElementById('serial_number');
          let csrftoken = document.getElementsByName('csrfmiddlewaretoken')[0].value

          if (!serial_number.value){
               showError("Please enter a Serial Number first.");
               return             
          }

          let serial_number_value = serial_number.value;

          let data_object = { serial_number: serial_number_value}
          let data = JSON.stringify(data_object)
          
          $.ajax({
                    beforeSend: function(xhrObj){
                         xhrObj.setRequestHeader("X-CSRFToken", csrftoken);
                         xhrObj.setRequestHeader("Content-Type","application/json");
                    },
                    type: "POST",
                    url: window.location.origin + '/config/git/asset-tag',
                    data: data,
                    success: function(result) {
                         if (result.status == 200){
                              printAssetTag(serial_number_value, result.message); //should update 1 to no_of_copies if that's going to be an option here
                         }else{
                              showError("Error " + result.status + ": " + result.message);
                         }
                    }
               });
               
          function printAssetTag(serial_number, asset_tag_no){
               const label_name = "Asset Tag Label";
               const zpl = document.getElementById(label_name).value;
                    const regex_sn = /@SN(.*)@SNE/gi; // serial number
                    const regex_an = /@AN(.*)@ANE/gi;  // asset number
                    const regex_fan = /@FAN(.*)@FANE/gi; // fixed asset name
                    const regex_pn = /@PN(.*)@PNE/gi; // part number
                    const regex_pon = /@PON(.*)@PONE/gi; // po number
                    const regex_suite = /@SU(.*)@SUE/gi; // suite                           
                    const regex_ds = /@DS(.*)@DSE/gi; // date of service                           

                    var zpl_ready = zpl.replace(regex_sn, serial_number);
                    zpl_ready = zpl_ready.replace(regex_an, asset_tag_no);
                    zpl_ready = zpl_ready.replace(regex_fan, "Server");
                    zpl_ready = zpl_ready.replace(regex_pon, 'PO1811300039');
                    zpl_ready = zpl_ready.replace(regex_pn, '1A52ND200-600-G'); 
                    zpl_ready = zpl_ready.replace(regex_suite, 's');                                            
                    zpl_ready = zpl_ready.replace(regex_ds, '2020.08.10');
                    writeToSelectedPrinter(zpl_ready);
          }


          };
     }

     let btn_print_shipping_label = document.getElementById('btn-print-shipping-label');
     if (btn_print_shipping_label != null){
          btn_print_shipping_label.onclick = function() {
               /*
               * SHIPPING LABEL
               */

               let serial_number = document.getElementById('serial_number');

               if (!serial_number.value){
                    showError("Please enter a Serial Number first.");
                    return             
               }
               
               let serial_number_value = serial_number.value;
               
               printShippingLabel(serial_number_value);

               function printShippingLabel(serial_number){
               
                    const label_name = "Shipping Label";
                    const zpl = document.getElementById(label_name).value;

                    const regex_sn = /@SN(.*)@SNE/gi; // serial number
                    const regex_an = /@AN(.*)@ANE/gi;  // asset number
                    const regex_fan = /@FAN(.*)@FANE/gi; // fixed asset name
                    const regex_pon = /@PON(.*)@PONE/gi; // po number
                    const regex_suite = /@SU(.*)@SUE/gi; // suite         
                    const regex_pn = /@PN(.*)@PNE/gi; // part number  
                    const regex_rev = /@REV(.*)@REVE/gi; // revision level                  

                    $.ajax({
                         type: "GET",
                         url: window.location.origin + '/config/git/get-git?serial_number=' + serial_number,
                         success: function(result) {
                              console.log(result);
                              console.log(typeof(result));
                              if (result.status == 200){
                                   var zpl_ready = zpl.replace(regex_sn, serial_number);
                                   zpl_ready = zpl_ready.replace(regex_an, result.message.asset_tag_number);
                                   zpl_ready = zpl_ready.replace(regex_fan, "Server");
                                   zpl_ready = zpl_ready.replace(regex_pon, result.message.po_no);
                                   zpl_ready = zpl_ready.replace(regex_pn, result.message.part_no); 
                                   zpl_ready = zpl_ready.replace(regex_suite, result.message.suite);
                                   zpl_ready = zpl_ready.replace(regex_rev, "X4");
                                   console.log(zpl_ready);
                                   writeToSelectedPrinter(zpl_ready);
                              }
                              else {
                                   showError("Error " + result.status + ": " + result.message + ". Possible cause: git data doesn't exist.");
                              }
                         }
                    });      
               }
          };
     }

     let btn_print_mac_address_label = document.getElementById('btn-print-mac-address-label');
     if (btn_print_mac_address_label != null){
          btn_print_mac_address_label.onclick = function() {
               /*
               * MAC ADDRESS LABEL
               */
               let serial_number = document.getElementById('serial_number');

               if (!serial_number.value){
                    showError("Please enter a Serial Number first.");
                    return             
               }
               
               let serial_number_value = serial_number.value;
               
               printShippingLabel(serial_number_value);

               function printShippingLabel(serial_number){
               
                    const label_name = "Mac Address Label";
                    const zpl = document.getElementById(label_name).value;

                    const regex_sn = /@SN(.*)@SNE/gi; // serial number
                    const regex_an = /@AN(.*)@ANE/gi;  // asset number
                    const regex_fan = /@FAN(.*)@FANE/gi; // fixed asset name
                    const regex_pon = /@PON(.*)@PONE/gi; // po number
                    const regex_suite = /@SU(.*)@SUE/gi; // suite         
                    const regex_pn = /@PN(.*)@PNE/gi; // part number  
                    const regex_rev = /@REV(.*)@REVE/gi; // revision level                  

                    $.ajax({
                         type: "GET",
                         url: window.location.origin + '/config/git/get-git?serial_number=' + serial_number,
                         success: function(result) {
                              console.log(result);
                              console.log(typeof(result));
                              if (result.status == 200){
                                   var zpl_ready = zpl.replace(regex_sn, serial_number);
                                   zpl_ready = zpl_ready.replace(regex_an, result.message.asset_tag_number);
                                   zpl_ready = zpl_ready.replace(regex_fan, "Server");
                                   zpl_ready = zpl_ready.replace(regex_pon, result.message.po_no);
                                   zpl_ready = zpl_ready.replace(regex_pn, result.message.part_no); 
                                   zpl_ready = zpl_ready.replace(regex_suite, result.message.suite);
                                   zpl_ready = zpl_ready.replace(regex_rev, "X4");
                                   console.log(zpl_ready);
                                   writeToSelectedPrinter(zpl_ready);
                              }
                              else {
                                   showError("Error " + result.status + ": " + result.message);
                              }
                         }
                    });
               }
          };
     }

     let btn_print_po_info_label = document.getElementById('btn-print-po-info-label');
     if (btn_print_po_info_label != null){
          btn_print_po_info_label.onclick = function() {
               /*
               * PO Info
               */

               let serial_number = document.getElementById('serial_number');

               if (!serial_number.value){
                    showError("Please enter a Serial Number first.");
                    return             
               }
               
               let serial_number_value = serial_number.value;
               
               printPoInfoLabel(serial_number_value);

               function printPoInfoLabel(serial_number){
               
                    const label_name = "PO Label";
                    const zpl = document.getElementById(label_name).value;

                    const regex_sn = /@SN(.*)@SNE/gi; // serial number
                    const regex_an = /@AN(.*)@ANE/gi;  // asset number
                    const regex_fan = /@FAN(.*)@FANE/gi; // fixed asset name
                    const regex_pon = /@PON(.*)@PONE/gi; // po number
                    const regex_suite = /@SU(.*)@SUE/gi; // suite         
                    const regex_pn = /@PN(.*)@PNE/gi; // part number  
                    const regex_rev = /@REV(.*)@REVE/gi; // revision level                  

                    $.ajax({
                         type: "GET",
                         url: window.location.origin + '/config/git/get-git?serial_number=' + serial_number,
                         success: function(result) {
                              console.log(result);
                              console.log(typeof(result));
                              if (result.status == 200){
                                   var zpl_ready = zpl.replace(regex_sn, serial_number);
                                   zpl_ready = zpl_ready.replace(regex_an, result.message.asset_tag_number);
                                   zpl_ready = zpl_ready.replace(regex_fan, "Server");
                                   zpl_ready = zpl_ready.replace(regex_pon, result.message.po_no);
                                   zpl_ready = zpl_ready.replace(regex_pn, result.message.part_no); 
                                   zpl_ready = zpl_ready.replace(regex_suite, result.message.suite);
                                   zpl_ready = zpl_ready.replace(regex_rev, "X4");
                                   writeToSelectedPrinter(zpl_ready);
                              }
                              else {
                                   showError("Error " + result.status + ": " + result.message);
                              }
                         }
                    });      
                                                                 
                    writeToSelectedPrinter(zpl_ready);
               }
          };
     }     

      function create_labels(serial_numbers, zpl){

          const regex_sn = /@SN(.*)@SNE/gi; // serial number
          const regex_an = /@AN(.*)@ANE/gi;  // asset number
          const regex_fan = /@FAN(.*)@FANE/gi; // fixed asset name
          const regex_pn = /@PN(.*)@PNE/gi; // part number
          const regex_pon = /@PON(.*)@PONE/gi; // po number
          const regex_suite = /@SU(.*)@SUE/gi; // suite                           
          const regex_ds = /@DS(.*)@DSE/gi; // date of service                    
                      
          let zpl_with_sn = []
 
           for (let i = 0; i < serial_numbers.length; i++) {
                var zpl_ready = zpl.replace(regex_sn, serial_numbers[i]);
                zpl_ready = zpl_ready.replace(regex_pn, "1A52ND200-600-G");
                zpl_with_sn.push(zpl_ready);
           }
 
           return zpl_with_sn;
      }
 });


 /*
      $( "#btn-print" ).click(function() {
           
           let label_type_dropdown = document.getElementById("label-type-select");
           let selected_label_type = label_type_dropdown.options[label_type_dropdown.selectedIndex].value;
           
           if (selected_label_type == '' || selected_label_type == undefined){
                label_type_dropdown.style.borderColor = 'red';               
                showError("You must select a label type.");
                return
           }
 
 
           let table = document.getElementById("print-sn-table");
           let sn_to_print = [];
           
           for (let i = 1, row; row = table.rows[i]; i++) {
 
                let print_checkbox = row.children[1].firstElementChild; 
 
                
                //get serial number of the checked rows
                if( print_checkbox.checked ){
                     let serial_number = row.children[5].firstElementChild.innerHTML;
                     sn_to_print.push(serial_number);
                }
           }
 
           //check if any serial number was selected, by checking if sn_to_print is an array AND if it's length is greater than 0
           if (!Array.isArray(sn_to_print) || !sn_to_print.length) {
                showError("No serial numbers were selected.")
           }else{
                let labels_to_print = create_labels(sn_to_print, selected_label_type);               
                printGroup(labels_to_print);
           }         
 
      });
 */