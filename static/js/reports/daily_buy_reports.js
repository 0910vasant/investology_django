// datatable code
var t;

t = $("#daily_buy_report_table").DataTable({
	dom: 'rpl<"label"B>fti',
    // order:[],
    buttons: [
        {
            extend: "csv",
			title:	"Daily Reports",
            // orientation: "potrait",
            // pageSize:"LEGEL"
            // exportOptions:{
            //     columns:[0,1,2,3,4,5,6,7]
            // }
			exportOptions: {
				columns:[0,1,2,3,4,5,6,7,8],
				format: {
					// colidx = [0,1,2,3,4,5,6,7]
					body: function ( inner, rowidx, colidx, node ) {
						return node.innerText;
					}
				}
			  }
        }
    ],
	ajax: "/daily_reports_api",
	columns: [
		{ data: null },
		{ data: null },
		{ data: null },
		{ data: null },
		{ data: null },
		{ data: null },
		{ data: null },
		{ data: null },
		{ data: null },
		{ data: null }],
	columnDefs: [
		{ className: "text-center", targets: [0,1,2,3,4,5,6,7,8,9] },
		{
			targets: [1], render: function (a, b, data, d){
			  // let date = new Date(Date)
			  let date = moment(data.CREATED_DATE).format('DD/MM/YYYY');
			  return date
			},
		},
		{
			targets: [2],
				render: function (a, b, data, d) {
					if (data.TABLE_NAME == "insurance") {
						html = data.CUSTOMER__RM_EP__NAME
					}
					else if(data.TABLE_NAME == "demat"){
						html = data.DEMAT_CUST__RM_EP__NAME
					}
					else{
						html = data.EP_RM__NAME
					}
				 	return html;
					
				},
		},
		{
			targets: [3],
				render: function (a, b, data, d) {
				  	if (data.TABLE_NAME == "insurance") {
						html = data.CUSTOMER__RM_EP__USERNAME
					}
					else if(data.TABLE_NAME == "demat"){
						html = data.DEMAT_CUST__RM_EP__USERNAME
					}
					else{
						html = data.EP_RM__USERNAME
					}
				 	return html;
				},
		},
		{
			targets: [4],
				render: function (a, b, data, d) {
					if (data.TABLE_NAME != "demat") {
						html = data.CUSTOMER__C_NAME
					}
					else{
						html = data.DEMAT_CUST__C_NAME
					}
				 	return html;
					
				},
		},
		{
			targets: [5],
				render: function (a, b, data, d) {
					if (data.TABLE_NAME != "demat") {
						html = data.CUSTOMER__PAN_NO
					}
					else{
						html = data.DEMAT_CUST__PAN_NO
					}
				 	return html;
					
				},
		},
		{
			targets: [6],
				render: function (a, b, data, d) {
					if (data.TABLE_NAME != "demat") {
						html = data.CUSTOMER__MOB_NO
					}
					else{
						html = data.DEMAT_CUST__MOB_NO
					}
				 	return html;
					
				},
		},
		{
			targets: [7],
				render: function (a, b, data, d) {
				  	if (data.TABLE_NAME == "insurance") {
						html = "INSURANCE"
					}
					else if (data.TABLE_NAME == "demat") {
						html = data.DEPOSITORY_TYPE.toUpperCase()
					}
					else if (data.TABLE_NAME == "buy_mf") {
						// type = data.BUY_TYPE.toUpperCase()
						html = "MF"+" "+ data.BUY_TYPE.toUpperCase()
					}
					else{
						html = data.BUY_TYPE.toUpperCase()

					}
				 	return html;
				},
		},
		{
			targets: [8],
				render: function (a, b, data, d) {
				  	if (data.TABLE_NAME == "insurance") {
						html = data.GROSS_AMT
					}
					else if (data.TABLE_NAME == "buy_fd") {
						html = data.AMOUNT
					}
					else if (data.TABLE_NAME == "buy_mf") {
						html = data.AMOUNT_INVESTED
					}
					else{
						html = data.COMMISSION
					}
				 	return html;
				},
		},
		
		// {
		// 	targets: [4],
		// 	render: function (a, b, data, d) {
		// 		let html;
		// 		html = `<p class="text-left" style="margin-bottom: 0px;white-space:nowrap;">Name: ${data.CUSTOMER__C_NAME}<br>Pan: ${data.CUSTOMER__PAN_NO}</p>`;
		// 		return html;
		// 	},
		// },
		{
			targets: [9],
			render: function (a, b, data, d) {
				
				// console.log(d)
				html = `<div class="dropdown">
                            <button class="btn btn-secondary dropdown-toggle" type="button" id="dropdownMenuButton" data-toggle="dropdown" aria-haspopup="true" aria-expanded="false">
                            Action
                            </button>
                            <div class="dropdown-menu" aria-labelledby="dropdownMenuButton">
                            <a class="dropdown-item load_buy_detail_reports" href="javascript:void(0);" data-id="${data.id}" data-table_name="${data.TABLE_NAME}"><i class="fa fa-info-circle"></i> Details</a>
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


$("body").on("click",".load_buy_detail_reports",function(){
	id = $(this).data("id")
	table_name = $(this).data("table_name")

	if (table_name == "insurance") {
		$.ajax({
			url: `/get_insurance/${id}`,
			success: function (response) {
				// console.log("respose insurance",response);
				data = response[0]
				$("#insurance_detail_modal").modal("toggle");

				$("#insurance_detail_modal #details_customer").val(data.CUSTOMER_NAME)
				$("#insurance_detail_modal #details_type_i").val(data.TYPE_INSURANCE_NAME)
				$("#insurance_detail_modal #details_i_name").val(data.INSURANCE_NAME)
				$("#insurance_detail_modal #details_i_p").val(data.INSURANCE_PERIOD)
				$("#insurance_detail_modal #details_date").val(data.START_DATE)
				$("#insurance_detail_modal #details_ppt").val(data.PPT)
				$("#insurance_detail_modal #details_pt").val(data.PT)
				$("#insurance_detail_modal #details_pb").val(data.PB_NAME)
				$("#insurance_detail_modal #details_net_p").val(data.NET_AMT)
				$("#insurance_detail_modal #details_gross_p").val(data.GROSS_AMT)
				$("#insurance_detail_modal #details_commission").val(data.COMMISSION)
				$("#insurance_detail_modal #details_commission_amt").val(data.COMMISSION_AMT)
				
			}
		});
	}
	else if (table_name == "buy_fd") {
		$.ajax({
			url: `/get_buy_fd/${id}`,
			success: function (response) {
				data = response[0]
				$("#fd_detail_modal").modal("toggle");
				if (data.USER_TYPE == "bm") {
					user_type = "Easy Investology"
				}
				else if(data.USER_TYPE == "rm"){
					user_type = "Relationship Manager"
				}
				else{
					user_type = "Easy Partner"
				}
				$("#fd_detail_modal_form #details_user_type").val(user_type)
				$("#fd_detail_modal #details_user").val(data.EP_RM_NAME)
				$("#fd_detail_modal_form #details_buy_type").val(data.BUY_TYPE.toUpperCase())
				$("#fd_detail_modal_form #details_customer").val(data.CUSTOMER_NAME)
				$("#fd_detail_modal_form #details_start_date").val(data.START_DATE)
				$("#fd_detail_modal_form #details_end_date").val(data.END_DATE)
				$("#fd_detail_modal_form #details_company_name").val(data.COMPANY_NAME)
				$("#fd_detail_modal_form #details_roi").val(data.INTEREST_RATE)
				$("#fd_detail_modal_form #details_tenure").val(data.TENURE)
				$("#fd_detail_modal_form #details_amt").val(data.AMOUNT)
				$("#fd_detail_modal_form #details_boi").val(data.BROKERAGE_PERCENTAGE)
				$("#fd_detail_modal_form #details_boi_amt").val(data.BROKERAGE_AMOUNT)
			}
		});
	}
	else if(table_name == "buy_mf"){
		$.ajax({
			url: `/get_buy_mf/${id}`,
			success: function (response) {
				// console.log("enter mf",response);
				data = response[0]
				$("#mf_detail_modal").modal("toggle");
				
				if (data.USER_TYPE == "bm") {
					user_type = "Easy Investology"
				}
				else if(data.USER_TYPE == "rm"){
					user_type = "Relationship Manager"
				}
				else{
					user_type = "Easy Partner"
				}
				$("#mf_detail_modal #details_user_type").val(user_type)
				$("#mf_detail_modal #details_user").val(data.EP_RM_NAME)
				$("#mf_detail_modal #details_date").val(data.DATE)
				$("#mf_detail_modal #details_customer").val(data.CUSTOMER_NAME)
				$("#mf_detail_modal #details_customer_status").val(data.CUSTOMER_STATUS)
				$("#mf_detail_modal #details_scheme_name").val(data.SCHEME_NAME)
				$("#mf_detail_modal #details_amt_i").val(data.AMOUNT_INVESTED)
				$("#mf_detail_modal #details_mode").val(data.MODE)
				$("#mf_detail_modal #details_buy_type").val(data.BUY_TYPE.toUpperCase())
			}
		});
	}
	else{
		$.ajax({
			url: `/get_demat_account/${id}`,
			success: function (response) {
				console.log("enter demat",response);
				data = response[0]
				$("#demat_acc_detail").modal("toggle");

				$("#demat_acc_detail #details_customer").val(data.DEMAT_CUST__C_NAME)
				$("#demat_acc_detail #details_depositary_type").val(data.DEPOSITORY_TYPE.toUpperCase())
				$("#demat_acc_detail #details_acc_no").val(data.ACC_NO)
				$("#demat_acc_detail #details_client_id").val(data.CLIENT_ID)
				$("#demat_acc_detail #details_demat_date").val(data.ACC_DATE)
				$("#demat_acc_detail #details_commission").val(data.COMMISSION)
			}
		});
	}
	
});

// $("body").on("submit","#daily_reports_filter_form",function(e){
// 	e.preventDefault()

// 	data = []
// 	data.push({'name':'payment_mode','value': $("#").val()})
// 	data.push({'name':'payment_mode','value': $("#").val()})
// 	console.log("data",data);
// });
$("#daily_reports_filter_form").submit(function (e) {
	e.preventDefault()
	data = $(this).serializeArray()
	// console.log("data",data);
	// console.log("data",data);
	$.ajax({
	  type: "get",
	  url: "/daily_reports_api",
	  data: data,
	  success: function (response) {
		// console.log("dsad",response);
		  t.clear();
		  t.rows.add(response.data);
		  t.draw();
	  }
	});
});