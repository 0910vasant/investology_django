var t;

t = $("#follows_up_table").DataTable({
	ajax: "/load_followups",

	columns: [
		{ data: null },
		// { data: null },
		{ data: "RM_EP__NAME" },
      	{ data: "RM_EP__USERNAME" },
		{ data: "LEADS__C_NAME" },
		{ data: "DATE" },
		{ data: "TIME" },
		{ data: "REMARK" },
		//   { data: 'NAME' },
		{ data: null },
	],

	columnDefs: [
		{ className: "text-center", targets: [0,1,2,3,4,5,6,7] },
		
		// {
		// targets: [1],
		// 		render: function (a, b, data, d) {
		// 			// let date = new Date(Date)
		// 			let html = `<p style="text-align: left;margin-bottom: 0px;white-space: nowrap;padding-left:35px;padding-right:35px;">Username: ${data.RM_EP__USERNAME} <br> Name: ${data.RM_EP__NAME}</p>`
		// 			return html;
		// 		},
		// },
		// LEADS
		{
			targets: [4],
			render: function (a, b, data, d) {
				// let date = new Date(Date)
				let date = moment(data.DATE).format("DD/MM/YYYY");
				return date;
			},
		},
		{
			targets: [5],
			render: function (a, b, data, d) {
				let hours = parseInt(data.TIME.slice(0, 2));
				let minutes = parseInt(data.TIME.slice(3, 5));
				let ampm = hours >= 12 ? "PM" : "AM";
				hours = hours % 12;
				hours = hours ? hours : 12;
				minutes = minutes < 10 ? "0" + minutes : minutes;
				let time = `${hours} : ${minutes} ${ampm}`;
				return time;
			},
		},
		{
			// puts a button in the last column
			// targets: [1], render: function (a, b, data, d){
			//   html = `${moment(data.CREATED_DATE, 'DD-MM-YYYY')}`
			//   console.log("data.CREATED_DATE",data.CREATED_DATE);
			//   console.log("html",html);
			// return html
			// },
			targets: [7],
			render: function (a, b, data, d) {
				// console.log(d)
				html = `<div class="dropdown">
                        <button class="btn btn-secondary dropdown-toggle" type="button" id="dropdownMenuButton" data-toggle="dropdown" aria-haspopup="true" aria-expanded="false">
                        Action
                        </button>
                        <div class="dropdown-menu" aria-labelledby="dropdownMenuButton">
                          <a class="dropdown-item edit_modal" data-toggle="modal" href="javascript:void(0);" data-target="#edit_followup" data-id="${data.id}"><i class="fa fa-edit"></i> Edit</a>
                          <hr class="drop-hr">
                          <a class="dropdown-item delete" href="javascript:void(0);" data-id="${data.id}"><i class="fa fa-trash"></i> Delete</a>
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
			// console.log(i,cell)
			cell.innerHTML = i + 1;
		});
}).draw();

$("body").on("click", ".delete", function () {
	let id = $(this).data("id");
	$.ajax({
		type: "post",
		url: `/delete_followup`,
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

$("#add_followup_form").submit(function (e) {
	e.preventDefault();
	data = $(this).serializeArray();
	$.ajax({
		type: "post",
		url: "/add_followup",
		data: data,
		success: function (response) {
			$("#add_followup").modal("toggle");
			t.ajax.reload();
			toastr.success(response.message);
		},
		error: function (response) {
			// console.log("response",response);
			toastr.error("Something went wrong");
			console.log("error");
		},
	});
});

$("#add_followup").on("hidden.bs.modal", function (e) {
	$("#add_followup_form").trigger("reset");
	$("#add_followup_form .select2").change();
	// $(this)
	//   .find("select")
	//         .val('').change()
	//         .end()
	//   .find("input")
	//       .val('')
	//       .end()
});

$("body").on("click", ".edit_modal", function () {
	let id = $(this).data("id");
	// console.log("entered",id);
	url = `/edit_followup/${id}`;
	$("#edit_followup_form").prop("action", url);

	$.ajax({
		type: "get",
		url: url,
		success: function (response) {
			// console.log("response",response);
			// console.log("response",response[0].NAME);
			// $("#edit_followup_form #cust").val(response[0].LEADS_id).change();
			$("#edit_followup_form #u_type").val(response[0].TYPE).change();
			$("#edit_followup_form #user").val(response[0].RM_EP_id).change();
			$("#edit_followup_form #followup_date").val(response[0].DATE);
			$("#edit_followup_form #followup_time").val(response[0].TIME);
			$("#edit_followup_form #remark").val(response[0].REMARK);
		},
		error: function (response) {
			// console.log("error",response);
		},
	});
});

$("#edit_followup_form").on("submit", function (e) {
	e.preventDefault();
	data = $(this).serializeArray();
	url = $(this).attr("action");
	$.ajax({
		type: "post",
		url: url,
		data: data,
		success: function (response) {
			$("#edit_followup").modal("toggle");
			t.ajax.reload(null, false);
			toastr.success(response.message);
		},
		error: function (response) {
			toastr.error("Somethin went wrong");
		},
	});
});

// $(document).ready(function () {
//   load_cust()
// });

// $(".user").change(function () {
// 	// user = $("#user").val()
// 	user = $(this).parents(".row").find("#user").val();
// 	user_type = $(this).parents(".row").find("#u_type").val();
// 	load_cust(user,user_type);
// });

// function load_cust(user,user_type) {
// 	console.log("user",user,"user_type",user_type);
// 	if (user != null) {
// 		cust_data = [`<option value="" disabled selected>Please Select Customer</option>`];
// 		$.ajax({
// 			// url: `/load_leads?user=${user}`,
// 			url: `/load_lead_cust?user=${user}`,
// 			data:{
// 				"user":user,
// 				"u_type": user_type
// 			},
// 			async: false,
// 			success: function (response) {
// 				$.each(response.data, function (i, v) {
// 					cust_data.push(`<option value="${v.id}">${v.C_NAME} || ${v.MOB_NO}</option>`);
// 				});
// 				$(".l_data").html(cust_data.join(""));
// 			},
// 		});
// 	}
// }

$(".cust_t,.user,.u_type").change(function (e) {

	let cust_type = "lead"
	let user = $(this).parents(".modal-body").find("#user").val()
	let u_type = $(this).parents(".modal-body").find("#u_type").val()
  
	// console.log("cust_type",cust_type);
	// console.log("user",user);
	// console.log("u_type",u_type);
	if (cust_type != "" && cust_type != null  && user != "" && user != null && u_type != "" && u_type != null) {
	  console.log("enter If");
	  $.ajax({
		type: "get",
		url: `/filter_customer`,
		data: {
		  "customer_type":cust_type,
		  "user":user,
		  "u_type":u_type,
		},
		success: function (response) {
		console.log("response",response);
		  let customer_html = [`<option value="" disabled="" selected="">Please Select Customer</option>`]
		  // if (cust_type == "customer_lead"){
		  //   $.each(response, function (i, v) { 
		  //     customer_html.push(`<option value="${v.id}">${v.NAME} | ${v.MOBILE}</option>`)
		  //   });
		  // }
	
			$.each(response, function (i, v) {
			   customer_html.push(`<option value="${v.id}">${v.C_NAME} | ${v.MOB_NO} | ${v.PAN_NO}</option>`)
			});

		  	$("#cust").html(customer_html.join(""));
		}
	  });
	}
  });