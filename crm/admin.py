from django.contrib import admin
from .models import *

from django.apps import apps

# # crm_models = apps.get_app_config('crm').get_models()
# # for model in crm_models:
# #     try:
# #         admin.site.register(model)
# #     except admin.sites.AlreadyRegistered:
# #         pass


# admin.site.register(Branch_Manager)
# # admin.site.register(Customer_types)
# admin.site.register(Relationship_Manager)
# admin.site.register(Easy_Partner)
# # admin.site.register(Branch_location_master)
# # admin.site.register(Easy_Partner)
# # admin.site.register(Insurance_type_master)
# # admin.site.register(Customer)
# # admin.site.register(Insurance)
# # admin.site.register(Update_insurance_alert)
# # admin.site.register(User)

# @admin.register(User)
# class UserAdmin(admin.ModelAdmin):
#     list_display = ("id","USER_ID","USER_TYPE","NAME","USERNAME","PASSWORD")

# # admin.site.register(LoginLogs)
# # admin.site.register(Attendance_user)
# # admin.site.register(Leads)
# # admin.site.register(Followups)
# # admin.site.register(Meetings)
# admin.site.register(Back_Office)



# # Register your models here.
@admin.register(User)
class UserAdmin(admin.ModelAdmin):
  list_display = ("id","USER_ID","USER_TYPE","OWNER","EMPLOYEE_CODE","EMPLOYEE_NUMBER","NAME","USERNAME","PASSWORD")
  list_filter = ["id","USER_ID","USER_TYPE","OWNER","EMPLOYEE_CODE","EMPLOYEE_NUMBER","NAME","USERNAME","PASSWORD"]

@admin.register(LoginLogs)
class LoginLogsAdmin(admin.ModelAdmin):
  list_display = ("id","USER_ID","USER_TYPE","LOGIN_DATETIME","LOGOUT_DATETIME","LOGIN_SESSION","IP_ADDRESS","LOGIN_STATUS")
  list_filter = ["id","USER_ID","USER_TYPE","LOGIN_DATETIME","LOGOUT_DATETIME","LOGIN_SESSION","IP_ADDRESS","LOGIN_STATUS"]

@admin.register(Customer_types)
class Customer_typesAdmin(admin.ModelAdmin):
  list_display = ("id","TYPE",)
  list_filter = ["id","TYPE"]

@admin.register(Branch_location_master)
class Branch_location_masterAdmin(admin.ModelAdmin):
  list_display = ("id","NAME",)
  list_filter = ["id","NAME"]

@admin.register(Branch_Manager)
class Branch_ManagerAdmin(admin.ModelAdmin):
  list_display = ("id","CODE","NAME","ADD1","ADD2","DOB","PHONE","MOB_NO","EMAIL","BANK_NAME","ACC_NO","IFSC_CODE","BRANCH_LOC","CREATE_LOGIN","CREATED_BY","MODIFIED_BY")
  list_filter = ["id","CODE","NAME","ADD1","ADD2","DOB","PHONE","MOB_NO","EMAIL","BANK_NAME","ACC_NO","IFSC_CODE","BRANCH_LOC","CREATE_LOGIN","CREATED_BY","MODIFIED_BY"]

@admin.register(Relationship_Manager)
class Relationship_ManagerAdmin(admin.ModelAdmin):
  list_display = ("id","BRANCH","CODE","NAME","ADD1","ADD2","DOB","PHONE","MOB_NO","EMAIL","BANK_NAME","ACC_NO","IFSC_CODE","PAN_NO","CREATE_LOGIN")
  list_filter = ["id","BRANCH","CODE","NAME","ADD1","ADD2","DOB","PHONE","MOB_NO","EMAIL","BANK_NAME","ACC_NO","IFSC_CODE","PAN_NO","CREATE_LOGIN"]

@admin.register(Easy_Partner)
class Easy_PartnerAdmin(admin.ModelAdmin):
  list_display = ("id","MF_C_P","RM","CODE","NAME","ADD1","ADD2","DOB","PHONE","MOB_NO","EMAIL","BANK_NAME","ACC_NO","IFSC_CODE","PAN_NO","CREATE_LOGIN")
  list_filter = ["id","MF_C_P","RM","CODE","NAME","ADD1","ADD2","DOB","PHONE","MOB_NO","EMAIL","BANK_NAME","ACC_NO","IFSC_CODE","PAN_NO","CREATE_LOGIN"]

@admin.register(BM_Brokerage)
class BM_BrokerageAdmin(admin.ModelAdmin):
  list_display = ("id","DOB","BM_NAME","AMC_NAME","TRAIL","CREATED_BY","MODIFIED_BY")
  list_filter = ["id","DOB","BM_NAME","AMC_NAME","TRAIL","CREATED_BY","MODIFIED_BY"]

@admin.register(RM_Brokerage)
class RM_BrokerageAdmin(admin.ModelAdmin):
  list_display = ("id","DOB","RM_NAME","AMC_NAME","TRAIL","CREATED_BY","MODIFIED_BY")
  list_filter = ["id","DOB","RM_NAME","AMC_NAME","TRAIL","CREATED_BY","MODIFIED_BY"]

@admin.register(Easy_Partner_Brokerage)
class Easy_Partner_BrokerageAdmin(admin.ModelAdmin):
  list_display = ("id","EFFECTIVE_DATE","PARTNER_NAME","AMC_NAME","TRAIL","ADD_INCENTIVE","TYPE","NOTE","CREATED_BY","MODIFIED_BY")
  list_filter = ["id","EFFECTIVE_DATE","PARTNER_NAME","AMC_NAME","TRAIL","ADD_INCENTIVE","TYPE","NOTE","CREATED_BY","MODIFIED_BY"]

@admin.register(Insurance_type_master)
class Insurance_type_masterAdmin(admin.ModelAdmin):
  list_display = ("id","NAME")
  list_filter = ["id","NAME"]

@admin.register(Customer)
class CustomerAdmin(admin.ModelAdmin):
  list_display = ("id","RM_EP","RM","EP","BM","IS_DELETED","TYPE","PAN_NO","C_NAME","CUST_DOB","MOB_NO","CUSTOMER_TYPES","CREATED_BY","MODIFIED_BY")
  list_filter = ["id","RM_EP","RM","EP","TYPE","PAN_NO","C_NAME","CUST_DOB","MOB_NO","CUSTOMER_TYPES","CREATED_BY","MODIFIED_BY"]

@admin.register(Insurance)
class InsuranceAdmin(admin.ModelAdmin):
  list_display = ("id","CUSTOMER","TYPE_INSURANCE","INSURANCE_NAME","INSURANCE_PERIOD","START_DATE","RENEWAL_DATE","PPT","PT","PB","NET_AMT","GROSS_AMT","COMMISSION","COMMISSION_AMT","CREATED_BY","MODIFIED_BY")
  list_filter = ["id","CUSTOMER","TYPE_INSURANCE","INSURANCE_NAME","INSURANCE_PERIOD","START_DATE","RENEWAL_DATE","PPT","PT","PB","NET_AMT","GROSS_AMT","COMMISSION","COMMISSION_AMT","CREATED_BY","MODIFIED_BY"]

@admin.register(Update_insurance_alert)
class Update_insurance_alertAdmin(admin.ModelAdmin):
  list_display = ("id","INSURACE","INSURANCE_PERIOD","START_DATE","RENEWAL_DATE")
  list_filter = ["id","INSURACE","INSURANCE_PERIOD","START_DATE","RENEWAL_DATE"]

@admin.register(Attendance_user)
class Attendance_userAdmin(admin.ModelAdmin):
  list_display = ("id","USER","DATE","PUNCH_IN","PUNCH_OUT","REMARK","CREATED_BY","MODIFIED_BY")
  list_filter = ["id","USER","DATE","PUNCH_IN","PUNCH_OUT","REMARK","CREATED_BY","MODIFIED_BY"]

@admin.register(Leads)
class LeadsAdmin(admin.ModelAdmin):
  list_display = ("id","RM_EP","PAN_NO","LEAD_TYPE","C_NAME","CUST_DOB","MOB_NO","EMAIL","CREATED_BY","MODIFIED_BY")
  list_filter = ["id","RM_EP","PAN_NO","LEAD_TYPE","C_NAME","CUST_DOB","MOB_NO","EMAIL","CREATED_BY","MODIFIED_BY"]

@admin.register(Followups)
class FollowupsAdmin(admin.ModelAdmin):
  list_display = ("id","RM_EP","TYPE","LEADS","DATE","TIME","REMARK","CREATED_BY","MODIFIED_BY")
  list_filter = ["id","RM_EP","TYPE","LEADS","DATE","TIME","REMARK","CREATED_BY","MODIFIED_BY"]

@admin.register(Meetings)
class MeetingsAdmin(admin.ModelAdmin):
  list_display = ("id","RM_EP","LEADS","I_CUST","TYPE","DATE","TIME","REMARK","USER_TYPE","CREATED_BY","MODIFIED_BY")
  list_filter = ["id","RM_EP","LEADS","I_CUST","TYPE","DATE","TIME","REMARK","USER_TYPE","CREATED_BY","MODIFIED_BY"]

@admin.register(Notifications)
class NotificationsAdmin(admin.ModelAdmin):
  list_display = ("id","CUSTOMER_IDS","TYPE","TITLE","DESCRIPTION","USER_TYPE","USER","CREATED_BY","MODIFIED_BY")
  list_filter = ["id","CUSTOMER_IDS","TYPE","TITLE","DESCRIPTION","USER_TYPE","USER","CREATED_BY","MODIFIED_BY"]

@admin.register(Policy_broker_master)
class Policy_broker_masterAdmin(admin.ModelAdmin):
  list_display = ("id","NAME","CREATED_BY","MODIFIED_BY")
  list_filter = ["id","NAME","CREATED_BY","MODIFIED_BY"]

@admin.register(Modules)
class ModulesAdmin(admin.ModelAdmin):
  list_display = ("id","NAME","URL","CREATED_DATE","UPDATED_DATE")
  list_filter = ["id","NAME","URL","CREATED_DATE","UPDATED_DATE"]

@admin.register(Buy_FD)
class Buy_FDAdmin(admin.ModelAdmin):
  list_display = ("id","EP_RM","BUY_TYPE","CUSTOMER","START_DATE","END_DATE","COMPANY_NAME","TENURE","INTEREST_RATE","AMOUNT","BROKERAGE_PERCENTAGE","BROKERAGE_AMOUNT","CREATED_BY","MODIFIED_BY")
  list_filter = ["id","EP_RM","BUY_TYPE","CUSTOMER","START_DATE","END_DATE","COMPANY_NAME","TENURE","INTEREST_RATE","AMOUNT","BROKERAGE_PERCENTAGE","BROKERAGE_AMOUNT","CREATED_BY","MODIFIED_BY"]

@admin.register(User_Role_Permission)
class User_Role_PermissionAdmin(admin.ModelAdmin):
  list_display = ("id","USER_TYPE","ALLOWED_MODULES","CREATED_BY","MODIFIED_BY")
  list_filter = ["id","USER_TYPE","ALLOWED_MODULES","CREATED_BY","MODIFIED_BY"]

# @admin.register(Commission_paid)
@admin.register(Commission_paid)
class Commission_paidAdmin(admin.ModelAdmin):
  list_display = ("id","EP","AMOUNT","TRANSACTION_DATE","TRANSACTION_CHECK_NO","CREATED_BY","MODIFIED_BY")
  list_filter = ["id","EP","AMOUNT","TRANSACTION_DATE","TRANSACTION_CHECK_NO","CREATED_BY","MODIFIED_BY"]

@admin.register(Buy_MF)
class Buy_MFAdmin(admin.ModelAdmin):
  list_display = ("id","EP_RM","USER_TYPE","DATE","CUSTOMER","CUSTOMER_STATUS","SCHEME_NAME","AMOUNT_INVESTED","MODE","BUY_TYPE")
  list_filter = ("id","EP_RM","USER_TYPE","DATE","CUSTOMER","CUSTOMER_STATUS","SCHEME_NAME","AMOUNT_INVESTED","MODE","BUY_TYPE")

@admin.register(Insurance_master)
class Insurance_masterAdmin(admin.ModelAdmin):
  list_display = ("id","INSURER","PRODUCT","PLAN_TYPE")

@admin.register(Demat_account)
class Demat_accountAdmin(admin.ModelAdmin):
  list_display = ("id","DEPOSITORY_TYPE")


admin.site.register(UploadInsuranceMaster)
admin.site.register(UploadMFMaster)
admin.site.register(MF_master)
