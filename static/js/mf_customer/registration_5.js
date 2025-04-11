$("#registration5_form").submit(function (e) { 
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
        url: "/registration5",
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

$(".source_of_wealth").change(function () { 
    text = $(this).find(":selected").text()
    if (text == "Others") {
        // a = $(this).parent().siblings(".other_country_div").show(100)
        a = $(this).parents(".col-md-4").siblings(".osow_div").show(300)
    }
    else{
        a = $(this).parents(".col-md-4").siblings(".osow_div").hide(300)
    }
});

$(".kyc_occupation").change(function () { 
    text = $(this).find(":selected").text()
    if (text == "Others") {
        // a = $(this).parent().siblings(".other_country_div").show(100)
        a = $(this).parents(".col-md-4").siblings(".other_occ_div").show(300)
    }
    else{
        a = $(this).parents(".col-md-4").siblings(".other_occ_div").hide(300)
    }
});

$("#income_type").change(function () { 
    a = $(this).find(':selected').data("id")
    $(".income-type").hide()
    $(`.${a}`).show()
});