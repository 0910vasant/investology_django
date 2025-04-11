var t

t = $('#leads_table').DataTable( {
  ajax: '/load_leads',

  columns: [
      { data: null },
    //   { data: null },
      { data: 'RM_EP__NAME' },
      { data: 'RM_EP__USERNAME' },
      { data: 'REQUIRE' },
      { data: 'C_NAME' },
      { data: 'MOB_NO' },
      { data: 'EMAIL' },
      { data: 'QUALIFICATION' },
      { data: 'ANNUAL_CTC' },
    //   { data: 'INDUSTRY_TYPE' },
    //   { data: 'NAME' },
      { data: null },
  ],
 
  columnDefs: [
        { className: 'text-center', targets: [0,1,2,3,4,5,6,7,8,9] },
        // {
        //     targets: [1], render: function (a, b, data, d){
        //         let html = `<p style="text-align: left;margin-bottom: 0px;white-space: nowrap;">Username: ${data.RM_EP__USERNAME} <br> Name: ${data.RM_EP__NAME}</p>`
        //         return html
        //     },
        // },
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
            targets: [9], render: function (a, b, data, d){
                // console.log(d)
                html = `<div class="dropdown">
                            <button class="btn btn-secondary dropdown-toggle" type="button" id="dropdownMenuButton" data-toggle="dropdown" aria-haspopup="true" aria-expanded="false">
                            Action
                            </button>
                            <div class="dropdown-menu" aria-labelledby="dropdownMenuButton">
                                <a class="dropdown-item" href="/edit_leads/${data.id}"><i class="fa fa-edit"></i> Edit</a>
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


  

// $("#add_insurace_name_form").submit(function (e) { 
//     e.preventDefault();
//     data = $(this).serializeArray();
//     $.ajax({
//         type: "post",
//         url: "/add_insurance_name",
//         data: data,
//         success: function (response) {
//             $("#add_insurace_name").modal("toggle");
//             t.ajax.reload()
//             toastr.success(response.message)
//         },
//         error: function (response) {
//             // console.log("response",response);
//             toastr.error(response.responseJSON.error)
//             console.log("error");
//         },
//     });
// });

// $('#add_insurace_name').on('hidden.bs.modal', function (e) {
//     $("#add_insurace_name_form").trigger("reset")
// })

// $("body").on("click",".edit_modal", function () {
//     let id = $(this).data("id")
//     // console.log("entered",id);
//     url = `/edit_insurance_name/${id}`

//     $("#edit_insurace_name_form").prop("action",url)
//     $.ajax({
//         type: "get",
//         url: url,
//         success: function (response) {
//           console.log("response",response[0].NAME);
//           $("#edit_insurace_name_form #insurance_name").val(response[0].NAME);
//         },
//         error: function (response){
//             // console.log("error",response);
//         }
//     });
// });

// $("#edit_insurace_name_form").on('submit', function (e) {
//     e.preventDefault()
//     data = $(this).serializeArray()
//     url = $(this).attr('action');
//     $.ajax({
//       type: "post",
//       url: url,
//       data : data ,
//       success: function (response) {
//         $("#edit_insurace_name").modal("toggle");
//         t.ajax.reload(null,false)
//         toastr.success(response.message)
//       },
//       error: function (response) {
//         toastr.error(response.responseJSON.error)
//         console.log("error");
//       },
//     });
//   });