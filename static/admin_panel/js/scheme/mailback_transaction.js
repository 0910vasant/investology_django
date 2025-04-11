
var t

t = $('#transaction_table').DataTable( {
  processing: true,
  // dom: '<"top"lfB>rt<"bottom"ip><"clear">',
  // dom: 'lBfrtip',
  // "paging": true,                // Enable pagination
  //   "lengthMenu": [10, 25, 50,100],    // Page length options
  //   "pageLength": 10,              // Default rows per page
  //   "ordering": true,              // Enable column sorting
  //   "order": [[ 0, 'asc' ]],       // Set default sort order
  //   "searching": true,             // Enable search functionality
  //   "info": true,                  // Show information at the bottom
  //   "language": {
  //       "paginate": {
  //           "previous": "Previous",   // Customize pagination buttons
  //           "next": "Next"
  //       }
  //   },
    buttons: [
      {
          extend: 'csv',
          text: '<i class="fa fa-refresh"></i> CSV',
          className: 'btn-custom-csv',
          title: "Mailback Details",
          exportOptions: {
              columns: [0, 1, 2, 3, 4, 5, 6, 7, 8, 9]  // Columns to export
          }
      }
    ],
    // buttons: [
      
    //     {
    //       extend: "csv",
    //       title:	"Mailback Details",
    //       exportOptions: {
    //         columns:[0,1,2,3,4,5,6,7,8,9],
    //         format: {
    //       // colidx = [0,1,2,3,4,5,6,7]
    //       body: function ( inner, rowidx, colidx, node ) {
    //       return node.innerText;
    //     }
		// 		}
		// 	  }
    //     }
    // ],
  ajax: '/load_mailback_transaction',

  columns: [
    { 
      "data": null, // This is for the serial number
      "render": function (data, type, row, meta) {
          return meta.row + 1; // Return row index + 1 for serial number
      }
    },
    { data: "INV_NAME__PAN_NO" },
    { data: "INV_NAME__CUST_NAME" },
    { data: "PROD_CODE__PRODCODE" },
    { data: "PROD_CODE__SCHEME_NAME" },      
    { data: 'FOLIO_NO' },
    { data: 'TOTAL_PURPRICE' },
    { data: 'TOTAL_UNITS' },
    { data: 'TOTAL_AMOUNT' },
    { data: null },
  ],
 
  columnDefs: [
      { className: 'text-center', targets: [0,1,2,3,4,5,6,7,8,9] },
      // {
      //   targets: [5], render: function (a, b, data, d){
      //     html = ""
      //     if (data.FUND_CODE__COMPANY == "kfintech") {
      //       html = data.FUND_CODE__COMPANY_FUND_CODE+data.SCHEME_CODE
      //       html = html.slice(0, -1);
      //     } else {
      //       html = data.FUND_CODE__FUND_CODE+data.SCHEME_CODE
            
      //     }
      //    return html
      //   },
      // },
      {
        targets: [9], render: function (a, b, data, d){
          // console.log(d)
          html = `<div class="dropdown">
                    <button class="btn btn-secondary dropdown-toggle py-1" type="button" id="dropdownMenuButton1" data-bs-toggle="dropdown" aria-expanded="false">
                        Action
                    </button>
                    <ul class="dropdown-menu" aria-labelledby="dropdownMenuButton1">
                    <li><a class="dropdown-item py-1 edit_modal" href="#" data-id="${data.id}" data-bs-toggle="modal" data-bs-target="#load_mailback_details">View</a></li>
                    </ul>
                  </div>`
                  // <hr class="drop-hr">
                  //         <a class="dropdown-item delete" href="javascript:void(0);" data-id="${data.id}"><i class="fa fa-trash"></i> Delete</a>
         return html
        },
      }
  ],
  } );



$("#add_mailback_transaction_form").on("submit", function (e) {
    e.preventDefault();

    data = new FormData(this);
    Swal.fire({
      title: 'Are you sure want to Submit Excel?',
      // showDenyButton: true,
      showCancelButton: true,
      confirmButtonText: 'Submit',
      denyButtonText: `Don't save`,
      }).then((result) => {
          /* Read more about isConfirmed, isDenied below */
          if (result.isConfirmed) {
            $(".from_preloader").show();
            $.ajax({
              type: "post",
              url: "/add_bulk_cams_kfintech_mailback",
              cache: false,
              processData: false,
              contentType: false,
              enctype: "multipart/form-data",
              data: data,
              success: function (response) {
                  $(".from_preloader").hide();
                  window.location.href = "/mailback_transaction";
                  toastr.success(response);
                },
                error: function (response) {
                  console.log("error messages");
                  toastr.error(response.responseJSON);
                  $(".from_preloader").hide();
                },
          });
          }
      })
  });

//   $("body").on("click",".edit_modal", function () {
//     id = $(this).data("id")
//     $("#edit_mfm_form").prop("action", `/edit_mfm/${id}`);
//     $.ajax({
//       url: `load_edit_mfm/${id}`,
//       success: function (response) {
//         // console.log("response",response);
//         let data = response[0]
//           $("#edit_mfm_form #scheme_name").val(data.SCHEME)
//           $("#edit_mfm_form #e_c_payout").val(data.E_C_P)
//           $("#edit_mfm_form #net_a_gst").val(data.NET_A_GST)
//           $("#edit_mfm_form #ep_payout").val(data.EP_PAYOUT)
//       }
//     });
// });

// $("#edit_mfm_form").on("submit", function (e) {
// 	e.preventDefault();
// 	data = $(this).serializeArray();
// 	url = $(this).attr("action");
// 	$.ajax({
// 		type: "post",
// 		url: url,
// 		data: data,
// 		success: function (response) {
// 			$("#edit_mf_master").modal("toggle");
// 			t.ajax.reload(null, false);
// 			toastr.success(response);
// 		},
// 		error: function (response) {
// 			toastr.error("Something went wrong");
// 		},
// 	});
// });