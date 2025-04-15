// datatable code

var t;

t = $("#buy_fd_table").DataTable({
	ajax: "/load_buy_fd",
	columns: [
		{ data: null },
		{ data: "EP_RM__NAME" },
		{ data: "EP_RM__USERNAME" },
		{ data: "BUY_TYPE" },
		{ data: "CUSTOMER" },
		{ data: "START_DATE" },
		{ data: "END_DATE" },
		{ data: "COMPANY_NAME" },
		{ data: "TENURE" },
		{ data: "INTEREST_RATE" },
		{ data: "AMOUNT" },
		{ data: "BROKERAGE_PERCENTAGE" },
		{ data: "BROKERAGE_AMOUNT" },
		{ data: null }],
	columnDefs: [
		{ className: "text-center", targets: [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11,12,13] },
		// {
		// 	targets: [1],
		// 		render: function (a, b, data, d) {
		// 		  // let date = new Date(Date)
		// 		  let html = `<p style="text-align: left;margin-bottom: 0px;white-space: nowrap;">Username: ${data.EP_RM__USERNAME} <br> Name: ${data.EP_RM__NAME}</p>`
		// 		  return html;
		// 		},
		// },
		{
			targets: [3],
				render: function (a, b, data, d) {
					return data.BUY_TYPE.toUpperCase()
				},
		},
		{
			targets: [4],
			render: function (a, b, data, d) {
				let html;
				html = `<p class="text-left" style="margin-bottom: 0px;white-space:nowrap;">Name: ${data.CUSTOMER__C_NAME}<br>Pan: ${data.CUSTOMER__PAN_NO}</p>`;
				return html;
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
			//<a class="dropdown-item" data-toggle="modal" href="javascript:void(0);" data-target="#viewModal"><i class="fa fa-eye" aria-hidden="true"></i> View</a>
			// <hr class="drop-hr"></hr>
			targets: [13],
			render: function (a, b, data, d) {
				// console.log(d)
				html = `<div class="dropdown">
                            <button class="btn btn-secondary dropdown-toggle" type="button" id="dropdownMenuButton" data-toggle="dropdown" aria-haspopup="true" aria-expanded="false">
                            Action
                            </button>
                            <div class="dropdown-menu" aria-labelledby="dropdownMenuButton">
                            <a class="dropdown-item edit_modal" data-toggle="modal" href="javascript:void(0);" data-target="#edit_buy_fd_modal" data-id="${data.id}"><i class="fa fa-edit"></i> Edit</a>
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


// add form js
$("#add_buy_fd_form").on("submit", function (e) {
	e.preventDefault();
	data = new FormData(this);
	// for (let [key, value] of data) {
	// 	console.log("from_data", `${key}`, `${value}`);
	// }
	$.ajax({
		type: "post",
		url: "/add_buy_fd",
		cache: false,
		processData: false,
		contentType: false,
		enctype: "multipart/form-data",
		data: data,
		success: function (response) {
			$("#add_buy_fd_form").trigger("reset")
			$("#add_buy_fd_form .select2").val("").change()
			$("#add_buy_fd_modal").modal("toggle");
			toastr.success(response.message);
			t.ajax.reload();
		},
		error: function (response) {
			toastr.error(response.responseJSON.error);
		},
	});
});

// load data in edit modal
$("body").on("click", ".edit_modal", function () {
	let id = $(this).data("id");
	// console.log("entered",id);
	url = `/get_buy_fd/${id}`;
	$("#edit_buy_fd_form").prop("action", `/edit_buy_fd/${id}`);
	$.ajax({
		type: "get",
		url: url,
		success: function (response) {
			$("#edit_buy_fd_form #u_type").val(response[0].USER_TYPE).change();
			$("#edit_buy_fd_form #user").val(response[0].EP_RM_id).change();
			$("#edit_buy_fd_form #buy_type").val(response[0].BUY_TYPE).change();
			$("#edit_buy_fd_form #customer").val(response[0].CUSTOMER_id).change();
			$("#edit_buy_fd_form #s_date").val(response[0].START_DATE);
			$("#edit_buy_fd_form #e_date").val(response[0].END_DATE);
			$("#edit_buy_fd_form #comp_name").val(response[0].COMPANY_NAME);
			$("#edit_buy_fd_form #tenure").val(response[0].TENURE);
			$("#edit_buy_fd_form #roi").val(response[0].INTEREST_RATE);
			$("#edit_buy_fd_form #amt").val(response[0].AMOUNT);
			$("#edit_buy_fd_form #b_percentage").val(response[0].BROKERAGE_PERCENTAGE);
			$("#edit_buy_fd_form #b_amt").val(response[0].BROKERAGE_AMOUNT);
		},
		error: function (response) {
			// console.log("error",response);
		},
	});
});

// edit form submit
$("#edit_buy_fd_form").on("submit", function (e) {
	e.preventDefault();
	data = new FormData(this);
	url = $(this).attr("action");
	for (let [key, value] of data) {
		console.log("from_data", `${key}`, `${value}`);
	}
	$.ajax({
		type: "post",
		url: url,
		cache: false,
		processData: false,
		contentType: false,
		enctype: "multipart/form-data",
		data: data,
		success: function (response) {
			$("#edit_buy_fd_modal").modal("toggle");
			toastr.success(response);
			t.ajax.reload();
		},
		error: function (response) {
			toastr.error(response.responseJSON.error);
		},
	});
});

// load customer in add and edit modal dropdown
// $(document).ready(function () {
// 	$.ajax({
// 		type: "get",
// 		url: `/filter_customer?customer_type=customer`,
// 		success: function (response) {
// 			let customer_html = [`<option value="" disabled="" selected="">Please Select Customer</option>`];
// 			$.each(response, function (i, v) {
// 				customer_html.push(`<option value="${v.id}">${v.C_NAME} | ${v.MOB_NO}</option>`);
// 			});
// 			$(".customer").html(customer_html.join(""));
// 		},
// 	});
// });

// autocalculate brokerage amount on change of amount and brokerage percentage field value
$(".user,.u_type").change(function (e) {
	cust_type = "customer"
	// let cust_type = $(this).parents(".modal-body").find("#cust_t").val()
	let user = $(this).parents(".modal-body").find("#user").val()
	let u_type = $(this).parents(".modal-body").find("#u_type").val()
	let obj = $(this)
  
	// console.log("cust_type",cust_type);
	// console.log("user",user);
	// console.log("u_type",u_type);
	if (user != "" && user != null && u_type != "" && u_type != null) {
	  $.ajax({
		type: "get",
		url: `/filter_customer`,
		data: {
		  "customer_type": cust_type,
		  "user":user,
		  "u_type":u_type,
		},
		async:false,
		success: function (response) {
		  let customer_html = [`<option value="" disabled="" selected="">Please Select Customer</option>`]
		  // if (cust_type == "customer_lead"){
		  //   $.each(response, function (i, v) { 
		  //     customer_html.push(`<option value="${v.id}">${v.NAME} | ${v.MOBILE}</option>`)
		  //   });
		  // }
	
		  if (cust_type == "customer" || cust_type == "lead") {
			$.each(response, function (i, v) {
				customer_html.push(`<option value="${v.id}">${v.C_NAME} | ${v.MOB_NO}</option>`)
			});
		  }
			// $(this).closest(".modal-body").find("#customer").html(customer_html.join(""))
		  // $(".customer").html(customer_html.join(""));
			obj.parents("form").find("#customer").html(customer_html.join(""));
		}
	  });
	}
});


$(".b_percentage,.amt").keyup(function () {
	let row = $(this).parents(".row");
	let amt = row.find("#amt").val();
	let c_amt;
	brokerage_percentage = row.find("#b_percentage").val();
	if (amt != "" && brokerage_percentage != "") {
		c_amt = Math.round((parseInt(amt) * parseFloat(brokerage_percentage)) / 100);
		row.find(".b_amt").val(c_amt);
	} else {
		row.find(".b_amt").val("");
	}
});

// hide rate of interest field in form for pms and aif buy type
$(".buy_type").change(function (e) {
	let buy_type = $(this).val();
	let target = $(this).parents(".row").find("#roi");
	let end_date = $(this).parents(".row").find("#e_date");
	let tenure = $(this).parents(".row").find("#tenure");
	if (buy_type == "pms" || buy_type == "aif" || buy_type == "Unlisted shares" || buy_type == "Fractional property") {
		$(target).prop("required", false);
		$(target).parents(".col-md-12").hide();
		$(end_date).parents(".col-md-6").hide();
		
	} else {
		$(target).prop("required", true);
		$(target).parents(".col-md-12").show();
		$(end_date).parents(".col-md-6").show();
		
	}

	if(buy_type == "Unlisted shares"){
		$(tenure).parents(".col-md-6").hide();
	}else{
		$(tenure).parents(".col-md-6").show();
	}
});

// show rate of interest on modal close
$(".modal").on("hide.bs.modal", function () {
	$("input[name=roi]").prop("required", true);
	$("input[name=roi]").parents(".col-md-12").show();
});

$("#mf_customer_button").on("click", function (){
	$("#fd_add_customer").prop("hidden", false);
	$("#customer").prop("disabled", true);
	$("#customer").prop("required", false);
});

$("#tenure").on("change",function(){
	start_date = $("#s_date").val();
	tenure = $("#tenure").val();
	const specificStartDate = new Date(start_date);
	const endSpecificDate = new Date(specificStartDate);
	if(specificStartDate){
		endSpecificDate.setMonth(specificStartDate.getMonth() + parseInt(tenure));
	}
	$("#e_date").val(""+endSpecificDate.getFullYear()+"-"+String(endSpecificDate.getMonth() + 1).padStart(2, '0')+"-"+String(endSpecificDate.getDate() + 1).padStart(2, '0'));
});