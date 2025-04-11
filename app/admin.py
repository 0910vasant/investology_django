from django.contrib import admin
from .models import Holding_nature_master ,Country_master , Bank_account_type_master ,Investor_category_master, KYC_data_logs,Tax_status_master,Bank_proof_master,Gross_annual_income_master,Scan_pan,Registration_personal_details , Registration_mfu_details ,Registration_holder_details ,Registration_bank_details ,Registration_communication_details,Nominee_details,Registration_nominee_details,Cart,Scheme_category,Scheme_sub_category,investology_login_session,Header_Checklist,Enc_password,User_Otp,Bank_master,Occupation_master,Mobile_belongs_to ,Nominee_Relation,can_creation_request_response
# Register your models here.


@admin.register(Mobile_belongs_to)
class Mobile_belongs_toAdmin(admin.ModelAdmin):
  list_display = ("id","CODE","NAME")

@admin.register(Nominee_Relation)
class Nominee_RelationAdmin(admin.ModelAdmin):
  list_display = ("id","NOM_REL_CODE","NOM_GURI_REL_CODE","NAME")

  


# USER
# REQUEST
# RESPONSE
admin.site.register(can_creation_request_response)
admin.site.register(Holding_nature_master)
# admin.site.register(Bank_account_type_master)
admin.site.register(Investor_category_master)

admin.site.register(Bank_proof_master)
admin.site.register(Gross_annual_income_master)

@admin.register(Tax_status_master)
class Tax_status_masterAdmin(admin.ModelAdmin):
  list_display = ("id","TAX_STATUS","TAX_STATUS_DESCRIPTION","TAX_STATUS_CODE")


@admin.register(Bank_master)
class Bank_masterAdmin(admin.ModelAdmin):
  list_display = ("id","NAME","CODE","PD","PN","NET_BANKING")
  search_fields = ['CODE']
# admin.site.register(Source_of_wealth_master)
# admin.site.register(Kra_address_type_master)
admin.site.register(Occupation_master)
# admin.site.register(Pep_status_master)
@admin.register(Country_master)
class Country_masterAdmin(admin.ModelAdmin):
  list_display = ("id","NAME","CODE")

# admin.site.register(State_master)
# admin.site.register(Pincode_master)
# admin.site.register(Identification_type_master)
@admin.register(Enc_password)
class Enc_passwordAdmin(admin.ModelAdmin):
  list_display = ("id","KEY","PASSWORD","ENC_PASSWORD")
# admin.site.register(Enc_password)
admin.site.register(Scan_pan)
# admin.site.register(Registration_personal_details)

@admin.register(Registration_personal_details)
class Registration_personal_detailsAdmin(admin.ModelAdmin):
  list_display = ("id","NAME","MOBILE","PAN_NO","CAN","CAN_STATUS","NOM_LINK_1","NOM_LINK_2","NOM_LINK_3")
  search_fields = ['MOBILE',"CAN_STATUS"]

@admin.register(Bank_account_type_master)
class Bank_account_type_masterAdmin(admin.ModelAdmin):
  list_display = ("id","BANK_ACCOUNT_TYPE","ACC_TYPE_FULL_FORM")


@admin.register(Registration_mfu_details)
class Registration_mfu_detailsAdmin(admin.ModelAdmin):
  list_display = ("id","USER","HOLDING_NATURE","INVESTOR_CATEGORY","TAX_STATUS","HOLDING_COUNT","IS_DELETED")
  search_fields = ['HOLDING_NATURE__HOLDING_TYPE',]

# admin.site.register(Registration_mfu_details)
@admin.register(Registration_holder_details)
class Registration_holder_detailsAdmin(admin.ModelAdmin):
  list_display = ("id","USER","HOLDER_TYPE","HOLDER_NAME","PAN_NO","TAX_RES_FLAG","IS_DELETED")
  list_filter   = ["USER",]

# admin.site.register(Registration_holder_details)

@admin.register(Registration_bank_details)
class Registration_bank_detailsAdmin(admin.ModelAdmin):
  list_display = ("id","USER","DEFAULT_BANK","ACC_NO","MMRN","PRN","IS_DELETED")
  list_filter   = ["USER","PRN"]
  search_fields = ["ACC_NO",]

# admin.site.register(Registration_bank_details)
# admin.site.register(Registration_bank_details)
# @admin.register(Registration_bank_details)
# class Registration_bank_detailsAdmin(admin.ModelAdmin):
#   list_display = ("id","USER","DEPOSITORY")
admin.site.register(Registration_communication_details)
# admin.site.register(Registration_kyc_details)
admin.site.register(Nominee_details)
admin.site.register(Registration_nominee_details)
# admin.site.register(Tax_details)


@admin.register(Cart)
class CartAdmin(admin.ModelAdmin):
  list_display = ("id","USER","BUY_TYPE")

@admin.register(Scheme_category)
class Scheme_categoryAdmin(admin.ModelAdmin):
  list_display = ("id","CATEGORY","CATEGORY_ID")

@admin.register(Scheme_sub_category)
class Scheme_sub_categoryAdmin(admin.ModelAdmin):
  list_display = ("id","CATEGORY","SUB_CATEGORY","SUB_CATEGORY_ID")


@admin.register(investology_login_session)
class investology_login_sessionAdmin(admin.ModelAdmin):
  list_display = ("id","APP_TYPE","SESSIONCONTEXT","SENDERSUBID")

@admin.register(Header_Checklist)
class Header_ChecklistAdmin(admin.ModelAdmin):
  list_display = ("id","APP_TYPE","CHECKLIST_USE_FOR","ENTITY_ID","ENTITY_NAME","LOGIN_ID","PASSWORD","EN_ENCR_PASSWORD","BASE_URL")

@admin.register(User_Otp)
class User_OtpAdmin(admin.ModelAdmin):
  list_display = ("id","MOBILE_NO","OTP")

@admin.register(KYC_data_logs)
class KYC_data_logsAdmin(admin.ModelAdmin):
  list_display = ("id","REQUEST_ID","CLIENT_REF_ID","CUSTOMER_IDENTIFIER","WORKFLOW_NAME")
  





  

