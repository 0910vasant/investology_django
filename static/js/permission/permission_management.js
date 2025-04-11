// $(function () {
//   $(".allowed_modules").on("change", function () {
//     let hidden_modules = $(this).parents(".row").find(".hidden_modules")
//     $.each($(this).val(), function (i, v) {
//         $(hidden_modules).find(`option[value=${v}]`).hide()
//     });

//     $.each($(this).find(`option:not(:selected)`), function (i, v) {
//         $(hidden_modules).find(`option[value=${v.value}]`).show()
//     });
// });

// $(".hidden_modules").on("change", function () {
//   let allowed_modules = $(this).parents(".row").find(".hidden_modules")
//     $.each($(this).val(), function (i, v) {
//         $(allowed_modules).find(`option[value=${v}]`).hide()
//     });

//     $.each($(this).find(`option:not(:selected)`), function (i, v) {
//         $(allowed_modules).find(`option[value=${v.value}]`).show()
//     });
// });
// });

var t;

t = $("#user_roll_table").DataTable({
	ajax: "/load_role_permission",
	columns: [
        { data: null }, 
        { data: "USER_TYPE" },
        { data: "ALLOWED_MODULES" },
        { data: null }],
	columnDefs: [
		{ className: "text-center", targets: [0, 1, 2, 3] },
    {
			targets: [1],
			render: function (a, b, data, d) {
				// console.log(d)
        let html
        u_type = data.USER_TYPE
        if(u_type == "superadmin"){
          html = "Superadmin"
        }
        else if(u_type == "admin"){
          html = "Admin"
        }
        else if(u_type == "bm"){
          html = "Branch Manager"
        }
        else if(u_type == "rm"){
          html = "Relationship Manager"
        }
        else if(u_type == "ep"){
          html = "Easy Partner"
        }
        else if(u_type == "bo"){
          html = "Back Office"
        }
				return html;
			},
		},
		{
			targets: [3],
			render: function (a, b, data, d) {
				// console.log(d)
				html = `<div class="dropdown">
                            <button class="btn btn-secondary dropdown-toggle" type="button" id="dropdownMenuButton" data-toggle="dropdown" aria-haspopup="true" aria-expanded="false">
                            Action
                            </button>
                            <div class="dropdown-menu" aria-labelledby="dropdownMenuButton">
                            <a class="dropdown-item edit_modal" data-toggle="modal" href="javascript:void(0);" data-target="#edit_permission_modal" data-id="${data.id}"><i class="fa fa-edit"></i> Edit</a>
                            <a class="dropdown-item delete" data-id="${data.id}" href="javascript:void(0);"><i class="fa fa-trash"></i> Delete</a>
                            </div>
                        </div>`;
				return html;
			},
		},
	],
});
t.on("order.dt search.dt", function () {
	t.column(0, { search: "applied", order: "applied" })
		.nodes()
		.each(function (cell, i) {
			cell.innerHTML = i + 1;
		});
}).draw();


$("#add_permission_form").submit(function (e) {
    e.preventDefault();
    data = $(this).serializeArray()
    // console.log(data)
    $.ajax({
      type: "post",
      url: "/add_role_permission",
      data: data,
      success: function (response) {
        toastr.success(response)
        $("#add_permission_modal").modal("toggle")
        $("#add_permission_form").trigger("reset")
        $(".select2").val("").change()
        t.ajax.reload()
      },
      error: function (response){
        // console.log("response",response);
        if (response.status == 412) {
          toastr.info(response.responseJSON)
        }
        else{
          toastr.error("Something went wrong")
        }
      }
    });
  });

$("body").on("click", ".edit_modal", function () {
	let id = $(this).data("id");
	// console.log("entered",id);
	url = `/get_role_permission/${id}`;
	$("#edit_permission_form").prop("action", `/edit_role_permission/${id}`);
	$.ajax({
		type: "get",
		url: url,
		success: function (response) {
            console.log("res",response);
            d = response[0].ALLOWED_MODULES
			$("#edit_permission_form #user_type").val([response[0].USER_TYPE]).change();
			$("#edit_permission_form #allowed_modules").val(d.split(",")).change();
		},
		error: function (response) {
			// console.log("error",response);
		},
	});
});

$("#edit_permission_form").submit(function (e) {
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
        $("#edit_permission_modal").modal("toggle")
        t.ajax.reload()
      },
      error: function (response){
        toastr.error("Something went wrong")
      }
    });
});


$("body").on("click",".delete", function () {
  let id = $(this).data("id");
  $.ajax({
    type: "get",
    url: `/delete_role_permission/${id}`,
    success: function (response) {
        toastr.success(response)
        t.ajax.reload()
      },
      error: function (response){
      }
  });
});