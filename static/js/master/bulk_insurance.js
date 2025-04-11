var t

t = $('#insurance_master_table').DataTable( {
  ajax: '/load_im_data',

  columns: [
      { data: null },
      { data: "INSURER" },
      { data: 'PRODUCT' },
      { data: 'PLAN_TYPE' },
      { data: 'PPT' },
      { data: 'PT' },
      { data: 'PB_G_OFF' },
      { data: 'PB_G_OFF_PERCENT' },
      { data: 'PB_RENEW_OFF' },
      { data: 'PB_RENEW_OFF_PERCENT' },
      { data: 'PB_GRID_ON' },
      { data: 'PB_GRID_ON_PERCENT' },
      { data: null },
  ],
 
  columnDefs: [
      { className: 'text-center', targets: [0,1,2,3,4,5,6,7,8,9,10,11,12] },
      {
        targets: [12], render: function (a, b, data, d){
          // console.log(d)
          html = `<div class="dropdown">
                      <button class="btn btn-secondary dropdown-toggle" type="button" id="dropdownMenuButton" data-toggle="dropdown" aria-haspopup="true" aria-expanded="false">
                      Action
                      </button>
                      <div class="dropdown-menu" aria-labelledby="dropdownMenuButton">
                          <a class="dropdown-item edit_modal" data-toggle="modal" href="javascript:void(0);" data-target="#edit_insurance_master" data-id="${data.id}"><i class="fa fa-edit"></i> Edit</a>
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


$("#add_insurace_master_form").on("submit", function (e) {
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
              url: "/add_bulk_insurance_excel",
              cache: false,
              processData: false,
              contentType: false,
              enctype: "multipart/form-data",
              data: data,
              success: function (response) {
                $.ajax({
                    type: "get",
                    url: "/add_insurance_master_bulk",
                    success: function (response) {
                        window.location.href = "/insurance_master";
                        toastr.success(response.message);
                    }
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
    $("#edit_im_form").prop("action", `/edit_im/${id}`);
    $.ajax({
      url: `load_edit_im/${id}`,
      success: function (response) {
        // console.log("response",response);
        let data = response[0]

          $("#edit_im_form #insurer_name").val(data.INSURER)
          $("#edit_im_form #product").val(data.PRODUCT)
          $("#edit_im_form #plan_type").val(data.PLAN_TYPE)
          $("#edit_im_form #ppt").val(data.PPT)
          $("#edit_im_form #pt").val(data.PT)
          $("#edit_im_form #pb_off").val(data.PB_G_OFF)
          $("#edit_im_form #pb_off_percent").val(data.PB_G_OFF_PERCENT)
          $("#edit_im_form #pb_renew").val(data.PB_RENEW_OFF)
          $("#edit_im_form #pb_renew_percent").val(data.PB_RENEW_OFF_PERCENT)
          $("#edit_im_form #pb_on").val(data.PB_GRID_ON)
          $("#edit_im_form #pb_on_percent").val(data.PB_GRID_ON_PERCENT)
      }
    });
});

$("#edit_im_form").on("submit", function (e) {
	e.preventDefault();
	data = $(this).serializeArray();
	url = $(this).attr("action");
	$.ajax({
		type: "post",
		url: url,
		data: data,
		success: function (response) {
			$("#edit_insurance_master").modal("toggle");
			t.ajax.reload(null, false);
			toastr.success(response);
		},
		error: function (response) {
			toastr.error("Something went wrong");
		},
	});
});

$("#button_add_im_data").on("submit", function (e) {
  console.log("done")
});