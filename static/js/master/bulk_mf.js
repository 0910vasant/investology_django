// console.log("enter blukk mf");
var t

t = $('#mfm_table').DataTable( {
  ajax: '/load_mfm_data',

  columns: [
      { data: null },
      { data: "SCHEME" },
      { data: 'E_C_P' },
      { data: 'NET_A_GST' },
      { data: 'EP_PAYOUT' },
      { data: null },
  ],
 
  columnDefs: [
      { className: 'text-center', targets: [0,1,2,3,4,5] },
      {
        targets: [5], render: function (a, b, data, d){
          // console.log(d)
          html = `<div class="dropdown">
                      <button class="btn btn-secondary dropdown-toggle" type="button" id="dropdownMenuButton" data-toggle="dropdown" aria-haspopup="true" aria-expanded="false">
                      Action
                      </button>
                      <div class="dropdown-menu" aria-labelledby="dropdownMenuButton">
                          <a class="dropdown-item edit_modal" data-toggle="modal" href="javascript:void(0);" data-target="#edit_mf_master" data-id="${data.id}"><i class="fa fa-edit"></i> Edit</a>
                      </div>
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


$("#add_mf_master_form").on("submit", function (e) {
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
            $.ajax({
              type: "post",
              url: "/add_bulk_mf_excel",
              cache: false,
              processData: false,
              contentType: false,
              enctype: "multipart/form-data",
              data: data,
              success: function (response) {
                $.ajax({
                    type: "get",
                    url: "/add_mf_master_bulk",
                    success: function (response) {
                        window.location.href = "/mf_master";
                        toastr.success(response.message);
                      },
                      error: function (response) {
                        console.log("error messages");
                        toastr.error(response.responseJSON.error);
                      },
                });
              },
              error: function (response) {
                console.log("error messages");
                toastr.error("Something Went Wrong");
              },
            });
          }
      })
  });

  $("body").on("click",".edit_modal", function () {
    id = $(this).data("id")
    $("#edit_mfm_form").prop("action", `/edit_mfm/${id}`);
    $.ajax({
      url: `load_edit_mfm/${id}`,
      success: function (response) {
        // console.log("response",response);
        let data = response[0]
          $("#edit_mfm_form #scheme_name").val(data.SCHEME)
          $("#edit_mfm_form #e_c_payout").val(data.E_C_P)
          $("#edit_mfm_form #net_a_gst").val(data.NET_A_GST)
          $("#edit_mfm_form #ep_payout").val(data.EP_PAYOUT)
      }
    });
});

$("#edit_mfm_form").on("submit", function (e) {
	e.preventDefault();
	data = $(this).serializeArray();
	url = $(this).attr("action");
	$.ajax({
		type: "post",
		url: url,
		data: data,
		success: function (response) {
			$("#edit_mf_master").modal("toggle");
			t.ajax.reload(null, false);
			toastr.success(response);
		},
		error: function (response) {
			toastr.error("Something went wrong");
		},
	});
});

$("#download_advisors_scheme").on("change", function(){
  url = `http://127.0.0.1:8000/get_mf_master/${$("#download_advisors_scheme").val()}`;
  $("#download_mf_excel").attr('href', url)
  value=$("#download_mf_excel").attr('href')
});