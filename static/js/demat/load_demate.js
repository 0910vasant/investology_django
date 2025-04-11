var t

t = $('#demate_table').DataTable( {
  ajax: '/load_demat_account',

  columns: [
      { data: null },
      { data: null },
      { data: "DEMAT_CUST__RM_EP__NAME" },
      { data: "DEMAT_CUST__RM_EP__USERNAME" },
      { data: "DEMAT_CUST__C_NAME" },
      { data: "DEMAT_CUST__MOB_NO" },
      
      { data: 'DEPOSITORY_TYPE' },
      { data: 'ACC_NO' },
      { data: 'CLIENT_ID' },
      
      { data: 'COMMISSION' },
    //   { data: 'NAME' },
      { data: null },
  ],
 
  columnDefs: [
        { className: 'text-center', targets: [0,1,2,3,4,5,6,7,8,9,10] },
      // {
      //   targets: [1],
      //       render: function (a, b, data, d) {
      //         let html = `<p style="text-align: left;margin-bottom: 0px;white-space: nowrap;">Username: ${data.RM_EP__USERNAME} <br> Name: ${data.RM_EP__NAME}</p>`
      //         return html;
      //       },
      // },

        {
            targets: [1], render: function (a, b, data, d){
            // html = `${moment(data.ACC_DATE, 'DD-MM-YYYY')}`
            let html = moment(data.ACC_DATE).format('DD/MM/YYYY');
            // console.log("data.ACC_DATE",data.ACC_DATE);
            // console.log("html",html);
            return html
            },
        },
        {
            targets: [6], render: function (a, b, data, d){
            let html
            if (data.DEPOSITORY_TYPE == "cdsl") {
                html = "CDSL"
            } else {
                html = "NSDL"
            }
            
            // console.log("data.ACC_DATE",data.ACC_DATE);
            // console.log("html",html);
            return html
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
            targets: [10], render: function (a, b, data, d){
                // console.log(d)
                html = `<div class="dropdown">
                            <button class="btn btn-secondary dropdown-toggle" type="button" id="dropdownMenuButton" data-toggle="dropdown" aria-haspopup="true" aria-expanded="false">
                            Action
                            </button>
                            <div class="dropdown-menu" aria-labelledby="dropdownMenuButton">
                            <a class="dropdown-item edit_modal" data-toggle="modal" href="javascript:void(0);" data-target="#edit_demat_account" data-id="${data.id}"><i class="fa fa-edit"></i> Edit</a>
                            </div>
                        </div>`
            return html
            },
        },
  ],
  } );
  t.on( 'order.dt search.dt', function () {
      t.column(0, {search:'applied', order:'applied'}).nodes().each( function (cell, i) {
          cell.innerHTML = i+1;
      } );
  } ).draw();