$("#display-sku").keyup(function () {
    var searchterms = $("#display-sku").val().toLowerCase().split(' ');
    $('#salesoorder_detail_tab tr').each(function (i, row) {
        $(row).hide(1);
        $("td", row).each(function (y, td) {
            var tdValue = $(td).text().toLowerCase();
            searchterms.forEach(function (entry) {
                if (tdValue.indexOf(entry) != -1) {
                    $(row).show(1);
                }
            });
        });
    });
});




$(document).ready(function(){
$('#push_to_list').click(function(){


  // Search all columns
//  $('#sku').keyup(function(){
    // Search Text
    var search = $('#sku').val();

    // Hide all table tbody rows
    //$('#salesoorder_detail_tab tbody tr').hide();

    // Count total search result
    var len = $('#salesoorder_detail_tab tbody tr:not(.notfound) td:contains("'+search+'")').length;

    if(len > 0){
      // Searching text in columns and show match row
      $('#salesoorder_detail_tab tbody tr:not(.notfound) td:contains("'+search+'")').each(function(){
        $(this).closest('tr').show();
        $(this).css('background', '#222');
        $(this).css('color', '#fff');
      });
    }else{
      $('.notfound').show();
      $('#messageSKU').css('display', 'block');
      $('#scan-sn-input').css('display', 'none');
      $('#messageSKU').html('<div id="myModal" class="modal-log-shipout message-box-bottom"><div class="modal-content"> <div class="warning-modal-body"> <p>No matched sku</p></div></div></div>');
 //     $('#bottomSection').html('<div id="myModal" class="modal-log-shipout message-box-bottom"><div class="modal-content"> <div class="warning-modal-body"> <p>No matched sku</p></div></div></div>');
      //$('errorSection').html('<div id="myModal" class="modal-log-shipout message-box-bottom"><div class="modal-content-error"><div class="warning-modal-body"><p>No matched sku.</p></div></div></div>';

    }

  });

  // Search on name column only
//});

});

// Case-insensitive searching (Note - remove the below script for Case sensitive search )
$.expr[":"].contains = $.expr.createPseudo(function(arg) {
   return function( elem ) {
     return $(elem).text().toUpperCase().indexOf(arg.toUpperCase()) >= 0;
   };
});
