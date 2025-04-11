var today = new Date();
        
// Format it as YYYY-MM-DD
var year = today.getFullYear();
var month = String(today.getMonth() + 1).padStart(2, '0'); // Months are 0-indexed
var day = String(today.getDate()).padStart(2, '0');

var formattedDate = year + '-' + month + '-' + day;

// Set the value of the date input
$('#to_date').val(formattedDate);

$("#valuation_report_form").on("submit", function (e) {
    e.preventDefault();
    console.log("ehsdifuisda");
    from_date   = $("#from_date").val()
    to_date     = $("#to_date").val()
    client_pan  = $("#client_pan").val()
    if (client_pan == null) {
        toastr.error("Please Select Client");
        return false
    }
    url = `https://app.easyinvestology.com/consolidated_valuation_report_page?from_date=${from_date}&to_date=${to_date}&client_pan=${client_pan}`
    window.open(url, '_blank');
    // consolidated_valuation_report_page?from_date=1990-01-01&to_date=2024-10-16&client_pan=CKFPP0393G&submit=
});