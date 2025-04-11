var t

t = $('#branch_location_table').DataTable( {
  ajax: '/load_branch_location',

  columns: [
      { data: null },
      { data: 'NAME' },
    //   { data: 'NAME' },
      { data: null },
  ],
 
  columnDefs: [
      { className: 'text-center', targets: [0,1,2] },
      {
          // puts a button in the last column
        // targets: [1], render: function (a, b, data, d){
        //   html = `${moment(data.CREATED_DATE, 'DD-MM-YYYY')}`
        //   console.log("data.CREATED_DATE",data.CREATED_DATE);
        //   console.log("html",html);
        // return html
        // },
        targets: [2], render: function (a, b, data, d){
            // console.log(d)
            html = `<div class="dropdown">
                        <button class="btn btn-secondary dropdown-toggle" type="button" id="dropdownMenuButton" data-toggle="dropdown" aria-haspopup="true" aria-expanded="false">
                        Action
                        </button>
                        <div class="dropdown-menu" aria-labelledby="dropdownMenuButton">
                            <!--<a class="dropdown-item" data-toggle="modal" href="javascript:void(0);" data-target="#viewModal"><i class="fa fa-eye" aria-hidden="true"></i> View</a>
                            <hr class="drop-hr">-->
                            <a class="dropdown-item edit_modal" data-toggle="modal" href="javascript:void(0);" data-target="#edit_branch_master" data-id="${data.id}"><i class="fa fa-edit"></i> Edit</a>
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


  

$("#add_branch_master_form").submit(function (e) { 
    e.preventDefault();
    data = $(this).serializeArray();
    $.ajax({
        type: "post",
        url: "/add_branch_location",
        data: data,
        success: function (response) {
            $("#add_branch_master").modal("toggle");
            t.ajax.reload()
            toastr.success(response.message)
        },
        error: function (response) {
            // console.log("response",response);
            toastr.error(response.responseJSON.error)
            console.log("error");
        },
    });
});

$('#add_branch_master').on('hidden.bs.modal', function (e) {
    $("#add_branch_master_form").trigger("reset")
})

$("body").on("click",".edit_modal", function () {
    let id = $(this).data("id")
    // console.log("entered",id);
    url = `/edit_branch_location/${id}`

    $("#edit_branch_master_form").prop("action",url)
    $.ajax({
        type: "get",
        url: url,
        success: function (response) {
          console.log("response",response[0].NAME);
          $("#edit_branch_master_form #location_name").val(response[0].NAME);
        },
        error: function (response){
            // console.log("error",response);
        }
    });
});

$("#edit_branch_master_form").on('submit', function (e) {
    e.preventDefault()
    data = $(this).serializeArray()
    url = $(this).attr('action');
    $.ajax({
      type: "post",
      url: url,
      data : data ,
      success: function (response) {
        $("#edit_branch_master").modal("toggle");
        t.ajax.reload(null,false)
        toastr.success(response.message)
      },
      error: function (response) {
        toastr.error(response.responseJSON.error)
        console.log("error");
      },
    });
  });