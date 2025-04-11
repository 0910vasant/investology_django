$("#registration3_1_form").submit(function (e) { 
    e.preventDefault();
    select_attr = $(this)
    select_id = this.id
    data = new FormData(this)
    data.append("user_id", $("#user_id").val());

    for(let[key,value] of data){
            console.log("from_data",`${key}`,`${value}`);
    }

    $.ajax({
        type: "post",
        url: "/registration3_1",
        data: data,
        processData: false,
        contentType: false,
        enctype: 'multipart/form-data',
        success: function (response) {
            toastr.success(response)
            unlock_cust(select_attr,select_id)
            // $("#user_id").val(response.user_id)
        },
        error: function (response) {
            // console.log("response",response);
            toastr.error(response.responseJSON.error)
            console.log("error");
        },
    });

    
});