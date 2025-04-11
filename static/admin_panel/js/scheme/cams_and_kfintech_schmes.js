
var t

t = $('#scheme_table').DataTable( {
  processing: true,
  dom: 'rpl<"label"B>fti',
    // order:[],
    buttons: [
        {
            extend: "csv",
			title:	"Cams & Kfintech Scheme Details",
            // orientation: "potrait",
            // pageSize:"LEGEL"
            // exportOptions:{
            //     columns:[0,1,2,3,4,5,6,7]
            // }
			exportOptions: {
				columns:[0,1,2,3,4,5,6,7,8,9],
				format: {
					// colidx = [0,1,2,3,4,5,6,7]
					body: function ( inner, rowidx, colidx, node ) {
						return node.innerText;
					}
				}
			  }
        }
    ],
  ajax: '/load_cams_kfintech_schemes',

  columns: [
      { data: null },
      { data: "COMPANY" },
      { data: "PRODCODE" },
      { data: "FUND_CODE" },
      { data: "SCHEME_CODE" },      
      { data: 'SCHEME_NAME' },
      { data: 'ISIN_NO' },
  ],
 
  columnDefs: [
      { className: 'text-center', targets: [0,1,2,3,4,5,6] },
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
      // {
      //   targets: [10], render: function (a, b, data, d){
      //     // console.log(d)
      //     html = `<div class="dropdown">
      //               <button class="btn btn-secondary dropdown-toggle py-1" type="button" id="dropdownMenuButton1" data-bs-toggle="dropdown" aria-expanded="false">
      //                   Action
      //               </button>
      //               <ul class="dropdown-menu" aria-labelledby="dropdownMenuButton1">
      //                 <li><a class="dropdown-item py-1" href="scheme_details/${data.id}">Details</a></li>
      //               </ul>
      //             </div>`
      //             // <hr class="drop-hr">
      //             //         <a class="dropdown-item delete" href="javascript:void(0);" data-id="${data.id}"><i class="fa fa-trash"></i> Delete</a>
      //    return html
      //   },
      // }
  ],
  } );
  t.on( 'order.dt search.dt', function () {
      t.column(0, {search:'applied', order:'applied'}).nodes().each( function (cell, i) {
          // console.log(i,cell)
          cell.innerHTML = i+1;
      } );
  } ).draw();


$("#add_scheme_form").on("submit", function (e) {
    e.preventDefault();
    console.log("enter suvmit");
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
              url: "/add_bulk_cams_kfintech_scheme",
              cache: false,
              processData: false,
              contentType: false,
              enctype: "multipart/form-data",
              data: data,
              success: function (response) {
                  $(".from_preloader").hide();
                  window.location.href = "/cams_kfintech_scheme";
                  toastr.success(response);
                },
                error: function (response) {
                  console.log("error messages");
                  toastr.error(response.responseJSON);
                  $(".from_preloader").hide();
                },
          });
            // $.ajax({
            //   type: "post",
            //   url: "/add_scheme_excel",
            //   cache: false,
            //   processData: false,
            //   contentType: false,
            //   enctype: "multipart/form-data",
            //   data: data,
            //   success: function (response) {
            //     $.ajax({
            //         type: "get",
            //         url: "/add_bulk_scheme",
            //         success: function (response) {
            //             $(".from_preloader").hide();
            //             window.location.href = "/buy_scheme";
            //             toastr.success(response);
            //           },
            //           error: function (response) {
            //             console.log("error messages");
            //             toastr.error(response.responseJSON);
            //             $(".from_preloader").hide();
            //           },
            //     });
            //   },
            //   error: function (response) {
            //     // console.log("error messages");
            //     $(".from_preloader").hide();
            //     toastr.error("Something Went Wrong");
            //   },
            // });
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