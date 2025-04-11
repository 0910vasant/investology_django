from django.urls import path
from admin_panel.views import *
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin_login', admin_login),
    path('admin_dashboard', admin_dashboard),

    path('customer_management', customer_management),
    path('load_admin_customer', load_admin_customer),
    path('customer_detail/<id>', customer_detail),
    path('can_error', can_error),
    path('load_can_error_data', load_can_error_data),
    path('get_canerror_req_res/<id>', get_canerror_req_res),
    
    # Scheme Details
    path('buy_scheme', buy_scheme),
    path('scheme_details/<id>', scheme_details),
    # path('add_scheme_excel', add_scheme_excel),
    path('add_bulk_scheme', add_bulk_scheme),
    path('load_scheme', load_scheme),

        # Threshold Details
    path('buy_threshold', buy_threshold),
    path('threshold_details/<id>', threshold_details),
    path('add_bulk_threshold', add_bulk_threshold),
    path('load_threshold', load_threshold),
    

    path('add_bulk_cams_kfintech_scheme', add_bulk_cams_kfintech_scheme),
    path('load_cams_kfintech_schemes', load_cams_kfintech_schemes),
    path('cams_kfintech_scheme', cams_kfintech_scheme),

    path('add_bulk_cams_kfintech_mailback', add_bulk_cams_kfintech_mailback),
    path('mailback_transaction', mailback_transaction),
    path('load_mailback_transaction', load_mailback_transaction),
    path('get_folio_investment/<id>', get_folio_investment),

    path('cams_kfintech_scheme_nav', cams_kfintech_scheme_nav),
    path('add_bulk_cams_kfintech_nav', add_bulk_cams_kfintech_nav),
    path('load_nav', load_nav),
    
    




    # Threshold Details
    path('buy_list', buy_list),
    path('buy_details/<id>', buy_detail),
    path('load_buy_list', load_buy_list),
    
    path('sales_list', sales_list),
    path('sales_details/<id>', sales_detail),
    path('load_sales_list', load_sales_list),

    path('scheme_category', scheme_category),
    path('scheme_sub_category', scheme_sub_category),
    path('amc', amc),


    
    path('remove_extra_space', remove_extra_space),

    path('check_amc', check_amc),
    path('add_amc_api',add_amc_api ),
    path('get_amc/<id>',get_amc ),
    path('edit_amc/<id>',edit_amc ),
    path('load_amc', load_amc),
    path('load_amc_table', load_amc_table),
    # path('test_api', test_api),


    path('valuation_reports', valuation_reports),
    path('consolidated_valuation_report_page', consolidated_valuation_report_page),
    path('detailized_folio', detailized_folio_view),
    # path('test_rushikesh', test_rushikesh),
    path('test_query',test_query),

    path('get_user_mobile_no/<id>', get_user_mobile_no),
    path('edit_user_mobile_no/<id>', edit_user_mobile_no),

    path('make_payment', make_payment),
    path('test_payu', test_payu),
    path('payment_response', payment_response),
    
    


    
    # path('customer_management', customer_management),
]



