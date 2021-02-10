/*
 Template Name: Stexo - Responsive Bootstrap 4 Admin Dashboard
 Author: Themesdesign
 Website: www.themesdesign.in
 File: Datatable js
 */

$(document).ready(function() {
//    $('#datatable').DataTable();
//
//    //Buttons examples
//    var table = $('#datatable-buttons').DataTable({
//        lengthChange: false,
//        buttons: ['copy', 'excel', 'pdf', 'colvis'],
//        scrollX: true,
//    });
//
//    table.buttons().container()
//        .appendTo('#datatable-buttons_wrapper .col-md-6:eq(0)');
var oTable = $('#datatables').DataTable({
          pageLength:10,
          ordering: true,
          columnDefs: [{
              width: "20%",
              orderable: false,
              targets: "no-sort"
          }],
          language: {
            emptyTable: "No data available"
           },
          order: [],
          "scrollX": true,

    });
} );
