var t

t = $('#scheme_category_table').DataTable( {
  ajax: '/load_scheme_category_table',

  columns: [
      { data: null },
      { data: 'CATEGORY' },
      { data: 'CATEGORY_ID' },
    //   { data: 'NAME' },
      { data: null },
  ],
 
  columnDefs: [
      { className: 'text-center', targets: [0,1,2,3] },
      {
          // puts a button in the last column
        // targets: [1], render: function (a, b, data, d){
        //   html = `${moment(data.CREATED_DATE, 'DD-MM-YYYY')}`
        //   console.log("data.CREATED_DATE",data.CREATED_DATE);
        //   console.log("html",html);
        // return html
        // },
        targets: [3], render: function (a, b, data, d){
            // console.log(d)
            html = `<div class="dropdown">
                      <button class="btn btn-secondary dropdown-toggle py-1" type="button" id="dropdownMenuButton1" data-bs-toggle="dropdown" aria-expanded="false">
                          Action
                      </button>
                      <ul class="dropdown-menu" aria-labelledby="dropdownMenuButton1">
                      <li><a class="dropdown-item py-1 edit_modal" data-id="${data.id}" href="javascript:void(0)" data-bs-toggle="modal" data-bs-target="#edit_scheme_category">Edit</a></li>
                      </ul>
                    </div>
                  </td>`
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


$("#add_scheme_category_form").submit(function (e) { 
    e.preventDefault();
    data = $(this).serializeArray();
    $.ajax({
        type: "post",
        url: "/add_scheme_category",
        data: data,
        success: function (response) {
            $("#add_scheme_category").modal("toggle");
            t.ajax.reload()
            toastr.success(response)
        },
        error: function (response) {
            // console.log("response",response);
            toastr.error(response.responseJSON)
            // console.log("error");
        },
    });
});

$('#add_scheme_category').on('hidden.bs.modal', function (e) {
    $("#add_scheme_category_form").trigger("reset")
})

$("body").on("click",".edit_modal", function () {
    let id = $(this).data("id")
    // console.log("entered",id);
    $("#edit_scheme_category_form").prop("action",`/edit_scheme_category/${id}`)
    $.ajax({
        type: "get",
        url: `/get_scheme_category/${id}`,
        success: function (response) {
          console.log("response",response);
          $("#edit_scheme_category_form #category").val(response[0].CATEGORY);
          $("#edit_scheme_category_form #category_id").val(response[0].CATEGORY_ID);

        },
        error: function (response){
            // console.log("error",response);
        }
    });
});

$("#edit_scheme_category_form").on('submit', function (e) {
  e.preventDefault()
  data = $(this).serializeArray()
  url = $(this).attr('action');
  $.ajax({
    type: "post",
    url: url,
    data : data ,
    success: function (response) {
      $("#edit_scheme_category").modal("toggle");
      t.ajax.reload(null,false)
      toastr.success(response)
    },
    error: function (response) {
      toastr.error(response.responseJSON)
      console.log("error");
    },
  });
});