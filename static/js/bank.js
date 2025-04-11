bank_name = [`<option value="" selected disabled>Select Bank Name</option>`]
console.log("load bank");
$.ajax({
    url: "/get_bank",
    async:false,
    success: function (response) {
        $.each(response, function (i, v){
            bank_name.push(`<option value="${v.id}">${v.NAME}</option>`)
        });
        $(".load_bank").html(bank_name.join(""));
        
    }
});



