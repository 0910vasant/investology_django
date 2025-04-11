
$(document).ready(function () {
// Start Country , State , City ,Pincodes Sections
    l_c = "all"
    load_country(l_c)
// End Country , State , City ,Pincodes Sections

// Start Account Section
    load_investor_category()
    load_tax_status()
    load_holding_nature()
    load_occupation()
// End Account Section

// Start Bank Details Sections
    load_bank_name()
    load_bank_acc_type()
    load_bank_proof()
// End Bank Details Sections

//  Start KYC Sections
    load_gross_annual_income()
    load_source_of_wealth()
    load_kra_add_type()
    load_pep_status()
//  End KYC Sections

//  Start FATCA Sections
    id_type = "all"
    load_identification_type(id_type)
//  End FATCA Sections

});

// Start Country , State , City ,Pincodes Sections
function trigger_select() {
    $('.select2').select2({
        width:"100%"
    });
}

function load_country(l_c){
    country = [`<option value="" selected disabled>Select Country</option>`]
    $.ajax({
        url: "/get_country",
        success: function (response) {
            $.each(response, function (i, v){
                country.push(`<option value="${v.id}">${v.NAME}</option>`)
            });
            if (l_c == "all") {
                $(".country").html(country.join(""));
            } else {
                $(".country").last().html(country.join(""));
            }
            
        }
    });
}
$("body").on('click','.blank_state', function () {
    toastr.info("You Have to Select Country First")
});
$("body").on('click','.blank_city', function () {
    toastr.info("You Have to Select State First")
});
$("body").on('click','.blank_pincode', function () {
    toastr.info("You Have to Select City First")
});

$("#cust_country").change(function () {
    state = [`<option value="" selected disabled>Select State</option>`]
    $.ajax({
        url: "/get_state",
        success: function (response) {
            $(".form-group").removeClass("blank_state")
            // console.log("response",response);
            $.each(response, function (i, v){
                state.push(`<option value="${v.id}">${v.NAME}</option>`)
            });
            $(".state").html(state.join(""));
        }
    });
});

$("#cust_state").change(function () {
    // id = $(this).val()
    id = 7
    console.log("id",id);
    city = [`<option value="" selected disabled>Select City</option>`]
    $.ajax({
        url: `/get_city/${id}`,
        success: function (response) {
            $(".form-group").removeClass("blank_city")
            // console.log("response",response);
            $.each(response, function (i, v){
                city.push(`<option value="${v.CITY}">${v.CITY}</option>`)
            });
            $(".city").html(city.join(""));
        }
    });
});

$("#cust_city").change(function () {
    id = $(this).val()
    console.log("id",id);
    city = [`<option value="" selected disabled>Select Pincode</option>`]
    $.ajax({
        url: `/get_pincode/${id}`,
        success: function (response) {
            $(".form-group").removeClass("blank_pincode")
            // console.log("response",response);
            $.each(response, function (i, v){
                city.push(`<option value="${v.id}">${v.PINCODE}</option>`)
            });
            $(".pincode").html(city.join(""));
        }
    });
});

// End Country , State , City ,Pincodes Sections

// Start Account Section
function load_investor_category(){
    investor_category = [`<option value="" selected disabled>Select Investor Category</option>`]
    $.ajax({
        url: "/get_investor_category",
        success: function (response) {
            $.each(response, function (i, v){
                investor_category.push(`<option value="${v.id}">${v.NAME}</option>`)
            });
            $(".investor_category").html(investor_category.join(""));
        }
    });
}

function load_tax_status(){
    tax_status = [`<option value="" selected disabled>Select Tax Status</option>`]
    $.ajax({
        url: "/get_tax_status",
        success: function (response) {
            $.each(response, function (i, v){
                tax_status.push(`<option value="${v.id}">${v.TAX_STATUS}</option>`)
            });
            $(".tax_status").html(tax_status.join(""));
        }
    });
}

function load_holding_nature(){
    holding_nature = [`<option value="" selected disabled>Select Holding Nature</option>`]
    $.ajax({
        url: "/get_holding_nature",
        success: function (response) {
            $.each(response, function (i, v){
                holding_nature.push(`<option value="${v.id}">${v.HOLDING_TYPE}</option>`)
            });
            $(".holding_nature").html(holding_nature.join(""));
        }
    });
}

function load_occupation(){
    occupation = [`<option value="" selected disabled>Select Occupation Code</option>`]
    $.ajax({
        url: "/get_occupation",
        success: function (response) {
            
            $.each(response, function (i, v){
                occupation.push(`<option value="${v.id}">${v.NAME}</option>`)
            });
            $(".occupation_code").html(occupation.join(""));
        }
    });
}
// End Account Section

// Start Bank Details Load

function load_bank_name(){
    bank_name = [`<option value="" selected disabled>Select Bank Name</option>`]
    $.ajax({
        url: "/get_bank",
        success: function (response) {
            $.each(response, function (i, v){
                bank_name.push(`<option value="${v.id}">${v.NAME}</option>`)
            });
            $(".bank_name").html(bank_name.join(""));
            
        }
    });
}
function load_bank_acc_type(){
    bank_acc_type = [`<option value="" selected disabled>Select Bank Account Type</option>`]
    $.ajax({
        url: "/get_bank_account_type",
        success: function (response) {
            $.each(response, function (i, v){
                bank_acc_type.push(`<option value="${v.id}">${v.BANK_ACCOUNT_TYPE}</option>`)
            });
            $(".bank_acc_type").html(bank_acc_type.join(""));
        }
    });
}

function load_bank_proof(){
    bank_proof = [`<option value="" selected disabled>Select Bank Proof Type</option>`]
    $.ajax({
        url: "/get_bank_proof",
        success: function (response) {
            // console.log("ressdsdproof",response);
            $.each(response, function (i, v){
                bank_proof.push(`<option value="${v.id}">${v.NAME}</option>`)
            });
            $(".bank_proof").html(bank_proof.join(""));
        }
    });
}


// End Bank Details Load

// Start KYC Sections

function load_gross_annual_income() {
    gross_annual_income = [`<option value="" selected disabled>Select Gross Annual Income</option>`]
    $.ajax({
        url: "/get_gross_annual_income",
        success: function (response) {
            // console.log("response",response);
            $.each(response, function (i, v){
                gross_annual_income.push(`<option value="${v.id}">${v.NAME}</option>`)
            });
            $(".gross_annual_income").html(gross_annual_income.join(""));
        }
    });
}

function load_source_of_wealth() {
    source_of_wealth = [`<option value="" selected disabled>Select Source Of Wealth</option>`]
    $.ajax({
        url: "/get_source_of_wealth",
        success: function (response) {
            $.each(response, function (i, v){
                source_of_wealth.push(`<option value="${v.id}">${v.NAME}</option>`)
            });
            $(".source_of_wealth").html(source_of_wealth.join(""));
        }
    });
}

function load_kra_add_type() {
    kra_address_type = [`<option value="" selected disabled>Select Types Of Address Given at KRA</option>`]
    $.ajax({
        url: "/get_kra_address_type",
        success: function (response) {
            $.each(response, function (i, v){
                kra_address_type.push(`<option value="${v.id}">${v.NAME}</option>`)
            });
            $(".kra_address_type").html(kra_address_type.join(""));
        }
    });
}


function load_pep_status() {
    pep_status = [`<option value="" selected disabled>Select PEP Status</option>`]
    $.ajax({
        url: "/get_pep_status",
        success: function (response) {
            // console.log("response",response);
            $.each(response, function (i, v){
                pep_status.push(`<option value="${v.id}">${v.NAME}</option>`)
            });
            $(".pep_status").html(pep_status.join(""));
        }
    });
}
// End KYC Sections

//  Start FATCA Sections
function load_identification_type(id_type) {
    identification_type = [`<option value="" selected disabled>Select Identification Type</option>`]
    $.ajax({
        url: "/get_identification_type",
        success: function (response) {
            // console.log("response",response);
            $.each(response, function (i, v){
                identification_type.push(`<option value="${v.id}">${v.NAME}</option>`)
            });
            if (id_type == "all") {
                $(".identification_type").html(identification_type.join(""));
            } else {
                $(".identification_type").last().html(identification_type.join(""));
            }
            
        }
    });
}
//  End FATCA Sections





