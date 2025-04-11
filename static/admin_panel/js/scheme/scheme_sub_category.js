var t

t = $('#add_scheme_sub_category_table').DataTable( {
  ajax: '/load_sub_scheme_category',

  columns: [
      { data: null },
      { data: 'CATEGORY__CATEGORY' },
      { data: 'SUB_CATEGORY' },
      { data: 'SUB_CATEGORY_ID' },
    //   { data: 'NAME' },
      { data: null },
  ],
 
  columnDefs: [
      { className: 'text-center', targets: [0,1,2,3,4] },
      {
          // puts a button in the last column
        // targets: [1], render: function (a, b, data, d){
        //   html = `${moment(data.CREATED_DATE, 'DD-MM-YYYY')}`
        //   console.log("data.CREATED_DATE",data.CREATED_DATE);
        //   console.log("html",html);
        // return html
        // },
        targets: [4], render: function (a, b, data, d){
            // console.log(d)
            html = `<div class="dropdown">
                    <button class="btn btn-secondary dropdown-toggle py-1" type="button" id="dropdownMenuButton1" data-bs-toggle="dropdown" aria-expanded="false">
                        Action
                    </button>
                    <ul class="dropdown-menu" aria-labelledby="dropdownMenuButton1">
                    <li><a class="dropdown-item py-1 edit_modal" href="javascript:void(0)" data-id="${data.id}" data-bs-toggle="modal" data-bs-target="#edit_scheme_sub_category">Edit</a></li>
                    </ul>
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


$("#add_sub_category_form").submit(function (e) { 
    e.preventDefault();
    data = $(this).serializeArray();
    $.ajax({
        type: "post",
        url: "/add_scheme_sub_category",
        data: data,
        success: function (response) {
            $("#add_scheme_sub_category").modal("toggle");
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

$('#add_scheme_sub_category').on('hidden.bs.modal', function (e) {
    $("#add_sub_category_form").trigger("reset")
    $("#add_sub_category_form select").val("")
})

$("body").on("click",".edit_modal", function () {
    let id = $(this).data("id")
    console.log("entered",id);
    $("#edit_sub_category_form").prop("action",`/edit_scheme_sub_category/${id}`)
    $.ajax({
        type: "get",
        url: `/get_scheme_sub_category/${id}`,
        success: function (response) {
          console.log("response",response);
          $("#edit_sub_category_form #category").val(response[0].CATEGORY).change();
          $("#edit_sub_category_form #sub_category").val(response[0].SUB_CATEGORY);
          $("#edit_sub_category_form #sub_category_id").val(response[0].SUB_CATEGORY_ID);

        },
        error: function (response){
            // console.log("error",response);
        }
    });
});

$("#edit_sub_category_form").on('submit', function (e) {
  e.preventDefault()
  data = $(this).serializeArray()
  url = $(this).attr('action');
  $.ajax({
    type: "post",
    url: url,
    data : data ,
    success: function (response) {
      $("#edit_scheme_sub_category").modal("toggle");
      t.ajax.reload(null,false)
      toastr.success(response)
    },
    error: function (response) {
      toastr.error(response.responseJSON)
      console.log("error");
    },
  });
});