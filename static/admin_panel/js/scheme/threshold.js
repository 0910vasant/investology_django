
var t
t = $('#threshold_table').DataTable( {
  processing: true,
  ajax: '/load_threshold',

  columns: [
      { data: null },
      { data: "FUND_CODE" },
      { data: 'SCHEME_CODE' },
      { data: 'TXN_TYPE' },
      { data: null },
  ],
 
  columnDefs: [
      { className: 'text-center', targets: [0,1,2,3,4] },
      {
        targets: [4], render: function (a, b, data, d){
          // console.log(d)
          html = `<div class="dropdown">
                    <button class="btn btn-secondary dropdown-toggle py-1" type="button" id="dropdownMenuButton1" data-bs-toggle="dropdown" aria-expanded="false">
                        Action
                    </button>
                    <ul class="dropdown-menu" aria-labelledby="dropdownMenuButton1">
                      <li><a class="dropdown-item py-1" href="/threshold_details/${data.id}">Details</a></li>
                    </ul>
                  </div>
                </td>`
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


$("#add_threshold_form").on("submit", function (e) {
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
              url: "/add_bulk_threshold",
              cache: false,
              processData: false,
              contentType: false,
              enctype: "multipart/form-data",
              data: data,
              success: function (response) {
                  $(".from_preloader").hide();
                  window.location.href = "/buy_threshold";
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
            //         url: "/add_bulk_threshold",
            //         success: function (response) {
            //             $(".from_preloader").hide();
            //             window.location.href = "/buy_threshold";
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