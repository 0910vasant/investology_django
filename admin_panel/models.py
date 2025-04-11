import os
from django.db import models

# Create your models here.



class Schemes(models.Model):
    # AMC                 = models.ForeignKey('admin_panel.AMC',on_delete=models.CASCADE,null=True)
    SCHEME_CODE         = models.CharField(max_length=30,blank=True,null=True,verbose_name="Scheme Code")
    FUND_CODE           = models.ForeignKey('admin_panel.AMC',on_delete=models.CASCADE,null=True)
    PLAN_NAME           = models.TextField(blank=True,null=True,verbose_name="Plan Name")
    SCHEME_TYPE         = models.CharField(max_length=10,blank=True,null=True,verbose_name="Scheme Type")
    PLAN_TYPE           = models.CharField(max_length=10,blank=True,null=True,verbose_name="Plan Type")
    PLAN_OPT            = models.CharField(max_length=30,blank=True,null=True,verbose_name="Plan opt")
    DIV_OPT             = models.CharField(max_length=30,blank=True,null=True,verbose_name="Div opt")
    AMFI_ID             = models.CharField(max_length=30,blank=True,null=True,verbose_name="Amfi Id")
    PRI_ISIN            = models.CharField(max_length=30,blank=True,null=True,verbose_name="Pri isin")
    SEC_ISIN            = models.CharField(max_length=30,blank=True,null=True,verbose_name="Sec isin")
    NFO_START           = models.DateField(blank=True,null=True,verbose_name="Nfo Start")
    NFO_END             = models.DateField(blank=True,null=True,verbose_name="Nfo End")
    ALLOT_DATE          = models.DateField(blank=True,null=True,verbose_name="Allot Date")
    REOPEN_DATE         = models.DateField(blank=True,null=True,verbose_name="Reopen Date")
    MATURITY_DATE       = models.DateField(blank=True,null=True,verbose_name="Maturity Date")
    ENTRY_LOAD          = models.TextField(blank=True,null=True,verbose_name="Entry Load")
    EXIT_LOAD           = models.TextField(blank=True,null=True,verbose_name="Exit Load")
    PUR_ALLOWED         = models.CharField(max_length=20,blank=True,null=True,verbose_name="Pur Allowed")
    NFO_ALLOWED         = models.CharField(max_length=20,blank=True,null=True,verbose_name="Nfo Allowed")
    REDEEM_ALLOWED      = models.CharField(max_length=20,blank=True,null=True,verbose_name="Redeem Allowed")
    SIP_ALLOWED         = models.CharField(max_length=20,blank=True,null=True,verbose_name="Sip Allowed")
    SWITCH_OUT_ALLOWED  = models.CharField(max_length=20,blank=True,null=True,verbose_name="switch out Allowed")
    SWITCH_IN_ALLOWED   = models.CharField(max_length=20,blank=True,null=True,verbose_name="switch in Allowed")
    STP_OUT_ALLOWED     = models.CharField(max_length=20,blank=True,null=True,verbose_name="stp out Allowed")
    STP_IN_ALLOWED      = models.CharField(max_length=20,blank=True,null=True,verbose_name="stp in Allowed")
    SWP_ALLOWED         = models.CharField(max_length=20,blank=True,null=True,verbose_name="swp Allowed")
    DEMAT_ALLOWED       = models.CharField(max_length=20,blank=True,null=True,verbose_name="demat Allowed")
    CATEGORY            = models.ForeignKey('app.Scheme_sub_category',on_delete=models.CASCADE,null=True)
    SCHEME_FLAG         = models.CharField(max_length=500,blank=True,null=True,verbose_name="scheme_flag")

    SIP_HUNDRED         = models.BooleanField(default=False)
    ORDER_NO            = models.CharField(max_length=20,blank=True,null=True,verbose_name="Order No")
    

    NEW_SCHEME          = models.BooleanField(default=False)
    IS_DELETED          = models.BooleanField(default=False)
    CREATED_DATE        = models.DateTimeField(auto_now_add=True,null=True)
    UPDATED_DATE        = models.DateTimeField(auto_now=True)
    
    class Meta:
        verbose_name = 'Scheme'
        verbose_name_plural = 'Scheme'

class Upload_scheme(models.Model):
    EXCEL = models.FileField(upload_to="Scheme Master",max_length=500,blank=True,null=True,verbose_name= "Upload Scheme Master")
    # SHEET_NAME = models.CharField(max_length=100,null=True,verbose_name="Sheet Name")
    
    IS_DELETED=models.BooleanField(default=False,null=True)
    CREATED_DATE = models.DateTimeField(auto_now_add=True,null=True)
    UPDATED_DATE = models.DateTimeField(auto_now=True,null=True)

    def delete(self,*args,**kwargs):
        # logger.info(f"delete PAth = {self.EXCEL.path}")
        # logger.info(f"Enter delete")
        if os.path.isfile(self.EXCEL.path):
            os.remove(self.EXCEL.path)
        super(Upload_scheme, self).delete(*args,**kwargs)
    class Meta:
        verbose_name_plural = "Upload Scheme Master"

class Threshold(models.Model):
    FUND_CODE           = models.ForeignKey('admin_panel.AMC',on_delete=models.CASCADE,null=True)
    SCHEME_CODE         = models.CharField(max_length=500,blank=True,null=True,verbose_name="Scheme Code")
    TXN_TYPE            = models.CharField(max_length=500,blank=True,null=True,verbose_name="Txn Type")
    SYS_FREQ            = models.CharField(max_length=500,blank=True,null=True,verbose_name="Sys Freq")
    SYS_FREQ_OPT        = models.CharField(max_length=500,blank=True,null=True,verbose_name="Sys Freq Opt")
    SYS_DATES           = models.TextField(blank=True,null=True,verbose_name="Sys Dates")
    MIN_AMT             = models.CharField(max_length=500,blank=True,null=True,verbose_name="Min Amt")
    MAX_AMT             = models.CharField(max_length=500,blank=True,null=True,verbose_name="Max Amt")
    MULTIPLE_AMT        = models.CharField(max_length=500,blank=True,null=True,verbose_name="Multiple Amt")
    MIN_UNITS           = models.CharField(max_length=500,blank=True,null=True,verbose_name="Min Units")
    MULTIPLE_UNITS      = models.CharField(max_length=500,blank=True,null=True,verbose_name="Multiple Units")
    MIN_INST            = models.CharField(max_length=500,blank=True,null=True,verbose_name="Min Inst")
    MAX_INST            = models.CharField(max_length=500,blank=True,null=True,verbose_name="Max Inst")
    SYS_PERPETUAL       = models.CharField(max_length=500,blank=True,null=True,verbose_name="Sys Perpetual")
    MIN_CUM_AMT         = models.CharField(max_length=500,blank=True,null=True,verbose_name="Min Cum Amt")
    START_DATE          = models.DateField(blank=True,null=True,verbose_name="Start Date")
    END_DATE            = models.DateField(blank=True,null=True,verbose_name="End Date")

    IS_DELETED      = models.BooleanField(default=False)
    CREATED_DATE    = models.DateTimeField(auto_now_add=True,null=True)
    UPDATED_DATE    = models.DateTimeField(auto_now=True)
    
    class Meta:
        verbose_name = 'Threshold'
        verbose_name_plural = 'Threshold'

class AMC(models.Model):
    FUND_CODE            = models.CharField(max_length=500,null=True,blank=True,verbose_name="Fund Code")
    FUND_NAME            = models.CharField(max_length=500,null=True,blank=True,verbose_name="Fund Name")

    company_choices = (
        ('cams','CAMS'),
        ('kfintech','KFintech')
    )
    COMPANY             = models.CharField(max_length=250,choices=company_choices,null=True,verbose_name="Company Name")
    COMPANY_FUND_CODE   = models.CharField(max_length=500,null=True,blank=True,verbose_name="Company Fund Code")

    IS_DELETED          = models.BooleanField(default=False)
    CREATED_DATE        = models.DateTimeField(auto_now_add=True,null=True)
    UPDATED_DATE        = models.DateTimeField(auto_now=True,null=True)

    class Meta:
        verbose_name = 'Amc Master'
        verbose_name_plural = 'Amc Master'

class Scheme_type_master(models.Model):
    NAME                = models.CharField(max_length=500,null=True,blank=True,verbose_name="Name")
     
    IS_DELETED          = models.BooleanField(default=False)
    CREATED_DATE        = models.DateTimeField(auto_now_add=True,null=True)
    UPDATED_DATE        = models.DateTimeField(auto_now=True,null=True)

    class Meta:
        verbose_name = 'Amc Master'
        verbose_name_plural = 'Amc Master'


class Cams_kfintech_schemes_master(models.Model):
    company_choices = (
        ('cams','CAMS'),
        ('kfintech','KFintech')
    )
    COMPANY             = models.CharField(max_length=250,choices=company_choices,null=True,verbose_name="Company Name")
    FUND_CODE           = models.CharField(max_length=500,null=True,blank=True,verbose_name="Fund Code")
    SCHEME_CODE         = models.CharField(max_length=500,null=True,blank=True,verbose_name="Fund Name")
    PRODCODE            = models.CharField(max_length=500,null=True,blank=True,verbose_name="Product Name")
    SCHEME_NAME         = models.TextField(blank=True,null=True,verbose_name="Schmes Name")
    ISIN_NO             = models.CharField(max_length=100,null=True,blank=True,verbose_name="Schmes ISIN Number")
    NAV_VALUE           = models.CharField(max_length=50,null=True,blank=True,verbose_name="NAV Value")
    NAV_DATE            = models.DateField(blank=True,null=True,verbose_name="NAV Date")

    IS_DELETED          = models.BooleanField(default=False)
    CREATED_DATE        = models.DateTimeField(auto_now_add=True,null=True)
    UPDATED_DATE        = models.DateTimeField(auto_now=True,null=True)

    class Meta:
        verbose_name = 'Cams Kfintech Schemes Master'
        verbose_name_plural = 'Cams Kfintech Schemes Master'
    
    		# scheme_type	isin_no	swing_nav

# class Cams_kfintech_transaction(models.Model):
#     company_choices = (
#         ('cams','CAMS'),
#         ('kfintech','KFintech')
#     )
#     COMPANY             = models.CharField(max_length=250,choices=company_choices,null=True,verbose_name="Company Name")
class customer_transaction(models.Model):
    PAN_NO              = models.CharField(max_length=500,null=True,blank=True,verbose_name="Pan Number")
    CUST_NAME           = models.CharField(max_length=500,null=True,blank=True,verbose_name="Customer Name")

    IS_DELETED          = models.BooleanField(default=False)
    CREATED_DATE        = models.DateTimeField(auto_now_add=True,null=True)
    UPDATED_DATE        = models.DateTimeField(auto_now=True,null=True)

    class Meta:
        verbose_name = 'Customer Transactions'
        verbose_name_plural = 'Customer Transactions'


class Cams_kfintech_transaction(models.Model):
    PROD_CODE           = models.ForeignKey('admin_panel.Cams_kfintech_schemes_master',on_delete=models.CASCADE,null=True,blank=True)
    INV_NAME            = models.ForeignKey('admin_panel.customer_transaction',on_delete=models.CASCADE,null=True,blank=True)
    FOLIO_NO            = models.CharField(max_length=100,null=True,blank=True,verbose_name="Folio No")
    ALT_FOLIO_NO        = models.CharField(max_length=100,null=True,blank=True,verbose_name="Alt Folio No")

    IS_DELETED          = models.BooleanField(default=False)
    CREATED_DATE        = models.DateTimeField(auto_now_add=True,null=True)
    UPDATED_DATE        = models.DateTimeField(auto_now=True)
    class Meta:
            verbose_name = 'Cams Transaction'
            verbose_name_plural = 'Cams Transaction'

class Cams_kfintech_transaction_details(models.Model):
    FOLIO_NO            = models.ForeignKey('admin_panel.Cams_kfintech_transaction',on_delete=models.CASCADE,null=True,blank=True)

    company_choices = (
        ('cams','CAMS'),
        ('kfintech','KFintech')
    )
    COMPANY             = models.CharField(max_length=100,choices=company_choices,null=True,verbose_name="Company Name")

    TRXNTYPE            = models.CharField(max_length=50,null=True,blank=True,verbose_name="Transaction Type")
    TRXNNO              = models.CharField(max_length=50,null=True,blank=True,verbose_name="Transaction Number")
    TRXNMODE            = models.CharField(max_length=50,null=True,blank=True,verbose_name="Transaction Mode")
    TRXNSTAT            = models.TextField(null=True,blank=True)
    # models.CharField(max_length=500,null=True,blank=True,verbose_name="Transaction Stat")
    
    USERCODE            = models.CharField(max_length=100,null=True,blank=True,verbose_name="User Code")
    USRTRXNO            = models.CharField(max_length=100,null=True,blank=True,verbose_name="User Transaction Number")
    TRADDATE            = models.DateField(blank=True,null=True,verbose_name="Trade Date")
    POSTDATE            = models.DateField(blank=True,null=True,verbose_name="Post Date")
    PURPRICE            = models.CharField(max_length=100,null=True,blank=True,verbose_name="Purchase Price")
    UNITS               = models.CharField(max_length=100,null=True,blank=True,verbose_name="Units")
    AMOUNT              = models.CharField(max_length=100,null=True,blank=True,verbose_name="Amounts")


    SUBBROK             = models.CharField(max_length=50,null=True,blank=True,verbose_name="Sub Broker Code")
    TRXN_NATURE         = models.CharField(max_length=500,null=True,blank=True,verbose_name="Transaction Nature")
    SWFLAG              = models.CharField(max_length=50,null=True,blank=True,verbose_name="sw Flag")

    OLD_FOLIO_NO        = models.CharField(max_length=50,null=True,blank=True,verbose_name="Old Folio No")

    SEQ_NO              = models.CharField(max_length=50,null=True,blank=True,verbose_name="Sequence Number")
    REINVEST_FLAG       = models.CharField(max_length=50,null=True,blank=True,verbose_name="Reinvest Flag")

    LOCATION            = models.CharField(max_length=100,null=True,blank=True,verbose_name="Location")
    SCHEME_TYPE         = models.CharField(max_length=100,null=True,blank=True,verbose_name="Scheme Type")
    TAX_STATUS          = models.CharField(max_length=100,null=True,blank=True,verbose_name="Tax Status")


    PAN_NO              = models.CharField(max_length=20,null=True,blank=True,verbose_name="Pan Number")
    TARG_SRC_SCHEME     = models.CharField(max_length=50,null=True,blank=True,verbose_name="Target Source Scheme")
    TRXN_TYPE_FLAG      = models.TextField(null=True,blank=True)

    TRXN_SUFFIX         = models.TextField(null=True,blank=True)
    SIPTRXNNO           = models.CharField(max_length=50,null=True,blank=True,verbose_name="Sip Transaction Number")
    TER_LOCATION        = models.CharField(max_length=50,null=True,blank=True,verbose_name="Ter Location")

    EUIN                = models.CharField(max_length=50,null=True,blank=True,verbose_name="Euin")
    EUIN_VALID          = models.CharField(max_length=50,null=True,blank=True,verbose_name="Euin Valid")
    EUIN_OPTED          = models.CharField(max_length=50,null=True,blank=True,verbose_name="Euin opted")
    SUB_BRK_ARN         = models.CharField(max_length=50,null=True,blank=True,verbose_name="Sub Broker Arn")

    SRC_BRK_CODE        = models.CharField(max_length=50,null=True,blank=True,verbose_name="Source Broker Code")
    SYS_REGN_DATE       = models.DateField(blank=True,null=True,verbose_name="System Date")

    ACC_NO              = models.CharField(max_length=50,null=True,blank=True,verbose_name="Account Number")
    BANK_NAME           = models.TextField(null=True,blank=True)
    GST_STATE_CODE      = models.CharField(max_length=50,null=True,blank=True,verbose_name="GST State Code")
    STAMP_DUTY          = models.CharField(max_length=50,null=True,blank=True,verbose_name="Stamp Duty")

    IS_DELETED          = models.BooleanField(default=False)
    CREATED_DATE        = models.DateTimeField(auto_now_add=True,null=True)
    UPDATED_DATE        = models.DateTimeField(auto_now=True)
    class Meta:
            verbose_name = 'Cams & Kfitech Transaction Details'
            verbose_name_plural = 'Cams & Kfitech Transaction Details'

class Cams_kfintech_NAV(models.Model):
    company_choices = (
        ('cams','CAMS'),
        ('kfintech','KFintech')
    )
    COMPANY             = models.CharField(max_length=100,choices=company_choices,null=True,verbose_name="Company Name")
    PRODCODE           = models.ForeignKey('admin_panel.Cams_kfintech_schemes_master',on_delete=models.CASCADE,null=True,blank=True)
    NAV_DATE            = models.DateField(blank=True,null=True,verbose_name="NAV Date")
    NAV_VALUE           = models.CharField(max_length=50,null=True,blank=True,verbose_name="NAV Value")
            
    IS_DELETED          = models.BooleanField(default=False)
    CREATED_DATE        = models.DateTimeField(auto_now_add=True,null=True)
    UPDATED_DATE        = models.DateTimeField(auto_now=True)
    class Meta:
        verbose_name = 'Cams & Kfitech NAV'
        verbose_name_plural = 'Cams & Kfitech NAV'
            
            
            
    