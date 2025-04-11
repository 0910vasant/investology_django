from django.urls import include, path

from app.views import *
from app.registration_xml_harshal import can_creation_status,can_modification_api

#"""---------------- EP Advisor app ---------"""
from app.views import load_under_customer
#"""---------------- MFU Can Creation ---------"""
from app.views import pan_validation ,send_kyc_link ,registration1 ,registration2 ,registration3 ,registration4

urlpatterns = [

    
    path('delete_customer', delete_customer_page),
    path('privacy_policy', privacy_policy_page),
    # master 
    path('get_holding_nature', get_holding_nature),
    path('get_bank_account_type', get_bank_account_type),
    path('get_investor_category', get_investor_category),
    path('get_tax_status', get_tax_status),
    path('get_bank_proof', get_bank_proof),
    path('get_gross_annual_income', get_gross_annual_income),
    path('get_source_of_wealth', get_source_of_wealth),
    path('get_kra_address_type', get_kra_address_type),
    path('get_occupation', get_occupation),
    path('get_pep_status', get_pep_status),
    path('get_country', get_country),
    path('get_state', get_state),
    path('get_city/<state>', get_city),
    path('get_pincode/<city>', get_pincode),
    path('get_identification_type', get_identification_type),
    path('get_bank', get_bank),
    path('get_enc_password', get_enc_password),
    path('scan_pan', scan_pan),

    # registration
    path('app_login', app_login),
    path('mfu_user_login_data', mfu_user_login_data),
    path('mfu_login_session', mfu_login_session),
    path('update_mfu_login_session_api', update_mfu_login_session_api),
    
    # Easy Partner Advisor app load
    path('load_under_customer', load_under_customer),

# --------------------------------------- MFU Can Creation Start -----------------------------------
    path('pan_validation', pan_validation),
    path('send_kyc_link',send_kyc_link),
    path('registration1', registration1),
    path('registration2', registration2),
    path('registration3', registration3),
    # path('registration3_1', registration3_1),
    # path('registration4', registration4),
    # path('registration5', registration5),
    path('registration4', registration4),

# --------------------------------------- MFU Can Creation End -----------------------------------
    path('manual_mfu_registration/<id>', manual_mfu_registration),
    path('manual_file_upload/<id>', manual_file_upload),
    
    # path('mfu_file_upload/<id>', mfu_file_upload),
    path('user_banks', user_banks),
    path('mfu_payeezz_registration', mfu_payeezz_registration),
    # path('mfu_payeezz_validation', mfu_payeezz_validation),

    # buy
    
    path('load_scheme_category', load_scheme_category),
    path('load_scheme_sub_category', load_scheme_sub_category),
    path('scheme_name_api', scheme_name_api),
    path('search_funds', search_funds),
    path('get_nfo_data', get_nfo_data),
    path('load_frequency', load_frequency),
    
    path('start_sip_hundred', start_sip_hundred),
    
    path('load_divident', load_divident),

    path('user_payezz', user_payezz),

    path('add_scheme_category',add_scheme_category ),
    path('get_scheme_category/<id>',get_scheme_category ),
    path('edit_scheme_category/<id>',edit_scheme_category ),
    path('load_scheme_category_table',load_scheme_category_table ),

    path('add_scheme_sub_category',add_scheme_sub_category ),
    path('get_scheme_sub_category/<id>',get_scheme_sub_category ),
    path('edit_scheme_sub_category/<id>',edit_scheme_sub_category ),
    path('load_sub_scheme_category',load_sub_scheme_category ),

    path('add_cart_api',add_cart_api ),
    path('cart_details',cart_details ),
    path('edit_cart_api/<id>',edit_cart_api),
    path('delete_cart/<id>',delete_cart),
    path('get_cart_api/<id>',get_cart_api),
    path('frequency_min_amt', frequency_min_amt),
    path('get_min_amt',get_min_amt),
    
    path('delete_success_cart',delete_success_cart),
    # path('test_registration/<id>', test_registration),
    path('can_creation_status/<int:pk>',can_creation_status,name="can_creation_status"),
    path('can_modification_api',can_modification_api, name="can_modification_api"),


    path('test_mfu_login',test_mfu_login),

    path('send_otp',send_otp),
    path('verify_otp',verify_otp),
    path('change_app_password',change_app_password),

    
    path('new_csv_download',new_csv_download),
    path('user_csv_download',user_csv_download),


    path('bulk_candata_creation',bulk_candata_creation),
    path('bulk_prn_and_bank_data',bulk_prn_and_bank_data),

    path('check_user_can_status',check_user_can_status),
    path('get_user_dashboard',get_user_dashboard),
    path('portfolio_valuation',portfolio_valuation),
    
    path('bulk_candata_bank_edit',bulk_candata_bank_edit),

    # rushikesh
    path('load_belongs_to',load_belongs_to),
    path('load_nominee_relation',load_nominee_relation),
    


]

    # path('test_registration_xml', test_registration_xml),

    # path('change_countrymaster', change_countrymaster),

    

