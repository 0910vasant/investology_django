
var t

t = $('#scheme_table').DataTable( {
  processing: true,
  dom: 'rpl<"label"B>fti',
    // order:[],
    buttons: [
        {
            extend: "csv",
			title:	"Scheme Details",
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
  ajax: '/load_scheme',

  columns: [
      { data: null },
      { data: null },
      // { data: "SCHEME_CODE" },
      // { data: "FUND_CODE__COMPANY" },
      // { data: "FUND_CODE__COMPANY_FUND_CODE" },
      { data: null },
      { data: 'PLAN_NAME' },
      // { data: 'PLAN_TYPE' },
      // { data: 'PRI_ISIN' },
      // { data: 'SEC_ISIN' },
      { data: null },
  ],
 
  columnDefs: [
      { className: 'text-center', targets: [0,1,2,3,4] },
      {
        targets: [1],
            render: function (a, b, data, d) {
                let html
                html1 = `<p style="text-align: center;margin-bottom: 0px;white-space: nowrap;padding-left:0px;padding-right:0px;">Fund Code: ${data.FUND_CODE__FUND_CODE}`
                html2 = `<br>Scheme Code: ${data.SCHEME_CODE}</p></p>`
                html = html1 + html2
              return html;
            },
      },

      {
        targets: [2],
            render: function (a, b, data, d) {
              let product_code
              if (data.FUND_CODE__COMPANY == "kfintech") {
                product_code = (data.FUND_CODE__COMPANY_FUND_CODE+data.SCHEME_CODE).slice(0, -1);
              } else {
                product_code = data.FUND_CODE__FUND_CODE+data.SCHEME_CODE
              }
              let html

              html1 = `<p style="text-align: center;margin-bottom: 0px;white-space: nowrap;padding-left:0px;padding-right:0px;">Name: ${data.FUND_CODE__COMPANY}`
              html2 = `<br>Fund Code: ${data.FUND_CODE__COMPANY_FUND_CODE}`
              html3 = `<br>Product Code: ${product_code}</p>`

              html = html1 + html2 + html3
              return html;
            },
      },
      {
        targets: [4],
            render: function (a, b, data, d) {
              let html
              if(data.PUR_ALLOWED == "Y"){
                html = '<i class="bi-check-circle-fill"></i>'
              }
              else{
                html = '<i class="bi-x-circle-fill"></i>'
              }
            return html;
          },
      },
      {
        targets: [5],
            render: function (a, b, data, d) {
              let html
              if(data.SIP_ALLOWED == "Y"){
                html = '<i class="bi-check-circle-fill"></i>'
              }
              else{
                html = '<i class="bi-x-circle-fill"></i>'
              }
            return html;
          },
      },
      {
        targets: [6],
            render: function (a, b, data, d) {
              let html
              if(data.SWP_ALLOWED == "Y"){
                html = '<i class="bi-check-circle-fill"></i>'
              }
              else{
                html = '<i class="bi-x-circle-fill"></i>'
              }
            return html;
          },
      },

//       PUR_ALLOWED
// SIP_ALLOWED
// SWP_ALLOWED
        

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
        targets: [7], render: function (a, b, data, d){
          // console.log(d)
          html = `<div class="dropdown">
                    <button class="btn btn-secondary dropdown-toggle py-1" type="button" id="dropdownMenuButton1" data-bs-toggle="dropdown" aria-expanded="false">
                        Action
                    </button>
                    <ul class="dropdown-menu" aria-labelledby="dropdownMenuButton1">
                      <li><a class="dropdown-item py-1" href="scheme_details/${data.id}">Details</a></li>
                    </ul>
                  </div>`
                  // <hr class="drop-hr">
                  //         <a class="dropdown-item delete" href="javascript:void(0);" data-id="${data.id}"><i class="fa fa-trash"></i> Delete</a>
         return html
        },
      }
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
              url: "/add_bulk_scheme",
              cache: false,
              processData: false,
              contentType: false,
              enctype: "multipart/form-data",
              data: data,
              success: function (response) {
                  $(".from_preloader").hide();
                  window.location.href = "/buy_scheme";
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