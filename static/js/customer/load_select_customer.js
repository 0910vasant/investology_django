$.ajax({
    url: "/load_select_customer",
    success: function (response) {
        customer = [`<option value="" disabled selected>Please Select Customer</option>`]
        $.each(response,function(i,v){
            customer.push(`<option value="${v.id}">${v.C_NAME} || ${v.MOB_NO}</option>`)
        });
        $(".select_customer").html(customer.join(""))
    }
});