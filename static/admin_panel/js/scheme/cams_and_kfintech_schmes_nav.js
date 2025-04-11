
var t

t = $('#nav_table').DataTable( {
  processing: true,
  // dom: 'rpl<"label"B>fti',
  //   // order:[],
  //   buttons: [
  //       {
  //           extend: "csv",
	// 		title:	"Cams & Kfintech Scheme NAV",
  //           // orientation: "potrait",
  //           // pageSize:"LEGEL"
  //           // exportOptions:{
  //           //     columns:[0,1,2,3,4,5,6,7]
  //           // }
	// 		exportOptions: {
	// 			columns:[0,1,2,3,4,5],
	// 			format: {
	// 				// colidx = [0,1,2,3,4,5,6,7]
	// 				body: function ( inner, rowidx, colidx, node ) {
	// 					return node.innerText;
	// 				}
	// 			}
	// 		  }
  //       }
  //   ],
  ajax: '/load_nav',

  columns: [
      { 
        data: null, // This is for the serial number
      },
      { data: null },
      { data: "COMPANY" },
      { data: "PRODCODE__PRODCODE" },
      { data: "PRODCODE__SCHEME_NAME" },
      { data: "NAV_VALUE" },
  ],

  columnDefs: [
      { className: 'text-center', targets: [0,1,2,3,4,5] },
      // puts a button in the last column
      {
        targets: [0], render: function (a, b, data, d){
         return d.row + 1;
        },
      },
      {
        targets: [1], render: function (a, b, data, d){
          html = moment(data.NAV_DATE).format('DD-MM-YYYY')
        return html
        },
      },
      {
        targets: [5], render: function (a, b, data, d){
         return parseFloat(data.NAV_VALUE).toFixed(2)
        },
      },
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


$("#add_nav_form").on("submit", function (e) {
    e.preventDefault();
    console.log("enter add_nav_form");
    data = new FormData(this);
    Swal.fire({
      title: 'Are you sure want to Submit NAV Excel?',
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
              url: "/add_bulk_cams_kfintech_nav",
              cache: false,
              processData: false,
              contentType: false,
              enctype: "multipart/form-data",
              data: data,
              success: function (response) {
                  $(".from_preloader").hide();
                  window.location.href = "/cams_kfintech_scheme_nav";
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
