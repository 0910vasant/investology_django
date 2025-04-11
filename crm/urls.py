from django.urls import path
from crm.views import *
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('demo_login', demo_login),
    path('', home),


    path('login', Login.as_view()),
    path('logout', Logout),
    
    path('create_user_login', Create_user_login.as_view()),
    path('change_password', Change_password.as_view()),
    path('forgot_password', Forgot_password.as_view()),
    path('profile', profile),

    path('dashboard', Index.as_view()),
    path('scheme_master', Scheme_Master.as_view()),
    path('client_family', Client_Family.as_view()),
    path('add_client_family', Add_Client_Family.as_view()),

    path('branch_location_master', branch_location_master_page),
    path('add_branch_location', add_branch_location.as_view()),
    path('edit_branch_location/<id>', edit_branch_location.as_view()),
    path('load_branch_location', load_branch_location),

    path('insurance_master', insurance_master_page),
    path('add_bulk_insurance_excel', AddBulkInsuranceExcel.as_view()),
    path('add_insurance_master_bulk', add_im_bulk),
    path('load_edit_im/<id>', load_edit_im),
    path('edit_im/<id>', edit_im),
    path('button_add_im_data', button_add_im_data),
    path('load_im_data', load_im_data),
    path('get_insurance/<id>', get_insurance),
    

    # path('load_scheme', mf_master_page),
    path('mf_master', mf_master_page),
    path('add_bulk_mf_excel', AddBulk_mfm_Excel.as_view()),
    path('add_mf_master_bulk', Add_mfm_Bulk),
    path('load_edit_mfm/<id>', load_edit_mfm),
    path('edit_mfm/<id>', edit_mfm),
    path('load_mfm_data', load_mfm_data),


    path('insurance_type_master', insurance_type_master_page),
    path('add_insurance_name', add_insurance_name.as_view()),
    path('edit_insurance_name/<id>', edit_insurance_name.as_view()),
    path('load_insurance_name', load_insurance_name),


    path('branch_manager_master', Branch_Manager_Page.as_view()),
    path('add_branch_manager', Add_Branch_Manager.as_view()),
    path('edit_branch_manager/<id>', Edit_Branch_Manager.as_view()),
    path('load_bm_data', load_bm_data),
    

    path('relationship_manager_master', Relationship_Manager_Page.as_view()),
    path('add_relationship_manager', Add_Relationship_Manager.as_view()),
    path('edit_relationship_manager/<id>', Edit_Relationship_Manager.as_view()),
    path('load_rm_data', load_rm_data),

    path('bo',bo_page),
    path('add_bo',add_bo_page),
    path('edit_bo/<id>',edit_bo_page),
    path('add_bo_api',add_bo_api),
    path('edit_bo_api/<id>',edit_bo_api),
    path('delete_bo_api/<id>',delete_bo_api),
    path('load_bo_data',load_bo_data_api),

    path('easy_partner_master', EP_Page.as_view()),
    path('add_ep', Add_Easy_Partner.as_view()),
    path('edit_ep/<id>', Edit_Easy_Partner.as_view()),
    
    path('get_easy_partner/<id>', get_easy_partner),
    path('load_ep_data', load_ep_data),
    path('get_user_ep_code/<id>', get_user_ep_code),
    path('edit_user_ep_code/<id>', edit_user_ep_code),
    
    

    

    path('super_partner', Super_Partner.as_view()),
    path('add_super_partner', Add_Super_Partner.as_view()),

    path('bm_brokerage', BM_Brokerage_Page.as_view()),
    path('add_bm_brokerage', Add_BM_Brokerage.as_view()),
    path('edit_bm_brokerage/<id>', Edit_BM_Brokerage.as_view()),
    path('load_bm_brokerage_data', load_bm_brokerage_data),

    path('rm_brokerage', RM_Brokerage_Page.as_view()),
    path('add_rm_brokerage', Add_RM_Brokerage.as_view()),
    path('edit_rm_brokerage/<id>', Edit_RM_Brokerage.as_view()),
    path('load_rm_brokerage_data', load_rm_brokerage_data),


    path('sp_brokerage', SP_Brokerage.as_view()),
    path('add_sp_brokerage', Add_SP_Brokerage.as_view()),

    path('easy_partner_brokerage', sub_broker_brokerage_page.as_view()),
    path('add_easy_partner_brokerage', Add_SUB_broker_Brokerage.as_view()),
    path('edit_easy_partner_brokerage/<id>', Edit_SUB_broker_Brokerage.as_view()),
    path('load_sub_brokerage_data', load_sub_brokerage_data),

    path('bse_sm_user', BSE_SM_User.as_view()),
    path('add_bse_sm_user', Add_BSE_SM_User.as_view()),

    path('mf_manually', MF_Manually.as_view()),
    path('add_mf_manually', Add_MF_Manually.as_view()),

    path('nav_view', NAV_View.as_view()),
    path('add_nav_view', Add_NAV_View.as_view()),
    path('edit_nav_view', Edit_NAV_View.as_view()),

    path('transaction_view', Transaction_View.as_view()),
    path('add_transaction_view', Add_Transaction_View.as_view()),
    path('edit_transaction_view', Edit_Transaction_View.as_view()),

    path('mf_valuation_report', MF_Valuation_Report.as_view()),

    path('account_statement_report', ACC_Statement_Report.as_view()),

    path('portfolio_composition', Portfolio_Composition.as_view()),

    path('capital_gain_report', Capital_Gain_Report.as_view()),
    path('capital_gain_report_page', Capital_Gain_Report_Page.as_view()),

    path('dividend_income_statement', Dividend_Income_Statement.as_view()),

    path('transaction_report', Transaction_Report.as_view()),

    path('sip_report', SIP_Report.as_view()),

    path('top_n_client', Top_N_Client.as_view()),

    path('scheme_comparison', Scheme_Comparison.as_view()),
    path('scheme_comparison_page', Scheme_Comparison_Page.as_view()),

    path('scheme_factsheet', Scheme_Factsheet.as_view()),
    path('scheme_factsheet_page', Scheme_Factsheet_Page.as_view()),

    path('arn_brokerage_report', ARN_Brokerage_Report.as_view()),
    path('arn_brokerage_report_page', ARN_Brokerage_Report_Page.as_view()),

    path('arn_clientwise_brokerage_report', ARN_Clientwise_Brokerage_Report.as_view()),
    path('arn_clientwise_brokerage_report_page', ARN_Clientwise_Brokerage_Report_Page.as_view()),

    path('arn_aum_report', ARN_AUM_Report.as_view()),
    path('arn_aum_typewise_report_page', ARN_AUM_Typewise_Report_Page.as_view()),
    path('arn_aum_schemewise_report_page', ARN_AUM_Schemewise_Report_Page.as_view()),
    path('arm_aum_clientwise_report_page', ARN_AUM_Clientwise_Report_Page.as_view()),

    path('add_mf_customer', add_mf_customer),

    # path('add_insurance_customer_master', add_insurance_customer_master),
    path('add_insurance_and_customer', add_insurance_and_customer),

    path('customer', customer_page),
    path('load_customer', load_customer),
    path('add_customer', Add_customer.as_view()),
    path('edit_customer/<id>', Edit_customer.as_view()),
    path('load_select_customer', load_select_customer),
    path('transfer_customer', transfer_customer),

    


    path('buy_insurance', insurance_page),
    path('insurance_alert', insurance_alert_page),
    path('add_insurance_alert', add_insurance_alert.as_view()),
    path('edit_insurance_alert/<id>', edit_insurance_alert.as_view()),
    path('load_insurance', load_insurance),
    path('load_new_insurance', load_new_insurance),
    path('get_new_insurance/<id>', get_new_insurance),
    path('edit_new_insurance_page/<id>', edit_new_insurance_page),
    path('update_insurance', update_insurance),
    path('add_insurance_and_customer', add_insurance_and_customer),

    path('policy_broker_master', policy_broker_page),
    path('add_policy_broker', add_policy_broker.as_view()),
    path('edit_policy_broker/<id>', edit_policy_broker.as_view()),
    path('load_policy_broker', load_policy_broker),

    path('load_insurance_alert', load_alert_insurance),
    
    path('delete_insurance_alert/<id>', delete_insurance_alert),


    path('attendance', attendance_page),
    path('load_attendance', load_attendance),
    path('punch_in', punch_in),
    path('punch_out', punch_out),
    path('add_attendance', add_attendace.as_view()),
    path('edit_attendance/<id>', edit_attendace.as_view()),
    path('delete_attendance/<id>',delete_attendance),
    

    path('leads', leads_page),
    path('load_leads', load_leads),
    path('load_lead_cust', load_lead_cust),
    path('add_leads', Add_leads.as_view()),
    path('edit_leads/<id>', Edit_leads.as_view()),

    path('followup', followup_page),
    path('load_followups', load_followups),
    path('add_followup', add_followup.as_view()),
    path('edit_followup/<id>', edit_followup.as_view()),
    path('delete_followup', delete_followup),

    path('meeting', meetings_page),
    path('load_meetings', load_meetings),
    path('add_meeting', add_meeting),
    path('edit_meeting', edit_meeting),
    path('delete_meeting', delete_meeting),
    path('get_meeting/<id>', get_meeting),
    path('filter_customer', filter_customer),
    # path('meetings_customer1', meetings_customer1),

    
    path('notification', notification_page),
    path('send_notification', send_notification),
    path('load_notifications', load_notifications),
    path('get_notification_users/<id>', get_notification_users),

# ----------------- Calculator Section Start -------------------------#
    path('sip_calculator', sip_calculator_page),
    path('sip_calc', sip_calculator),

    path('sip_lumpsum_calculator', sip_lumpsum_calculator_page),
    path('sip_lumpsum_calc', sip_lumpsum_calculator),

    
    path('swp_calculator', swp_calculator_page),
    path('swp_calc', swp_calculator),

    path('step_up_sip_calc', step_up_sip_calculator),
    path('child_education_plan_calc', child_education_plan_calculator),

    
# ----------------- Calculator Section End -------------------------#

#---------------------Load User Api----------------------------------#

    path('load_user_type', load_user_type),

# ----------------- Buy FD, PMS -------------------------#
    path('buy_fd',buy_fd_page),
    path('add_buy_fd',add_buy_fd),
    path('edit_buy_fd/<id>',edit_buy_fd),
    path('delete_buy_fd/<id>',delete_buy_fd),
    path('get_buy_fd/<id>',get_buy_fd),
    path('load_buy_fd',load_buy_fd),

# ----------------- Buy MF-------------------------#
    
    path("buy_mf",buy_mf_page),
    path("add_buy_mf",add_buy_mf),
    path("edit_buy_mf/<id>",edit_buy_mf),
    path("delete_buy_mf/<id>",delete_buy_mf),
    path("load_buy_mf",load_buy_mf),
    path("get_buy_mf/<id>",get_buy_mf),


    
    # path('buy_pms',buy_pms_page),
    
    # path('test_crontab', test_crontab),


    path('permission',PermissionManagement.as_view()),
    path('add_role_permission',add_role_permission),
    path('edit_role_permission/<id>',edit_role_permission),
    path('delete_role_permission/<id>',delete_role_permission),
    path('get_role_permission/<id>',get_role_permission),
    path('load_role_permission',load_role_permission),

# ----------------- Payment start-------------------------#
    path('payment',payment),
    path('payment_table',payment_table),
    path('all_ep',all_ep),
    path('add_pay_out',add_pay_out),
    path('edit_pay_out',edit_pay_out),
    path('delete_pay_out/<id>',delete_pay_out),
    path('get_ep_pay_out/<id>',get_ep_pay_out),
    path('get_pay_out/<id>',get_pay_out),
    path('payout_history/<id>',payout_history),

# ----------------- Payment end -------------------------#
    path('unauthorized',unauthorized),
    # path('add_branch_manager', add_branch_manager),

    # path('scheme_comparison', Scheme_Comparison.as_view()),
    # path('comparison_page', Comparison_Page.as_view()),
    path('ep_dashboard_api',ep_dashboard_api),
    path('admin_list',admin_list),
    
    path('create_admin',create_admin),
    path('get_admin/<id>',get_admin),
    path('edit_admin/<id>',edit_admin),
    

    path('load_admin',load_admin),

    #demat Account
    path('demat_account',demat_account_page),
    path('load_demat_account',load_demat_account),
    path('add_demat_account',add_demat_account),
    path('get_demat_account/<id>',get_demat_account),
    path('edit_demat_account/<id>',edit_demat_account),


    path('daily_buy_reports',daily_buy_reports),
    path('daily_reports_api',daily_reports_api),
    
    
]
