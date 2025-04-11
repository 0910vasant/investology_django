var t

t = $('#can_error_list_table').DataTable( {
    processing: true,
    // dom: 'rpl<"label"B>fti',
    // order:[],
    buttons: [
        {
            extend: "csv",
			title:	"Can",
            // orientation: "potrait",
            // pageSize:"LEGEL"
            // exportOptions:{
            //     columns:[0,1,2,3,4,5,6,7]
            // }
			exportOptions: {
				columns:[0,1,2,3,4,5],
				format: {
					// colidx = [0,1,2,3,4,5,6,7]
					body: function ( inner, rowidx, colidx, node ) {
						return node.innerText;
					}
				}
			  }
        }
    ],
  ajax: '/load_can_error_data',

  columns: [
      { 
        "data": null, // This is for the serial number
        "render": function (data, type, row, meta) {
            return meta.row + 1; // Return row index + 1 for serial number
        }
      },
      { data: 'USER__NAME' },
      { data: 'USER__PAN_NO' },
      { data: 'USER__MOBILE' },
      { data: 'USER__EMAIL' },
      { data: null },
  ],
 
  columnDefs: [
        { className: 'text-center', targets: [0,1,2,3,4,5] },
        
        {
            targets: [5], render: function (a, b, data, d){
                // console.log(d)
                html = `<div class="dropdown">
                            <button class="btn btn-secondary dropdown-toggle py-1" type="button" id="dropdownMenuButton1" data-bs-toggle="dropdown" aria-expanded="false">
                                Action
                            </button>
                            <ul class="dropdown-menu" aria-labelledby="dropdownMenuButton1">
                            <li><a class="dropdown-item py-1 view" href="javascript:void(0)" data-id="${data.id}" data-bs-toggle="modal" data-bs-target="#view_req_res">View</a></li>
                            </ul>
                        </div>`
            return html
            },
        },
  ],
  } );

//   get_canerror_req_res

$("body").on("click",".view", function () {
console.log("entree click");
let id = $(this).data("id")
$.ajax({
    type: "GET",
    url: `/get_canerror_req_res/${id}`,
        success: function (response) {
            // toastr.success(response);
            console.log("response",response);
           
            html = `<p>${response[0].REQUEST}</p>
            <p>${response[0].RESPONSE}</p>`
            
            $("#view_req_res .modal-body").html(html)
      },
      error: function (response) {
        // console.log("error messages");
        toastr.error(response.responseJSON);
      },
});

});