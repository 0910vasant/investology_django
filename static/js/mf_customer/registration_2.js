$("#registration2_form").submit(function (e) { 
    e.preventDefault();
    select_attr = $(this)
    select_id = this.id
    data = $(this).serializeArray();

    data.push({name: 'user_id', value: $("#user_id").val()})
    user_id

    $.ajax({
        type: "post",
        url: "/registration2",
        data: data,
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

$("#holding_nature").change(function () { 
    text = $(this).find(':selected').text()
    //aos_div =  anyone_or_survivor_div
    if (text != "Single") {
        $(".aos_div").show(500)
    } else {
        $(".aos_div").hide(500)
    }
    // $(".secondary_div").hide()
    // $(`#${a}`).show()
});
