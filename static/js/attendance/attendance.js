var t;
if (user_type == "admin" || user_type == "superadmin") {
	t = $("#attendance_table").DataTable({
		ajax: "/load_attendance",

		columns: [
			{ data: null },
			{ data: "USER__NAME" },
			{ data: "USER__USERNAME" },
			{ data: null },
			{ data: "DATE" },
			{ data: "PUNCH_IN" },
			{ data: "PUNCH_OUT" },
			{ data: null },
			{ data: null },
		],

		columnDefs: [
			{ className: "text-center", targets: [0, 1, 2, 3, 4,5,6,7,8] },
    //   {
    //     targets: [1],
	// 			render: function (a, b, data, d) {
    //       let html = `<p style="text-align: left;margin-bottom: 0px;white-space: nowrap;">Username: ${data.USER__USERNAME} <br> Name: ${data.USER__NAME}</p>`
    //       return html;
    //     },
    //   },
	  {
        targets: [7],
			render: function (a, b, data, d) {
			let html
			if (data.REMARK == "" || data.REMARK == null) {
				html = "-"
			}
			else{
				html = data.REMARK
			}
			return html;
        },
      },
      
      {
		targets: [3],
				render: function (a, b, data, d) {
				let html
				tp = data.USER__USER_TYPE
				if (tp == "bm") {
					html = "Branch Manager"
				}
				else if(tp == "rm"){
					html = "Relationship Manager"
				}
				else{
					html = "Back Office"
				}
				return html;
       	 	},
      	},
		{
			targets: [8],
			render: function (a, b, data, d) {
				// console.log(d)
				let html;
				html = `<div class="dropdown">
							<button class="btn btn-secondary dropdown-toggle" type="button" id="dropdownMenuButton" data-toggle="dropdown" aria-haspopup="true" aria-expanded="false">
							Action
							</button>
							<div class="dropdown-menu" aria-labelledby="dropdownMenuButton">
								<a class="dropdown-item edit_modal" data-toggle="modal" href="javascript:void(0);" data-target="#edit_attendance_modal" data-id="${data.id}"><i class="fa fa-edit"></i> Edit</a>
							<hr class="drop-hr">
							<a class="dropdown-item delete" href="javascript:void(0);" data-id="${data.id}"><i class="fa fa-trash"></i> Delete</a>
						</div>
						</div>`
				// if (user_type == "admin" || user_type == "superadmin") {
				// 	html = html1 + html2 + html3;
				// } else {
				// 	html = html1 + html3;
				// }
				return html;
			},
		},
		],
	});
	t.on("order.dt search.dt", function () {
		t.column(0, { search: "applied", order: "applied" })
			.nodes()
			.each(function (cell, i) {
				// console.log(i,cell)
				cell.innerHTML = i + 1;
			});
	}).draw();
} else {
	t = $("#attendance_table").DataTable({
		ajax: "/load_attendance",

		columns: [
			{ data: null },
			{ data: "DATE" },
			{ data: "PUNCH_IN" },
			{ data: "PUNCH_OUT" },
			//   { data: 'NAME' },
			// { data: null },
		],

		// columnDefs: [
		// 	{ className: "text-center", targets: [0, 1, 2, 3, 4] },
		// 	{
		// 		targets: [4],
		// 		render: function (a, b, data, d) {
		// 			let html;
		// 			html1 = `<div class="dropdown">
        //                   <button class="btn btn-secondary dropdown-toggle" type="button" id="dropdownMenuButton" data-toggle="dropdown" aria-haspopup="true" aria-expanded="false">
        //                   Action
        //                   </button>
        //                   <div class="dropdown-menu" aria-labelledby="dropdownMenuButton">
        //                       <!-- <a class="dropdown-item" data-toggle="modal" href="javascript:void(0);" data-target="#viewModal"><i class="fa fa-eye" aria-hidden="true"></i> View</a>
        //                       <hr class="drop-hr"> -->`;
		// 			html2 = `<a class="dropdown-item edit_modal" data-toggle="modal" href="javascript:void(0);"data-target="#edit_attendance_modal" data-id="${data.id}"><i class="fa fa-edit"></i> Edit</a>
		// 					<hr class="drop-hr">
        //                     <a class="dropdown-item delete" href="javascript:void(0);" data-id="${data.id}"><i class="fa fa-trash"></i> Delete</a>`;
		// 			html3 = `</div>
        //               </div>`;
		// 			if (user_type == "admin" || user_type == "superadmin") {
		// 				html = html1 + html2 + html3;
		// 			} else {
		// 				html = html1 + html3;
		// 			}
		// 			return html;
		// 		},
		// 	},
		// ],
	});
	t.on("order.dt search.dt", function () {
		t.column(0, { search: "applied", order: "applied" })
			.nodes()
			.each(function (cell, i) {
				// console.log(i,cell)
				cell.innerHTML = i + 1;
			});
	}).draw();
}

$("#add_attendance_form").submit(function (e) {
	e.preventDefault();
	data = $(this).serializeArray();
	$.ajax({
		type: "post",
		url: "/add_attendance",
		data: data,
		success: function (response) {
			$("#add_attendance_modal").modal("toggle");
			t.ajax.reload();
			toastr.success(response.message);
		},
		error: function (response) {
			// console.log("response",response);
			toastr.error(response.responseJSON.error);
			console.log("error");
		},
	});
});

$("#add_attendance_modal").on("hidden.bs.modal", function (e) {
	$("#add_attendance_form").trigger("reset");
	$(".select2").val("").change()
});

$("body").on("click", ".edit_modal", function () {
	let id = $(this).data("id");
	url = `/edit_attendance/${id}`;
	$("#edit_attendance_form").prop("action", url);
	$.ajax({
		type: "get",
		url: url,
		// async:false,
		success: function (response) {
			// console.log("response",response,"type",response[0].USER__USER_TYPE,"id",response[0].USER__id);
			$("#edit_attendance_form #u_type").val(response[0].USER__USER_TYPE).change();
			$("#edit_attendance_form #user").val(response[0].USER__id).change();
			$("#edit_attendance_form #a_date").val(response[0].DATE);
			$("#edit_attendance_form #in_time").val(response[0].PUNCH_IN);
			$("#edit_attendance_form #out_time").val(response[0].PUNCH_OUT);
			$("#edit_attendance_form #remark").val(response[0].REMARK);
		},
		error: function (response) {
			// console.log("error",response);
		},
	});
});

$("#edit_attendance_form").submit(function (e) {
	e.preventDefault();
	data = $(this).serializeArray();
	url = $(this).attr("action");
	$.ajax({
		type: "post",
		url: url,
		data: data,
		success: function (response) {
			$("#edit_attendance_modal").modal("toggle");
			toastr.success(response);
			t.ajax.reload();
		},
		error: function (response) {
			toastr.error(response.responseJSON.error);
		},
	});
});


$(".user").on("submit", function (e) {
	e.preventDefault();
	data = $(this).serializeArray();
	url = $(this).attr("action");
	$.ajax({
		type: "post",
		url: url,
		data: data,
		success: function (response) {
			$("#edit_insurace_name").modal("toggle");
			t.ajax.reload(null, false);
			toastr.success(response.message);
		},
		error: function (response) {
			toastr.error(response.responseJSON.error);
			console.log("error");
		},
	});
});

$("body").on("click", ".delete", function () {
	let id = $(this).data("id");
	$.ajax({
		type: "post",
		url: `/delete_attendance/${id}`,
		data: {
			csrfmiddlewaretoken: $("input[name=csrfmiddlewaretoken]").val(),
			id: id,
		},
		success: function (response) {
			toastr.success(response);
			t.ajax.reload();
		},
		error: function (response) {
			toastr.error("something went wrong");
		},
	});
});
