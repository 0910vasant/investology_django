var t
t = $('#bm_brokerage_table_data').DataTable( {
  ajax: '/load_bm_brokerage_data',

  columns: [
      { data: null },
      { data: 'DOB' },
      { data: 'BM_NAME.NAME' },
      { data: 'AMC_NAME' },
      { data: 'TRAIL' },
      { data: null },
  ],
 
  columnDefs: [
      { className: 'text-center', targets: [0,1,2,3,4,5] },
      {
          // puts a button in the last column
        // targets: [1], render: function (a, b, data, d){
        //   html = `${moment(data.CREATED_DATE, 'DD-MM-YYYY')}`
        //   console.log("data.CREATED_DATE",data.CREATED_DATE);
        //   console.log("html",html);
        // return html
        // },
        targets: [5], render: function (a, b, data, d){
            // console.log(d)
            html = `<div class="dropdown">
                        <button class="btn btn-secondary dropdown-toggle" type="button" id="dropdownMenuButton" data-toggle="dropdown" aria-haspopup="true" aria-expanded="false">
                        Action
                        </button>
                        <div class="dropdown-menu" aria-labelledby="dropdownMenuButton">
                            <a class="dropdown-item" data-toggle="modal" href="javascript:void(0);" data-target="#viewModal" href="#"><i class="fa fa-eye" aria-hidden="true"></i> View</a>
                            <hr class="drop-hr">
                            <a class="dropdown-item" href="/edit_bm_brokerage/${data.id}"><i class="fa fa-edit"></i> Edit</a>
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