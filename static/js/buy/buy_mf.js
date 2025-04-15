var t;

t = $("#buy_mf_table").DataTable({
	dom: 'rpl<"label"B>fti',
    // order:[],
    buttons: [
        {
            extend: "csv",
			title:	"MF Reports",
            // orientation: "potrait",
            // pageSize:"LEGEL"
            // exportOptions:{
            //     columns:[0,1,2,3,4,5,6,7]
            // }
			exportOptions: {
				columns:[0,1,2,7],
				format: {
					// colidx = [0,1,2,3,4,5,6,7]
					body: function ( inner, rowidx, colidx, node ) {
						return node.innerText;
					}
				}
			  }
        }
    ],
	ajax: "/load_buy_mf",
	columns: [
		{ data: null }, 
		{ data: "DATE" }, 
		{ data: "EP_RM__NAME" },
		{ data: "EP_RM__USERNAME" },
		{ data: null }, 
		{ data: "CUSTOMER_STATUS" }, 
		{ data: "SCHEME_NAME" }, 
		{ data: "AMOUNT_INVESTED" },
		{ data: "MODE" },
		{ data: "BUY_TYPE" },
		{ data: null }],
	columnDefs: [
		{ className: "text-center", targets: [0, 1, 2, 3, 4, 5, 6, 7, 8, 9 ,10] },
		// {
		// 	targets: [2],
		// 	render: function (a, b, data, d) {
		// 		return `<p style="margin-bottom:0px;text-align: left;white-space: nowrap;">Name: ${data.EP_RM__NAME}<br> Username: ${data.EP_RM__USERNAME}<br> User Type: ${data.USER_TYPE.toUpperCase()}</p>`;
		// 	},
		// },
		{
			targets: [4],
			render: function (a, b, data, d) {
				return `<p style="margin-bottom:0px;text-align: left;padding-left:35px;padding-right:5px;">Name: ${data.CUSTOMER__C_NAME}<br> Pan No: ${data.CUSTOMER__PAN_NO}</p>`;
			},
		},
		{
			targets: [10],
			render: function (a, b, data, d) {
				// console.log(d)
				html = `<div class="dropdown">
                            <button class="btn btn-secondary dropdown-toggle" type="button" id="dropdownMenuButton" data-toggle="dropdown" aria-haspopup="true" aria-expanded="false">
                            Action
                            </button>
                            <div class="dropdown-menu" aria-labelledby="dropdownMenuButton">
                            <a class="dropdown-item edit_modal" data-toggle="modal" href="javascript:void(0);" data-target="#edit_buy_mf_modal" data-id="${data.id}"><i class="fa fa-edit"></i> Edit</a>
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
			cell.innerHTML = i + 1;
		});
}).draw();

// add form submit
$("#add_buy_mf_form").submit(function (e) {
	e.preventDefault();
	data = $(this).serializeArray();
	$.ajax({
		type: "post",
		url: "/add_buy_mf",
		data: data,
		success: function (response) {
			$("#add_buy_mf_modal").modal("toggle");
			$("#add_buy_mf_form").trigger("reset")
      		$(".select2").val("").change()
			toastr.success(response);
			t.ajax.reload();
		},
		error: function (response) {
			toastr.error(response.responseJSON);
		},
	});
});

$("body").on("click", ".edit_modal", function () {
	let id = $(this).data("id");
	console.log("entered", id);
	url = `/get_buy_mf/${id}`;
	$("#edit_buy_mf_form").prop("action", `/edit_buy_mf/${id}`);
	$.ajax({
		type: "get",
		url: url,
		success: function (response) {
			$("#edit_buy_mf_form #u_type").val(response[0].USER_TYPE).change();
			$("#edit_buy_mf_form #user").val(response[0].EP_RM_id).change();
			$("#edit_buy_mf_form #date").val(response[0].DATE);
			$("#edit_buy_mf_form #customer").val(response[0].CUSTOMER_id).change();
			$("#edit_buy_mf_form #customer_status").val(response[0].CUSTOMER_STATUS).change();
			// $("#edit_buy_mf_form #scheme_name").val(response[0].SCHEME_NAME);
			$("#edit_buy_mf_form #scheme_name").val(response[0].SCHEME_NAME).change();
			$("#edit_buy_mf_form #amount_invested").val(response[0].AMOUNT_INVESTED);
			$("#edit_buy_mf_form #mode").val(response[0].MODE).change();
			$("#edit_buy_mf_form #buy_type").val(response[0].BUY_TYPE).change();
		},
		// selectEl.val('sugar').change();
		error: function (response) {
			// console.log("error",response);
		},
	});
});
// edit_buy_mf
// edit form submit
$("#edit_buy_mf_form").submit(function (e) {
	e.preventDefault();
	data = $(this).serializeArray();
	url = $(this).attr("action");
	$.ajax({
		type: "post",
		url: url,
		data: data,
		success: function (response) {
			$("#edit_buy_mf_modal").modal("toggle");
			toastr.success(response);
			t.ajax.reload();
		},
		error: function (response) {
			toastr.error(response.responseJSON);
		},
	});
});

$(".user,.u_type").change(function (e) {
	cust_type = "customer";
	// let cust_type = $(this).parents(".modal-body").find("#cust_t").val()
	let user = $(this).parents(".modal-body").find("#user").val();
	let u_type = $(this).parents(".modal-body").find("#u_type").val();
	let obj = $(this);

	// console.log("cust_type",cust_type);
	// console.log("user",user);
	// console.log("u_type",u_type);
	if (user != "" && user != null && u_type != "" && u_type != null) {
		$.ajax({
			type: "get",
			url: `/filter_customer`,
			data: {
				customer_type: cust_type,
				user: user,
				u_type: u_type,
			},
			async: false,
			success: function (response) {
				let customer_html = [`<option value="" disabled="" selected="">Please Select Customer</option>`];
				// if (cust_type == "customer_lead"){
				//   $.each(response, function (i, v) {
				//     customer_html.push(`<option value="${v.id}">${v.NAME} | ${v.MOBILE}</option>`)
				//   });
				// }

				if (cust_type == "customer" || cust_type == "lead") {
					$.each(response, function (i, v) {
						customer_html.push(`<option value="${v.id}">${v.C_NAME} | ${v.MOB_NO}</option>`);
					});
				}
				// $(this).closest(".modal-body").find("#customer").html(customer_html.join(""))
				// $(".customer").html(customer_html.join(""));
				obj.parents("form").find("#customer").html(customer_html.join(""));
			},
		});
	}
});

$("body").on("click", ".delete", function () {
	let id = $(this).data("id");
	$.ajax({
		type: "post",
		url: `/delete_buy_mf/${id}`,
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



$.ajax({
	url: "load_mfm_data",
	success: function (data) {
		dropdown = [`<option value="" disabled selected>Please Select Scheme</option>`]
		// console.log('data',data);
		console.log(data);
		loaded_mf_data = data
		$.each(data.data, function (i, v) { 
			// console.log('v',v);
			// dropdown = `<option value="${v.id}">${v.SCHEME}</option>`
			dropdown.push(`<option value="${v.id}">${v.SCHEME}</option>`);
			
		});

		// console.log('v',dropdown);
		// $('#scheme_name').append(dropdown);
		$('.scheme_name').html(dropdown.join(""));
		// $('#scheme_name_edit').html(dropdown.join(""));
	},
	error: function (data) {
		toastr.error("something went wrong");
	},
});

$("#amount_invested").on("change", function(){
	scheme_value = $("#scheme_name").val()
	console.log(scheme_value);
	amount = parseFloat($("#amount_invested").val());
	console.log(amount);
	$.ajax({
		url: `/load_edit_mfm/${scheme_value}`,
		success: function (data) {
			console.log(typeof(data[0]['NET_A_GST']));
			ei_commision = (amount / 100) *  data[0]['E_C_P'];
			net_gst = (ei_commision / 100) *  18.00;
			pay_out = ei_commision - net_gst;
			$("#ei_commision").val(ei_commision.toFixed(2));
			$("#net_gst").val(net_gst.toFixed(2));
			$("#pay_out").val(pay_out.toFixed(2));
			console.log(typeof(pay_out))
			if(amount < 10000000.00){
				console.log('Red Diamond')
				
				$("#advisors_scheme").val('Red Diamond');
				final_amount = (pay_out / 100) * 73;
				console.log(final_amount);
				$("#advisor_payout").val(final_amount.toFixed(2));
			}
			if((amount >= 10000000.00 && amount < 40000000.00)){
				console.log('Blue diamond')
				$("#advisors_scheme").val('Blue diamond');
				final_amount = (pay_out / 100) * 76;
				$("#advisor_payout").val(final_amount.toFixed(2));
			}
			if(amount >= 40000000.00 && amount < 70000000.00){
				console.log('h')
				$("#advisors_scheme").val('Pink Diamond');
				final_amount = (pay_out / 100) * 78;
				$("#advisor_payout").val(final_amount.toFixed(2));
			}
			if(amount >= 70000000.00 && amount < 120000000.00){
				console.log('h')
				$("#advisors_scheme").val('Emerald')
				final_amount = (pay_out / 100) * 80;
				$("#advisor_payout").val(final_amount.toFixed(2));
			}
			if(amount >= 120000000.00 && amount < 180000000.00){
				console.log('h')
				$("#advisors_scheme").val('Sapphire')
				final_amount = (pay_out / 100) * 82;
				$("#advisor_payout").val(final_amount.toFixed(2));
			}
			if(amount >= 180000000.00){
				console.log('h')
				$("#advisors_scheme").val('Red Ruby')
				final_amount = (pay_out / 100) * 85;
				$("#advisor_payout").val(final_amount.toFixed(2));
			}
		},
		error: function (data) {
			toastr.error("something went wrong");
		},
	});
	
});

// $("#advisors_scheme").on("change", function(){
// 	// amount = parseFloat($("#amount_invested").val());
// 	// console.log(amount)
// 	pay_out = parseFloat($("#pay_out").val());
// 	if($("#advisors_scheme").val() == 'Red Diamond' && amount < 10000000.00){
// 		final_amount = (pay_out.toFixed(2) / 100) * 73.00
// 		console.log(final_amount)
// 		$("#advisor_payout").val(final_amount.toFixed(2));
// 	}
// 	if($("#advisors_scheme").val() == 'Blue diamond' && (amount >= 10000000.00 && amount < 40000000.00)){
// 		final_amount = (pay_out.toFixed(2) / 100) * 76.00
// 		$("#advisor_payout").val(final_amount.toFixed(2));
// 	}
// 	if($("#advisors_scheme").val() == 'Pink Diamond' && (amount >= 40000000.00 && amount < 70000000.00)){
// 		final_amount = (pay_out.toFixed(2) / 100) * 78.00
// 		$("#advisor_payout").val(final_amount.toFixed(2));
// 	}
// 	if($("#advisors_scheme").val() == 'Emerald' && (amount >= 70000000.00 && amount < 120000000.00)){
// 		final_amount = (pay_out.toFixed(2) / 100) * 80.00
// 		$("#advisor_payout").val(final_amount.toFixed(2));
// 	}
// 	if($("#advisors_scheme").val() == 'Sapphire' && (amount >= 120000000.00 && amount < 180000000.00)){
// 		final_amount = (pay_out.toFixed(2) / 100) * 82.00
// 		$("#advisor_payout").val(final_amount.toFixed(2));
// 	}
// 	if($("#advisors_scheme").val() == 'Red Ruby' && amount > 180000000.00){
// 		final_amount = (pay_out.toFixed(2) / 100) * 85.00
// 		$("#advisor_payout").val(final_amount.toFixed(2));
// 	}
// });