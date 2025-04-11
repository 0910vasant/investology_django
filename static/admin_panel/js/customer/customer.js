var t

t = $('#customer_table').DataTable( {
    processing: true,
    // dom: 'rpl<"label"B>fti',
    // order:[],
    buttons: [
        {
            extend: "csv",
			title:	"Can",
            // orientation: "potrait",
            // pageSize:"LEGEL"
            // exportOptions:{
            //     columns:[0,1,2,3,4,5,6,7]
            // }
			exportOptions: {
				columns:[0,1,2,3,4,5],
				format: {
					// colidx = [0,1,2,3,4,5,6,7]
					body: function ( inner, rowidx, colidx, node ) {
						return node.innerText;
					}
				}
			  }
        }
    ],
  ajax: '/load_admin_customer',

  columns: [
      { 
        "data": null, // This is for the serial number
        "render": function (data, type, row, meta) {
            return meta.row + 1; // Return row index + 1 for serial number
        }
      },
      { data: "NAME" },
      { data: 'MOBILE' },
      { data: 'PAN_NO' },
      { data: 'CAN' },
      { data: null },
  ],
 
  columnDefs: [
        { className: 'text-center', targets: [0,1,2,3,4,5] },
        
        {
            targets: [5], render: function (a, b, data, d){
                // console.log(d)
                html = `<div class="dropdown">
                            <button class="btn btn-secondary dropdown-toggle py-1" type="button" id="dropdownMenuButton1" data-bs-toggle="dropdown" aria-expanded="false">
                                Action
                            </button>
                            <ul class="dropdown-menu" aria-labelledby="dropdownMenuButton1">
                            <li><a class="dropdown-item py-1" href="/customer_detail/${data.id}">Details</a></li>
                            <hr class="drop-hr">
                            <li><a class="dropdown-item py-1 edit_mobile_no" href="javascript:void(0);" data-id="${data.id}" data-bs-toggle="modal" data-bs-target="#change_mobile_no_modal"><i class="fa fa-edit" aria-hidden="true"></i>Edit Mobile No</a></li>
                 
                            </ul>
                        </div>`
            return html
            },
        },
  ],
  } );
  // <a class="dropdown-item edit_epcode" data-toggle="modal" href="javascript:void(0);" data-id=${data.LOGIN__id} data-target="#change_epcode_modal"><i class="fa fa-edit" aria-hidden="true"></i>Edit Ep Code</a>
//   t.on( 'order.dt search.dt', function () {
//       t.column(0, {search:'applied', order:'applied'}).nodes().each( function (cell, i) {
//           cell.innerHTML = i+1;
//       } );
//   } ).draw();

$("#add_bulk_customer_form").on("submit", function (e) {
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
              url: "/bulk_candata_creation",
              cache: false,
              processData: false,
              contentType: false,
              enctype: "multipart/form-data",
              data: data,
              success: function (response) {
                  $(".from_preloader").hide();
                  window.location.href = "/customer_management";
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

  $("#add_bulk_payeezz_form").on("submit", function (e) {
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
              url: "/bulk_prn_and_bank_data",
              cache: false,
              processData: false,
              contentType: false,
              enctype: "multipart/form-data",
              data: data,
              success: function (response) {
                  $(".from_preloader").hide();
                  window.location.href = "/customer_management";
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

  $("body").on("click",".edit_mobile_no", function () {
    let id = $(this).data("id")
    // console.log("entered",id);

    $("#change_mobile_no_form").prop("action",`/edit_user_mobile_no/${id}`)
    $.ajax({
        type: "post",
        url: `/get_user_mobile_no/${id}`,
        success: function (response) {
          console.log("response",response);

          $("#change_mobile_no_form #user_name").val(response.user_name);
          $("#change_mobile_no_form #mobile_no").val(response.mobile_no);
          
        },
        error: function (response){
            // console.log("error",response);
        }
    });
  });

  


  
  $("#change_mobile_no_form").on('submit', function (e) {
  e.preventDefault()
  data = $(this).serializeArray()
  url = $(this).attr('action');
  $.ajax({
    type: "post",
    url: url,
    data : data ,
    success: function (response) {
      $("#change_mobile_no_modal").modal("toggle");
      t.ajax.reload(null,false)
      toastr.success(response)
    },
    error: function (response) {
      toastr.error(response.responseJSON)
      console.log("error");
    },
  });
  });