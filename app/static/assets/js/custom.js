$(document).ajaxStart(function () {
    //ajax request went so show the loading image
    $('.loader').show();
 })
$(document).ajaxStop(function () {
   //got response so hide the loading image
     $('.selectpicker').selectpicker();
     $('.loader').fadeOut('Slow');
});


