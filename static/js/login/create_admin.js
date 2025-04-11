var t

t = $('#admin_table').DataTable( {
  ajax: '/load_admin',
  columns: [
      { data: null },
      { data: 'NAME' },
      { data: 'USERNAME' },
    //   { data: 'NAME' },
      { data: null },
  ],
 
  columnDefs: [
      { className: 'text-center', targets: [0,1,2,3] },
      {
        targets: [3], render: function (a, b, data, d){
            // console.log(d)
            html = `<div class="dropdown">
                        <button class="btn btn-secondary dropdown-toggle" type="button" id="dropdownMenuButton" data-toggle="dropdown" aria-haspopup="true" aria-expanded="false">
                        Action
                        </button>
                        <div class="dropdown-menu" aria-labelledby="dropdownMenuButton">
                             <a class="dropdown-item" data-toggle="modal" href="javascript:void(0);" data-target="#viewModal"><i class="fa fa-eye" aria-hidden="true"></i> View</a>
                            <hr class="drop-hr"> 
                            <a class="dropdown-item edit_modal" data-toggle="modal" href="javascript:void(0);" data-id=${data.id} data-target="#edit_admin"><i class="fa fa-edit"></i> Edit</a>
                            <hr class="drop-hr">
                            <a class="dropdown-item fp" data-toggle="modal" href="javascript:void(0);" data-u_type="admin" data-id=${data.id} data-target="#forgot_password_modal"><i class="fas fa-question" aria-hidden="true"></i>Fogot Password</a>
                        </div>
                    </div>`
           return html
        },
      },
  ],
  } );
  t.on( 'order.dt search.dt', function () {
      t.column(0, {search:'applied', order:'applied'}).nodes().each( function (cell, i) {
          // console.log(i,cell)
          cell.innerHTML = i+1;
      } );
  } ).draw();

$("#create_admin_form").submit(function (e) {
    e.preventDefault();
    data = $(this).serializeArray()
    console.log("data",data);
    password = data[3].value
    password1 = data[4].value

    console.log("password",password,"password1",password1);
    if (password == password1) {
        // toastr.success("Sucess")
        $.ajax({
            type : "post",
            url  : "/create_admin",
            data : data ,
            success: function (response) {
              toastr.success(response)
              $("#create_admin").modal("toggle");
            //   window.location.reload()
            },
            error: function (response) {
              toastr.error(response.responseJSON)
            },
          });
    }
    else{
        toastr.error("Password And Confirm Paswword must Be same")
    }
});

$("#create_admin").on("hidden.bs.modal", function (e) {
	$("#create_admin_form").trigger("reset");
	$("#create_admin_form .select2").change();
});

// create_admin_form


$("body").on("click",".edit_modal", function () {
  let id = $(this).data("id")
  url = `/get_admin/${id}`
  $("#edit_admin_form").prop("action", `/edit_admin/${id}`);
  $.ajax({
      type: "get",
      url: url,
      success: function (response) {
        console.log("response",response);
        // console.log("response",response[0].NAME);
        let data = response[0]
        $("#edit_admin_form #admin_name").val(data.NAME)
        $("#edit_admin_form #username_a").val(data.USERNAME)
      },
      error: function (response){
          // console.log("error",response);
      }
  });
});

$("#edit_admin_form").submit(function (e) {
  e.preventDefault();
  data = $(this).serializeArray()
  url = $(this).attr("action");
// console.log(data)
  $.ajax({
    type: "post",
    url: url,
    data: data,
    success: function (response) {
      toastr.success(response)
      $("#edit_admin").modal("toggle")
      t.ajax.reload()
    },
    error: function (response){
      toastr.error("Something went wrong")
    }
  });
});