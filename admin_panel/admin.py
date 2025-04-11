from django.contrib import admin
from .models import Cams_kfintech_NAV, Cams_kfintech_schemes_master, Upload_scheme , Schemes, Threshold, AMC , Cams_kfintech_transaction, Cams_kfintech_transaction_details, customer_transaction
# Register your models here.

@admin.register(Upload_scheme)
class Upload_schemeAdmin(admin.ModelAdmin):
  list_display = ("id","EXCEL")

#@admin.register(Schemes)
# class SchemesAdmin(admin.ModelAdmin):
#   list_display = ("id","SCHEME_CODE","FUND_CODE")


@admin.register(Schemes)
class SchemesAdmin(admin.ModelAdmin):
  list_display = ("id","SCHEME_CODE","PLAN_NAME","SIP_HUNDRED")
  # list_filter = ("id",'CATEGORY',"PLAN_NAME","PLAN_TYPE","PLAN_OPT","SIP_HUNDRED")

  list_filter = ("id",'CATEGORY',"PLAN_NAME","PLAN_TYPE","PLAN_OPT","SIP_HUNDRED","FUND_CODE__FUND_NAME")

  search_fields = ['id']
  search_fields = ['id', 'SCHEME_CODE','PLAN_NAME' ]
  # def fund_code(self,obj):
  #   if obj.FUND_CODE:
  #     return FUND_CODE.FUND_CODE
  #   else:
  #     return ""
    
  # def fund_name(self,obj):
  #   if obj.FUND_CODE:
  #     return FUND_CODE.FUND_NAME
  #   else:
  #     return ""

  
admin.site.register(Threshold)



@admin.register(AMC)
class AMCAdmin(admin.ModelAdmin):
  list_display = ("id","FUND_CODE","FUND_NAME","COMPANY","COMPANY_FUND_CODE")
  search_fields = ['COMPANY',]



@admin.register(Cams_kfintech_transaction)
class Cams_kfintech_transactionAdmin(admin.ModelAdmin):
  list_display = ("id",)

@admin.register(Cams_kfintech_transaction_details)
class Cams_kfintech_transaction_detailsAdmin(admin.ModelAdmin):
  list_display = ("id",)
  
@admin.register(customer_transaction)
class customer_transaction_detailsAdmin(admin.ModelAdmin):
  list_display = ("id","PAN_NO","CUST_NAME")


@admin.register(Cams_kfintech_schemes_master)
class Cams_kfintech_schemes_masterAdmin(admin.ModelAdmin):
  list_display = ("id","COMPANY","SCHEME_CODE","PRODCODE")

  search_fields = ['PRODCODE',]


# @admin.register(Cams_kfintech_NAV)
# class Cams_kfintech_NAVAdmin(admin.ModelAdmin):
#   list_display = ("id","COMPANY","PRODCODE__PRODCODE","NAV_DATE","NAV_VALUE")

#   search_fields = ['PRODCODE',]

  



