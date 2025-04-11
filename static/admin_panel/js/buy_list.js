var t;

t = $("#buy_list_table").DataTable({
	ajax: "/load_buy_list",
	columns: [
		{ data: null },
		{ data: "USER__NAME" }, 
		{ data: "USER__PAN_NO" },
		{ data: "USER__CAN" },
		{ data: "GROUPORDERNO" },
		{ data: null }],
	columnDefs: [
		{ className: "text-center", targets: [0, 1, 2, 3, 4,5] },
		
		// {
		// 	targets: [4],
		// 	render: function (a, b, data, d) {
		// 		return `<p style="margin-bottom:0px;text-align: left;padding-left:35px;padding-right:5px;">Name: ${data.CUSTOMER__C_NAME}<br> Pan No: ${data.CUSTOMER__PAN_NO}</p>`;
		// 	},
		// },
		{
			targets: [5],
			render: function (a, b, data, d) {
				// console.log(d)
				html = `<div class="dropdown">
                            <button class="btn btn-secondary dropdown-toggle py-1" type="button" id="dropdownMenuButton1" data-bs-toggle="dropdown" aria-expanded="false">
                                Action
                            </button>
                            <ul class="dropdown-menu" aria-labelledby="dropdownMenuButton1">
                            <li><a class="dropdown-item py-1" href="/buy_details/${data.id}">Details</a></li>
                            </ul>
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