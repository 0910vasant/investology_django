$.ajax({
    url: "/ep_dashboard_api",
    success: function (data) {
        // console.log('data', data);
        $("#pending_amt").html(data.pending_amt);
        $("#customer_count").html(data.customer_count);
        $("#total_commission").html(data.total_commission);
        $("#total_business").html(data.total_business);
        $("#received_amount").html(data.received_amount);
    }
    
});

