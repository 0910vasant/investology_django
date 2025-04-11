import os
from django.db import models
from django.contrib.auth.hashers import make_password
from app.pass_enc import encrypt,decrypt
from django.core.exceptions import ValidationError
import logging
logger = logging.getLogger(__name__)

# Create your models here.

# master start
class Holding_nature_master(models.Model):
    CODE = models.CharField(max_length=2)
    HOLDING_TYPE = models.CharField(max_length=500)

    IS_DELETED = models.BooleanField(default=False)
    CREATED_DATE = models.DateTimeField(auto_now_add=True)
    UPDATED_DATE = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.HOLDING_TYPE 
    
    class Meta:
        verbose_name = 'Holding Nature Master'
        verbose_name_plural = 'Holding Nature Master'


class Bank_account_type_master(models.Model):
    BANK_ACCOUNT_TYPE = models.CharField(max_length=500)
    ACC_TYPE_FULL_FORM = models.CharField(max_length=500,null=True,blank=True)

    IS_DELETED = models.BooleanField(default=False)
    CREATED_DATE = models.DateTimeField(auto_now_add=True)
    UPDATED_DATE = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.BANK_ACCOUNT_TYPE 
    
    class Meta:
        verbose_name = 'Banck Acc Type Master'
        verbose_name_plural = 'Banck Acc Type Master'


class Investor_category_master(models.Model):
    NAME = models.CharField(max_length=500)
    CODE = models.CharField(max_length=500)

    IS_DELETED = models.BooleanField(default=False)
    CREATED_DATE = models.DateTimeField(auto_now_add=True)
    UPDATED_DATE = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.CODE} - {self.NAME}"
    
    class Meta:
        verbose_name = 'Investor Category Master'
        verbose_name_plural = 'Investor Category Master'


class Tax_status_master(models.Model):
    INVESTOR_CATGORY        = models.ForeignKey(Investor_category_master,on_delete=models.CASCADE)
    TAX_STATUS              = models.CharField(max_length=500)
    TAX_STATUS_DESCRIPTION  = models.CharField(max_length=500)
    TAX_STATUS_CODE         = models.CharField(max_length=500)
    BANK_ACCOUNT_TYPE       = models.ManyToManyField(Bank_account_type_master)

    IS_DELETED              = models.BooleanField(default=False)
    CREATED_DATE            = models.DateTimeField(auto_now_add=True)
    UPDATED_DATE            = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f'Code : {self.TAX_STATUS} - Desc : {self.TAX_STATUS_DESCRIPTION}'
    
    class Meta:
        verbose_name = 'Tax Status Master'
        verbose_name_plural = 'Tax Status Master'


class Bank_proof_master(models.Model):
    NAME = models.CharField(max_length=500)
    CODE = models.CharField(max_length=500)

    IS_DELETED = models.BooleanField(default=False)
    CREATED_DATE = models.DateTimeField(auto_now_add=True)
    UPDATED_DATE = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.CODE} - {self.NAME}"
    
    class Meta:
        verbose_name = 'Bank Proof Master'
        verbose_name_plural = 'Bank Proof Master'


class Gross_annual_income_master(models.Model):
    NAME = models.CharField(max_length=500)
    CODE = models.CharField(max_length=500)

    IS_DELETED = models.BooleanField(default=False)
    CREATED_DATE = models.DateTimeField(auto_now_add=True)
    UPDATED_DATE = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.CODE} - {self.NAME}"
    
    class Meta:
        verbose_name = 'Gross Annual Income Master'
        verbose_name_plural = 'Gross Annual Income Master'


class Source_of_wealth_master(models.Model):
    NAME = models.CharField(max_length=500)
    CODE = models.CharField(max_length=500)

    IS_DELETED = models.BooleanField(default=False)
    CREATED_DATE = models.DateTimeField(auto_now_add=True)
    UPDATED_DATE = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.CODE} - {self.NAME}"
    
    class Meta:
        verbose_name = 'Source of Wealth Master'
        verbose_name_plural = 'Source of Wealth Master'


class Kra_address_type_master(models.Model):
    NAME = models.CharField(max_length=500)
    CODE = models.CharField(max_length=500)

    IS_DELETED = models.BooleanField(default=False)
    CREATED_DATE = models.DateTimeField(auto_now_add=True)
    UPDATED_DATE = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.CODE} - {self.NAME}"
    
    class Meta:
        verbose_name = 'Kra address type Master'
        verbose_name_plural = 'Kra address type Master'


class Occupation_master(models.Model):
    NAME = models.CharField(max_length=500)
    CODE = models.CharField(max_length=500)

    IS_DELETED = models.BooleanField(default=False)
    CREATED_DATE = models.DateTimeField(auto_now_add=True)
    UPDATED_DATE = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.CODE} - {self.NAME}"
    
    class Meta:
        verbose_name = 'Occupation Master'
        verbose_name_plural = 'Occupation Master'


class Pep_status_master(models.Model):
    NAME = models.CharField(max_length=500)
    CODE = models.CharField(max_length=500)

    IS_DELETED = models.BooleanField(default=False)
    CREATED_DATE = models.DateTimeField(auto_now_add=True)
    UPDATED_DATE = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.CODE} - {self.NAME}"
    
    class Meta:
        verbose_name = 'PEP Status Master'
        verbose_name_plural = 'PEP Status Master'


class Country_master(models.Model):
    NAME = models.CharField(max_length=500)
    CODE = models.CharField(max_length=500)

    IS_DELETED = models.BooleanField(default=False)
    CREATED_DATE = models.DateTimeField(auto_now_add=True,null=True)
    UPDATED_DATE = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.CODE} - {self.NAME}"
    
    class Meta:
        verbose_name = 'Country Master'
        verbose_name_plural = 'Country Master'


class State_master(models.Model):
    COUNTRY = models.ForeignKey(Country_master, on_delete=models.CASCADE)
    NAME = models.CharField(max_length=500)
    CODE = models.CharField(max_length=500)

    IS_DELETED = models.BooleanField(default=False)
    CREATED_DATE = models.DateTimeField(auto_now_add=True)
    UPDATED_DATE = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.CODE} - {self.NAME}"
    
    class Meta:
        verbose_name = 'State Master'
        verbose_name_plural = 'State Master'


class Pincode_master(models.Model):
    COUNTRY = models.ForeignKey(Country_master, on_delete=models.CASCADE)
    STATE = models.ForeignKey(State_master, on_delete=models.CASCADE)
    CITY = models.CharField(max_length=500)
    PINCODE = models.CharField(max_length=500)

    IS_DELETED = models.BooleanField(default=False)
    CREATED_DATE = models.DateTimeField(auto_now_add=True)
    UPDATED_DATE = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.id} - {self.STATE} - {self.CITY} - {self.PINCODE}"
    
    class Meta:
        verbose_name = 'Pincode Master'
        verbose_name_plural = 'Pincode Master'


class Identification_type_master(models.Model):
    NAME = models.CharField(max_length=500)
    CODE = models.CharField(max_length=500)

    IS_DELETED = models.BooleanField(default=False)
    CREATED_DATE = models.DateTimeField(auto_now_add=True)
    UPDATED_DATE = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.CODE} - {self.NAME}"

    class Meta:
        verbose_name = 'Indentification Type Master'
        verbose_name_plural = 'Indentification Type Master'
        
        
class Bank_master(models.Model):
    NAME            = models.CharField(max_length=500)
    CODE            = models.CharField(max_length=500)
    # ePayEezz Registration Banks
    #  PD - Debit Card based PN- Net Banking based
    PD              = models.BooleanField(default=False)
    PN              = models.BooleanField(default=False)
    # Net Banking-Banks
    NET_BANKING     = models.BooleanField(default=False)

    IS_DELETED      = models.BooleanField(default=False)
    CREATED_DATE    = models.DateTimeField(auto_now_add=True,null=True)
    UPDATED_DATE    = models.DateTimeField(auto_now=True,null=True)

    def __str__(self):
        return f"{self.CODE} - {self.NAME}"

    class Meta:
        verbose_name = 'Bank Master'
        verbose_name_plural = 'Bank Master'
    pass

# enc_password
class Enc_password(models.Model):
    KEY                 = models.CharField(max_length=500)
    PASSWORD            = models.CharField(max_length=500)
    ENC_PASSWORD        = models.CharField(max_length=500,null=True,blank=True)

    IS_DELETED          = models.BooleanField(default=False)
    CREATED_DATE        = models.DateTimeField(auto_now_add=True,null=True)
    UPDATED_DATE        = models.DateTimeField(auto_now=True)

    def save(self, *args, **kwargs):
        self.ENC_PASSWORD = encrypt(self.PASSWORD,self.KEY)
        super().save(*args, **kwargs)

    def clean(self):
        if Enc_password.objects.filter(KEY=self.KEY,PASSWORD=self.PASSWORD).exclude(id=self.id).exists():
            raise ValidationError("Error")
    
      
        
    class Meta:
        verbose_name = 'Encrypted Password'
        verbose_name_plural = 'Encrypted Password'


# pan images for scanning
class Scan_pan(models.Model):
    PAN_IMAGE           = models.ImageField(upload_to="pan/")
    PAN                 = models.CharField(max_length=50,null=True)

    IS_DELETED          = models.BooleanField(default=False)
    CREATED_DATE        = models.DateTimeField(auto_now_add=True,null=True)
    UPDATED_DATE        = models.DateTimeField(auto_now=True)
    
    class Meta:
        verbose_name = 'Scan Pan'
        verbose_name_plural = 'Scan Pan'
    
    def __str__(self):
        return f"id = {self.id} | Pan Number = {self.PAN} | Pan Image = {self.PAN_IMAGE}"

# registration1
class can_creation_request_response(models.Model):
    USER             = models.ForeignKey("app.Registration_personal_details", on_delete=models.CASCADE,null=True,blank=True)
    REQUEST          = models.TextField(null=True,blank=True)
    RESPONSE         = models.TextField(null=True,blank=True)

    IS_DELETED      = models.BooleanField(default=False)
    CREATED_DATE    = models.DateTimeField(auto_now_add=True,null=True)
    UPDATED_DATE    = models.DateTimeField(auto_now=True)
    
    class Meta:
        verbose_name = 'Can Creation Request Response'
        verbose_name_plural = 'Can Creation Request Response'

# personal details - registration1
class Registration_personal_details(models.Model):
    RM_EP               = models.ForeignKey("crm.User",blank=True,null=True, on_delete=models.CASCADE,verbose_name="Customer Under this user")
    BM                  = models.ForeignKey("crm.Branch_Manager",blank=True,null=True, on_delete=models.CASCADE,verbose_name="Branch Manager")
    RM                  = models.ForeignKey("crm.Relationship_Manager",blank=True,null=True, on_delete=models.CASCADE,verbose_name="Relationship Manager")
    EP                  = models.ForeignKey("crm.Easy_Partner",blank=True,null=True, on_delete=models.CASCADE,verbose_name="Easy Partner")
    utc                 = [
                            ("bm","Branch Manager"),
                            ("rm","Relationship Manager"),
                            ("ep","Easy Partner"),
                        ]
    TYPE                = models.CharField(max_length=150,blank=True,null=True,choices=utc)
    ''' 
        Above Column is for EP Advisor app
        Below Column is for Investology App
    '''
    app_type_choices = (
            ('uat','UAT'),
            ('prod','Production')
        )
    APP_TYPE        = models.CharField(max_length=250,choices=app_type_choices,null=True)
    cust_type_choices = (
            ('mfu','MFU'),
            ('other','Other')
        )
    CUST_TYPE       = models.CharField(max_length=250,choices=cust_type_choices,null=True)
    PAN_NO          = models.CharField(max_length=500,null=True,blank=True)
    NAME            = models.CharField(max_length=500)
    EMAIL           = models.CharField(max_length=500)
    MOBILE          = models.CharField(max_length=500)
    PASSWORD        = models.CharField(max_length=500)

    CAN             = models.CharField(max_length=50,null=True,blank=True)
    NOM_LINK_1      = models.TextField(null=True,blank=True)
    NOM_LINK_2      = models.TextField(null=True,blank=True)
    NOM_LINK_3      = models.TextField(null=True,blank=True)

    ''' 
        Below Column is for Can Status
        Without Approved can Investor not invest any mutual funds
    '''
    can_status_choices = (
            ('AP','Approved'),
            ('PE','Pending'),
            ('RJ','Rejected'),
            ('OH','On Hold'),
            ('SM','Submit to MFU'),
            
        )
    CAN_STATUS      = models.CharField(max_length=100,choices=can_status_choices,default='PE')
    REASONS         = models.TextField(null=True,blank=True)

    IS_DELETED      = models.BooleanField(default=False)
    CREATED_DATE    = models.DateTimeField(auto_now_add=True,null=True)
    UPDATED_DATE    = models.DateTimeField(auto_now=True)
    
    class Meta:
        verbose_name = 'Registration Personal Details'
        verbose_name_plural = 'Registration Personal Details'

    def save(self, *args, **kwargs):
        # if Registration_personal_details.objects.filter(MOBILE=self.MOBILE,IS_DELETED=False).exists():
        if Registration_personal_details.objects.filter(id=self.id).exists():
            # logger.info("1")
            a = Registration_personal_details.objects.get(id = self.id)
            if a.PASSWORD == self.PASSWORD:
                # logger.info("2")
                return super().save(*args, **kwargs)
            else:
                # logger.info("3")
                self.PASSWORD=make_password(self.PASSWORD)
                return super().save(*args, **kwargs)
        else:
            # logger.info("4")
            self.PASSWORD=make_password(self.PASSWORD)
            return super().save(*args, **kwargs)
    
    def __str__(self):
        return f"{self.id} - {self.NAME}"

# mfu Holder details - registration2
class Registration_mfu_details(models.Model):
    USER                    = models.ForeignKey(Registration_personal_details, on_delete=models.CASCADE,null=True,blank=True)
    HOLDING_NATURE          = models.ForeignKey(Holding_nature_master, on_delete=models.CASCADE,null=True,blank=True)
    INVESTOR_CATEGORY       = models.ForeignKey(Investor_category_master, on_delete=models.CASCADE,null=True,blank=True)
    TAX_STATUS              = models.ForeignKey(Tax_status_master, on_delete=models.CASCADE,null=True,blank=True)
    HOLDING_COUNT           = models.CharField(max_length=500,null=True,blank=True)

    IS_DELETED              = models.BooleanField(default=False)
    CREATED_DATE            = models.DateTimeField(auto_now_add=True,null=True)
    UPDATED_DATE            = models.DateTimeField(auto_now=True)

# Primary , Secondary &Third , Guardian (only for Minor) Holder
class Registration_holder_details(models.Model):
    USER                    = models.ForeignKey(Registration_personal_details, on_delete=models.CASCADE,null=True,blank=True)
    # 1) ----------      Basic Details Start     ----------
    holder_type_choice = (
        ("PR", "Primary"),
        ("SE", "Secondary"),
        ("TH", "Third"),
        ("GU", "Guardian"),
    )
    belongs_to_choice = (
        ("SE", "Self"),
        ("SP", "Spouse"),
        ("DC", "Dependent Children"),
        ("DP", "Dependent Parents"),
        ("DS", "Dependent Siblings"),
        ("GD", "Guardian"),
        ("F", "Family"),
    )

    HOLDER_TYPE             = models.CharField(choices=holder_type_choice, max_length=50,null=True,blank=True)
    HOLDER_NAME             = models.CharField(max_length=500,null=True,blank=True)
    HOLDER_DOB              = models.DateField(null=True,blank=True)
    PAN_EXEMPT_FLAG         = models.CharField(max_length=500,null=True,blank=True,default="N")
    PAN_NO                  = models.CharField(max_length=500,null=True,blank=True)
    HOLDER_PAN_IMG          = models.FileField(upload_to="Holder Pan Image",null=True,blank=True)
        # Only for Minor
    MINOR_BIRTH_CERTIFICATE = models.FileField(upload_to="Minor Birth Certificate",null=True,blank=True)
        # Contact Details Start
    RESIDENCE_ISD           = models.CharField(max_length=500,null=True,blank=True,default="91")
    RESIDENCE_STD           = models.CharField(max_length=500,null=True,blank=True)
    RESIDENCE_PHONE_NO      = models.CharField(max_length=500,null=True,blank=True)

    MOB_ISD_CODE            = models.CharField(max_length=500,null=True,blank=True,default="91")
    PRI_MOB_NO              = models.CharField(max_length=500,null=True,blank=True)
    PRI_MOB_BELONGSTO       = models.CharField(max_length=500,null=True,blank=True) # S-self ,F =Family
    ALT_MOB_NO              = models.CharField(max_length=500,null=True,blank=True)

    OFF_ISD                 = models.CharField(max_length=500,null=True,blank=True,default="91")
    OFF_STD                 = models.CharField(max_length=500,null=True,blank=True)
    OFF_PHONE_NO            = models.CharField(max_length=500,null=True,blank=True)

    PRI_EMAIL               = models.CharField(max_length=500,null=True,blank=True)
    PRI_EMAIL_BELONGSTO     = models.CharField(max_length=500,null=True,blank=True) # S-self ,F =Family
    ALT_EMAIL               = models.CharField(max_length=500,null=True,blank=True)

        # Only for Guardian
    RELATIONSHIP_WITH_MINOR = models.CharField(max_length=500,null=True,blank=True)
    PROOF_OF_RELATIONSHIP   = models.CharField(max_length=500,null=True,blank=True)
    RELATIONSHIP_PROOF_DOC  = models.FileField(upload_to="Proof Of Relationship",null=True,blank=True)
    # ----------      Basic Details End     ----------
    # 2) ----------    Additional KYC Details  Start ----------
    income_type_choice = (
        ('gross_annual_income','Gross Annual Income'),
        ('networth','Networth')
    )
    INCOME_TYPE             = models.CharField(choices=income_type_choice, max_length=50,null=True,blank=True)

    GROSS_ANNUAL_INCOME     = models.ForeignKey(Gross_annual_income_master, on_delete=models.CASCADE,null=True,blank=True)# Gross
    NETWORTH_IN_RUPEES      = models.CharField(max_length=11,null=True,blank=True)# Networth
    NETWORTH_AS_ON_DATE     = models.DateField(null=True,blank=True)# Networth

    SOURCE_OF_WEALTH        = models.ForeignKey(Source_of_wealth_master ,on_delete=models.CASCADE,null=True,blank=True)
    SOURCE_OF_WEALTH_OTHERS = models.CharField(max_length=50,null=True,blank=True)
    KRA_ADDRESS_TYPE        = models.ForeignKey(Kra_address_type_master, on_delete=models.CASCADE,null=True,blank=True)
    OCCUPATION              = models.ForeignKey(Occupation_master ,on_delete=models.CASCADE,null=True,blank=True)
    OCCUPATION_OTHERS       = models.CharField(max_length=50,null=True,blank=True)
    PEP_STATUS              = models.ForeignKey(Pep_status_master ,on_delete=models.CASCADE,null=True,blank=True)
    ANY_OTHER_INFORMATION   = models.CharField(max_length=100,null=True,blank=True)
    # ----------    Additional KYC Details  End ----------
    # 3)----------    FATCA Details  Start ----------
    tax_res_flag_choices = (
        ("Y","Yes"),
        ("N","No"),
    )
    BIRTH_CITY              = models.CharField(max_length=60,null=True,blank=True)
    BIRTH_COUNTRY           = models.ForeignKey('app.Country_master',related_name="fatca_birth_country",on_delete=models.CASCADE,null=True,blank=True)
    BIRTH_COUNTRY_OTH       = models.CharField(max_length=50,null=True,blank=True)
    CITIZENSHIP             = models.ForeignKey('app.Country_master',related_name="fatca_citizenship",on_delete=models.CASCADE,null=True,blank=True)
    CITIZENSHIP_OTH         = models.CharField(max_length=50,null=True,blank=True)
    NATIONALITY             = models.ForeignKey('app.Country_master',related_name="fatca_nationality",on_delete=models.CASCADE,null=True,blank=True)
    NATIONALITY_OTH         = models.CharField(max_length=50,null=True,blank=True)
    TAX_RES_FLAG            = models.CharField(max_length=500,choices=tax_res_flag_choices,default="N",blank=True,null=True)
            # Tax Country Other Than India
    TAX_COUNTRY             = models.ForeignKey(Country_master,on_delete=models.CASCADE,null=True,blank=True)
    TAX_COUNTRY_OTH         = models.CharField(max_length=250,null=True,blank=True)
    TAX_REF_NO              = models.CharField(max_length=500,null=True,blank=True)
    IDENTI_TYPE             = models.ForeignKey(Identification_type_master, on_delete=models.CASCADE, null=True,blank=True)
    IDENTI_TYPE_OTH         = models.CharField(max_length=500,null=True,blank=True)
    # ----------    FATCA Details  End ----------
    IS_DELETED              = models.BooleanField(default=False)
    CREATED_DATE            = models.DateTimeField(auto_now_add=True,null=True)
    UPDATED_DATE            = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = 'Registration Holder Details'
        verbose_name_plural = 'Registration Holder Details'

    def __str__(self):
        return f"{self.id} - {self.USER.NAME}"

# class Registration_mfu_details(models.Model):
    # USER                    = models.ForeignKey(Registration_personal_details, on_delete=models.CASCADE,null=True,blank=True)
    # # CAN = models.CharField(max_length=50,null=True,blank=True)
    # CLIENT_CODE             = models.CharField(max_length=500,null=True,blank=True)
    # INVESTOR_CATEGORY       = models.ForeignKey(Investor_category_master, on_delete=models.CASCADE,null=True,blank=True)
    # TAX_STATUS              = models.ForeignKey(Tax_status_master, on_delete=models.CASCADE,null=True,blank=True)
    # HOLDING_NATURE          = models.ForeignKey(Holding_nature_master, on_delete=models.CASCADE,null=True,blank=True)
    # PRIMARY_HOLDER_NAME     = models.CharField(max_length=500)
    # PRIMARY_HOLDER_DOB      = models.DateField(null=True,blank=True)
    # STATUS                  = models.CharField(max_length=500,null=True,blank=True)
    # GENDER                  = models.CharField(max_length=500)
    # SECONDARY_PAN_HOLDER    = models.CharField(max_length=500,null=True,blank=True)
    # SECONDARY_HOLDER_NAME   = models.CharField(max_length=500,null=True,blank=True)
    # SECONDARY_HOLDER_DOB    = models.CharField(max_length=500,null=True,blank=True)
    # THIRD_PAN_HOLDER        = models.CharField(max_length=500,null=True,blank=True)
    # THIRD_HOLDER_NAME       = models.CharField(max_length=500,null=True,blank=True)
    # THIRD_HOLDER_DOB        = models.CharField(max_length=500,null=True,blank=True)
    # OCCUPATION_CODE         = models.ForeignKey(Occupation_master,on_delete=models.CASCADE,null=True,blank=True)

    # IS_DELETED              = models.BooleanField(default=False)
    # CREATED_DATE            = models.DateTimeField(auto_now_add=True,null=True)
    # UPDATED_DATE            = models.DateTimeField(auto_now=True)

    # class Meta:
    #     verbose_name = 'Registration MFU Details'
    #     verbose_name_plural = 'Registration MFU Details'

    # def __str__(self):
    #     return f"{self.id} - {self.USER.NAME}"

# bank details - registration3
class Registration_bank_details(models.Model):
    USER                = models.ForeignKey(Registration_personal_details, on_delete=models.CASCADE,null=True)

    DEFAULT_BANK        = models.BooleanField(default=False)

    ACC_NO              = models.CharField(max_length=500)
    ACC_TYPE            = models.ForeignKey(Bank_account_type_master, on_delete=models.CASCADE,null=True)
    BANK_NAME           = models.ForeignKey(Bank_master,on_delete=models.CASCADE,null=True)
    MICR_NO             = models.CharField(max_length=500)
    IFSC_CODE           = models.CharField(max_length=500)
    BANK_PROOF          = models.ForeignKey(Bank_proof_master, on_delete=models.CASCADE,null=True,blank=True)
    BANK_PROOF_FILE     = models.FileField(upload_to="bank_proof",null=True)

    ''' 
        We will get below columns value when hit this api mfu_payeezz_registration for mandate
        this is for mandate reaion
    '''

    MANDATE_BANK        = models.BooleanField(default=False)
    MMRN                = models.CharField(max_length=50,null=True,blank=True)
    APPROVELINK         = models.TextField(null=True,blank=True)
    UNIQUEREFNO         = models.CharField(max_length=50,null=True,blank=True)
    TRANSACTION_LIMIT   = models.CharField(max_length=50,null=True,blank=True)
    MANDATE_START_DATE  = models.DateField(null=True,blank=True)
    MANDATE_END_DATE    = models.DateField(null=True,blank=True)
    

    ''' 
        We will get below columns value when hit this api  for mandate
        This is for epayezz validation
    '''
    mmrn_reg_status_choices = (
        ('RQ','Pending'),
        ('CL','Cancelled'),
        ('PA','Confirmed'),
        ('PR','Rejected')
    )

    mmrn_Aggr_status_choices = (
            ('RQ','Requested'),
            ('RA','Aggregator Rejected'),
            ('PA','Confirmed'),
            ('PR','Rejected'),
            ('SE','Send to Aggregator'),
            ('PS','Request Acknowledged by Aggregator'),
            ('PF','Request Rejected By Aggregator'),
            ('PE','Pending'),
            ('AC','Request Cancelled by Aggregator'),
            ('AK','Aggregator Accepted'),
        )
    
    PRN                 = models.CharField(max_length=50,null=True,blank=True)
    MMRN_REG_STATUS     = models.CharField(max_length=100,choices=mmrn_reg_status_choices,null=True,blank=True)
    MMRN_AGGR_STATUS    = models.CharField(max_length=100,choices=mmrn_Aggr_status_choices,null=True,blank=True)

    IS_DELETED          = models.BooleanField(default=False)
    CREATED_DATE        = models.DateTimeField(auto_now_add=True,null=True)
    UPDATED_DATE        = models.DateTimeField(auto_now=True)
    
    class Meta:
        verbose_name = 'Registration Bank Details'
        verbose_name_plural = 'Registration Bank Details'
    
    def __str__(self):
        return f"{self.id} - {self.USER.NAME}"


# class Registration_bank_details(models.Model):
#     depository_choices = (
#         ("cdsl", "CDSL"),
#         ("nsdl", "NSDL"),
#     )
#     USER                = models.ForeignKey(Registration_personal_details, on_delete=models.CASCADE)
#     BANK_DETAILS        = models.ManyToManyField(Registration_bank_details)
#     DEPOSITORY          = models.BooleanField(default=False)
#     DESPOSITORY_TYPE    = models.CharField(choices=depository_choices, max_length=50,null=True,blank=True)

#     IS_DELETED          = models.BooleanField(default=False)
#     CREATED_DATE        = models.DateTimeField(auto_now_add=True,null=True)
#     UPDATED_DATE        = models.DateTimeField(auto_now=True)
    
#     class Meta:
#         verbose_name = 'Registration Banks Details'
#         verbose_name_plural = 'Registration Banks Details'

#     def __str__(self):
#         return f"{self.id} - {self.USER.NAME}"


# communication details - registration4
class Registration_communication_details(models.Model):
    communication_mode_choices = (
        ('Phone','Phone'),
        ('Email','Email'),
        ('Physical','Physical')
    )
    USER                = models.ForeignKey(Registration_personal_details,null=True, on_delete=models.CASCADE)
    ADDRESS_1           = models.CharField(max_length=500)
    ADDRESS_2           = models.CharField(max_length=500,blank=True)
    ADDRESS_3           = models.CharField(max_length=500,blank=True)
    PIN_CODE            = models.ForeignKey(Pincode_master, on_delete=models.CASCADE,null=True)
    STATE               = models.ForeignKey(State_master, on_delete=models.CASCADE,null=True)
    COUNTRY             = models.ForeignKey(Country_master, on_delete=models.CASCADE,null=True)
    RESIDENCE_PHONE     = models.CharField(max_length=500,blank=True)
    RESIDENCE_FAX       = models.CharField(max_length=500,blank=True)
    OFFICE_PHONE        = models.CharField(max_length=500,blank=True)
    OFFICE_FAX          = models.CharField(max_length=500,blank=True)
    COMMUNICATION_MODE  = models.CharField(max_length=500,choices=communication_mode_choices)
    PRIMARY_EMAIL       = models.CharField(max_length=500)
    PRIMARY_MOBILE      = models.CharField(max_length=500)

    IS_DELETED          = models.BooleanField(default=False)
    CREATED_DATE        = models.DateTimeField(auto_now_add=True,null=True)
    UPDATED_DATE        = models.DateTimeField(auto_now=True)
    
    class Meta:
        verbose_name = 'Registration Communication Details'
        verbose_name_plural = 'Registration Communication Details'

    def __str__(self):
        return f"{self.id} - {self.USER.NAME}"


# kyc details - registration5
# class Registration_kyc_details(models.Model):
#     income_choices = (
#             ('gross_annual_income','Gross Annual Income'),
#             ('networth','Networth')
#         )
#     USER                    = models.ForeignKey(Registration_personal_details,null=True, on_delete=models.CASCADE)
#     INCOME                  = models.CharField(max_length=250,choices=income_choices)
#     GROSS_ANNUAL_INCOME     = models.ForeignKey(Gross_annual_income_master, on_delete=models.CASCADE,null=True)
#     NETWORTH_IN_RUPEES      = models.CharField(max_length=50,null=True)
#     NETWORTH_AS_ON_DATE     = models.DateField(null=True)

#     SOURCE_OF_WEALTH        = models.ForeignKey(Source_of_wealth_master ,on_delete=models.CASCADE,null=True)
#     SOURCE_OF_WEALTH_OTHERS = models.CharField(max_length=500,null=True,blank=True)
#     KRA_ADDRESS_TYPE        = models.ForeignKey(Kra_address_type_master, on_delete=models.CASCADE,null=True)
#     OCCUPATION              = models.ForeignKey(Occupation_master ,on_delete=models.CASCADE,null=True)
#     OCCUPATION_OTHERS       = models.CharField(max_length=500,null=True,blank=True)
#     PEP_STATUS              = models.ForeignKey(Pep_status_master ,on_delete=models.CASCADE,null=True)
#     ANY_OTHER_INFORMATION   = models.CharField(max_length=500,null=True,blank=True)

#     IS_DELETED              = models.BooleanField(default=False)
#     CREATED_DATE            = models.DateTimeField(auto_now_add=True,null=True)
#     UPDATED_DATE            = models.DateTimeField(auto_now=True)
    
#     class Meta:
#         verbose_name = 'Registration KYC Details'
#         verbose_name_plural = 'Registration KYC Details'

#     def __str__(self):
#         return f"{self.id} - {self.USER.NAME}"
class Registration_nominee_details(models.Model):
    USER                        = models.ForeignKey(Registration_personal_details, on_delete=models.CASCADE)
    nominee_option_choice = (
        ('N','No - I/We declare to Opt out'),
        ('Y','Yes - I/We wish to nominate'),
        ('X','I/We do not wish to Nominate under CAN')
    )
    nominee_verification_type_choice = (
        ('P','Physical Form'),
        ('E','Nominee 2FA'),
        ('X','Not applicable')
    )

    NOMINEE_OPTION              = models.CharField(choices=nominee_option_choice,max_length=500,null=True)
    NOMINEE_VERIFICATION_TYPE   = models.CharField(choices=nominee_verification_type_choice,max_length=500,null=True)
    # NOMINEE                 = models.BooleanField(default=False)
    # NOMINEE_DETAILS         = models.ManyToManyField(Nominee_details,blank=True)

    IS_DELETED                  = models.BooleanField(default=False)
    CREATED_DATE                = models.DateTimeField(auto_now_add=True,null=True)
    UPDATED_DATE                = models.DateTimeField(auto_now=True)
    
    class Meta:
        verbose_name = 'Registration Nominees Details'
        verbose_name_plural = 'Registration Nominees Details'

    def __str__(self):
        return f"{self.id} - {self.USER.NAME}"

# nominee details - registration6
class Nominee_details(models.Model):
    USER                        = models.ForeignKey(Registration_personal_details, on_delete=models.CASCADE)
    # REG_NOMINEE                 = models.ForeignKey("app.Registration_nominee_details", on_delete=models.CASCADE, null=True)
    NOMINEE_NAME                = models.CharField(max_length=500,null=True)
    RELATIONSHIP_WITH_CLIENT    = models.CharField(max_length=500,null=True)
    NOMINEE_PERCENTAGE          = models.CharField(max_length=500,null=True)
    NOMINEE_DOB                 = models.DateField(null=True,blank=True)
    NOMINEE_IS_MINOR            = models.BooleanField(default=False)
    GUARDIAN_NAME               = models.CharField(max_length=500,null=True,blank=True)
    GUARDIAN_RELATION           = models.CharField(max_length=500,null=True,blank=True)
    GUARDIAN_DOB                = models.DateField(null=True,blank=True)#18+

    IS_DELETED                  = models.BooleanField(default=False)
    CREATED_DATE                = models.DateTimeField(auto_now_add=True,null=True)
    UPDATED_DATE                = models.DateTimeField(auto_now=True)
    
    class Meta:
        verbose_name = 'Nominee Details'
        verbose_name_plural = 'Nominee Details'

    def __str__(self):
        return f"{self.id} - {self.USER.NAME}"





# fatca details - registartion7
# class Tax_details(models.Model):
#     FATCA                        = models.ForeignKey("app.Registration_fatca_details", on_delete=models.CASCADE,null=True)
#     other_country_tax_resident = (
#         ("yes","yes"),
#         ("no","no"),
#     )
#     USER                        = models.ForeignKey(Registration_personal_details, on_delete=models.CASCADE)
#     COUNTRY                     = models.ForeignKey(Country_master,on_delete=models.CASCADE,null=True)
#     OTHER_COUNTRY               = models.CharField(max_length=250,null=True,blank=True)
#     TAX_REFERENCE_NUMBER        = models.CharField(max_length=500)
#     IDENTIFICATION_TYPE         = models.ForeignKey(Identification_type_master, on_delete=models.CASCADE, null=True)
#     OTHERS_IDENTIFICATION_TYPE  = models.CharField(max_length=500,null=True,blank=True)

#     IS_DELETED                  = models.BooleanField(default=False)
#     CREATED_DATE                = models.DateTimeField(auto_now_add=True,null=True)
#     UPDATED_DATE                = models.DateTimeField(auto_now=True)
    
#     class Meta:
#         verbose_name = 'Registration Tax Details'
#         verbose_name_plural = 'Registration Tax Details'

#     def __str__(self):
#         return f"{self.id} - {self.USER.NAME}"


# class Registration_fatca_details(models.Model):
    # tax_resident_of_other_country_choices = (
    #     ("yes","Yes"),
    #     ("no","No"),
    # )
    # USER                            = models.ForeignKey(Registration_personal_details, on_delete=models.CASCADE)
    # BIRTH_CITY                      = models.CharField(max_length=500,null=True)
    # BIRTH_COUNTRY                   = models.ForeignKey('app.Country_master',related_name="birth_country",on_delete=models.CASCADE,null=True)
    # OTHERS_COUNTRY                  = models.CharField(max_length=500,null=True,blank=True)
    # CITIZENSHIP                     = models.ForeignKey('app.Country_master',related_name="citizenship",on_delete=models.CASCADE,null=True)
    # OTHERS_CITIZENSHIP              = models.CharField(max_length=500,null=True,blank=True)
    # NATIONALITY                     = models.ForeignKey('app.Country_master',related_name="nationality",on_delete=models.CASCADE,null=True)
    # OTHERS_NATIONALITY              = models.CharField(max_length=500,null=True,blank=True)
    # TAX_RESIDENT_OF_OTHER_COUNTRY   = models.CharField(max_length=500,choices=tax_resident_of_other_country_choices,default="no",blank=True,null=True)
    # TAX_DETAILS                     = models.ManyToManyField(Tax_details,blank=True)

    # IS_DELETED                      = models.BooleanField(default=False)
    # CREATED_DATE                    = models.DateTimeField(auto_now_add=True,null=True)
    # UPDATED_DATE                    = models.DateTimeField(auto_now=True)
    
    # class Meta:
    #     verbose_name = 'Registration FATCA Details'
    #     verbose_name_plural = 'Registration FATCA Details'

    # def __str__(self):
    #     return f"{self.id} - {self.USER.NAME}"

class Scheme_category(models.Model):
    CATEGORY        = models.CharField(max_length=500,null=True,blank=True)
    CATEGORY_ID     = models.CharField(max_length=500,null=True,blank=True)

    IS_DELETED      = models.BooleanField(default=False)
    CREATED_DATE    = models.DateTimeField(auto_now_add=True,null=True)
    UPDATED_DATE    = models.DateTimeField(auto_now=True)
    
    class Meta:
        verbose_name = 'Scheme Category'
        verbose_name_plural = 'Scheme Category'

    def __str__(self):
        return f"{self.CATEGORY}"

class Scheme_sub_category(models.Model):
    CATEGORY        = models.ForeignKey('app.Scheme_category',related_name="birth_country",on_delete=models.CASCADE,null=True)
    SUB_CATEGORY    = models.CharField(max_length=500,null=True,blank=True)
    SUB_CATEGORY_ID = models.CharField(max_length=500,null=True,blank=True)

    IS_DELETED      = models.BooleanField(default=False)
    CREATED_DATE    = models.DateTimeField(auto_now_add=True,null=True)
    UPDATED_DATE    = models.DateTimeField(auto_now=True)
    
    class Meta:
        verbose_name = 'Scheme Sub Category'
        verbose_name_plural = 'Scheme Sub Category'

class investology_login_session(models.Model):
    app_type_choices = (
            ('uat','UAT'),
            ('prod','Production')
        )
    APP_TYPE            = models.CharField(max_length=250,choices=app_type_choices,null=True)
    LASTLOGONDATE       = models.DateField(blank=True,null=True,verbose_name="Last Login Date")
    PWDEXPDATEINDAT     = models.DateField(blank=True,null=True,verbose_name="Password Expiry Date")
    FORCEADDAUTHFLG     = models.CharField(max_length=500,null=True,blank=True,verbose_name="Force Add Auth Flag")
    PARTICIPANTID       = models.CharField(max_length=500,null=True,blank=True,verbose_name="Participant id")
    OFFICEID            = models.CharField(max_length=500,null=True,blank=True,verbose_name="Office id")
    SESSIONCONTEXT      = models.CharField(max_length=500,null=True,blank=True,verbose_name="Session Context")
    SENDERSUBID         = models.CharField(max_length=500,null=True,blank=True,verbose_name="Sender Sub id")

    IS_DELETED          = models.BooleanField(default=False)
    CREATED_DATE        = models.DateTimeField(auto_now_add=True,null=True)
    UPDATED_DATE        = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = 'Investology login Session'
        verbose_name_plural = 'Investology login Session'
    
class Header_Checklist(models.Model):
    app_type_choices = (
            ('uat','UAT'),
            ('prod','Production')
        )
    checklist_use_for_choices = (
            ('can','CAN'),
            ('transaction','Transaction')
        )
    APP_TYPE                        = models.CharField(max_length=10,choices=app_type_choices,null=True)
    CHECKLIST_USE_FOR               = models.CharField(max_length=20,choices=checklist_use_for_choices,null=True)
    ENTITY_ID                       = models.CharField(max_length=10,null=True,blank=True,verbose_name="Entity Id")
    ENTITY_NAME                     = models.CharField(max_length=100,null=True,blank=True,verbose_name="Entity Name")
    LOGIN_ID                        = models.CharField(max_length=100,null=True,blank=True,verbose_name="Login Id")
    PASSWORD                        = models.CharField(max_length=100,null=True,blank=True,verbose_name="Password")
    EN_ENCR_PASSWORD                = models.CharField(max_length=100,null=True,blank=True,verbose_name="Symmetric key (for password encryption)")
    BASE_URL                        = models.CharField(max_length=255,null=True,blank=True,verbose_name="Base Url")
    ARN_NO                          = models.CharField(max_length=100,null=True,blank=True,verbose_name="Arn No")
    EUIN_CODE                       = models.CharField(max_length=100,null=True,blank=True,verbose_name="Euin Code")
    
    IS_DELETED                      = models.BooleanField(default=False,null=True)
    CREATED_DATE                    = models.DateTimeField(auto_now_add=True,null=True)
    UPDATED_DATE                    = models.DateTimeField(auto_now=True,null=True)

    class Meta:
        verbose_name = 'Header Checklist'
        verbose_name_plural = 'Header Checklist'

class Cart(models.Model):
    buy_type_choices = (
            ('additional_purchase','Additional Purchase'),
            ('mutual_funds','Mutual Funds'),
            ('sip','SIP'),
            ('swp','SWP'),
            ('switch','Switch'),
            ('stp','STP'),
            ('redemption','Redemption')
        )
    USER                = models.ForeignKey('app.Registration_personal_details',on_delete=models.CASCADE,null=True,blank=True)
    PLAN_NAME           = models.ForeignKey('admin_panel.Schemes',related_name="source_scheme",on_delete=models.CASCADE,null=True,blank=True)
    BUY_TYPE            = models.CharField(max_length=250,choices=buy_type_choices)
    FOLLIO_NO           = models.CharField(max_length=500,null=True,blank=True,verbose_name="Follio Number")
    GOAL                = models.CharField(max_length=500,null=True,blank=True,verbose_name="Goal")
    # MIN_AMT             = models.CharField(max_length=500,null=True,blank=True,verbose_name="Min Amount")
    INVEST_AMT          = models.CharField(max_length=500,null=True,blank=True,verbose_name="Investment Amount")

    FREQUENCY           = models.CharField(max_length=500,null=True,blank=True,verbose_name="Frequency")
    DAY                 = models.CharField(max_length=500,null=True,blank=True,verbose_name="Sip Day")
    START_MONTH         = models.CharField(max_length=500,null=True,blank=True,verbose_name="Start Month")
    START_YEAR          = models.CharField(max_length=500,null=True,blank=True,verbose_name="Start Year")
    NO_OF_INSTALLMENT   = models.CharField(max_length=500,null=True,blank=True,verbose_name="No Of installment")
    END_MONTH           = models.CharField(max_length=500,null=True,blank=True,verbose_name="End Month")
    END_YEAR            = models.CharField(max_length=500,null=True,blank=True,verbose_name="End Year")
    REOPEN_DATE         = models.DateField(blank=True,null=True,verbose_name="Reopen Date")

    # RTAAMCCODE          = models.CharField(max_length=500,null=True,blank=True,verbose_name="Rta Amc Code")
    # CITIZENSHIP             = models.ForeignKey('app.Country_master',related_name="fatca_citizenship",on_delete=models.CASCADE,null=True,blank=True)
    # RTASCHEMECODE       = models.CharField(max_length=500,null=True,blank=True,verbose_name="Rta Scheme Code")
    # SRCSCHEMECODE       = models.CharField(max_length=500,null=True,blank=True,verbose_name="Src Scheme Code")
    TARSCHEMECODE       = models.ForeignKey('admin_panel.Schemes',related_name="target_scheme",on_delete=models.CASCADE,null=True,blank=True)
    DIVIDENDOPTION      = models.CharField(max_length=500,null=True,blank=True,verbose_name="Dividend Option")
    TXNVOLUMETYPE       = models.CharField(max_length=500,null=True,blank=True,verbose_name="Txn Volume Type")
    # EUINDECLARATION     = models.CharField(max_length=500,null=True,blank=True,verbose_name="Euin Declaration")
    NFO_ALLOWED          = models.BooleanField(default=False)

    IS_DELETED          = models.BooleanField(default=False)
    CREATED_DATE        = models.DateTimeField(auto_now_add=True,null=True)
    UPDATED_DATE        = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = 'Cart'
        verbose_name_plural = 'Cart'


# for Can Status Check
class CanCreationStatus(models.Model):
    USER          = models.ForeignKey('app.Registration_personal_details',on_delete=models.CASCADE,null=True,blank=True)
    can_status_choices = (
            ('AP','Approved'),
            ('PE','Pending'),
            ('RJ','Rejected')
        )
    CAN_STATUS          = models.CharField(max_length=100,choices=can_status_choices,default='Pending')
    IS_DELETED          = models.BooleanField(default=False)
    CREATED_DATE        = models.DateTimeField(auto_now_add=True,null=True)
    UPDATED_DATE        = models.DateTimeField(auto_now=True)

    class Meta:
        db_table= "can_creation_status"



class User_Otp(models.Model):
    # USER                = models.ForeignKey('app.Registration_personal_details',on_delete=models.CASCADE,null=True,blank=True)
    MOBILE_NO           = models.CharField(max_length=500,null=True,blank=True,verbose_name="Mobile No")
    OTP                 = models.CharField(max_length=500,null=True,blank=True,verbose_name="Otp")

    IS_DELETED          = models.BooleanField(default=False)
    CREATED_DATE        = models.DateTimeField(auto_now_add=True,null=True)
    UPDATED_DATE        = models.DateTimeField(auto_now=True)
    class Meta:
            verbose_name = 'Otp'
            verbose_name_plural = 'Otp'

class KYC_data_logs(models.Model):
    REQUEST_ID          = models.CharField(max_length=500,null=True,blank=True,verbose_name="Request Id")
    CLIENT_REF_ID       = models.CharField(max_length=500,null=True,blank=True,verbose_name="Client Ref Id")
    CUSTOMER_IDENTIFIER = models.CharField(max_length=500,null=True,blank=True,verbose_name="Customer Identifier")
    WORKFLOW_NAME       = models.CharField(max_length=500,null=True,blank=True,verbose_name="Workflow Name")

    IS_DELETED          = models.BooleanField(default=False)
    CREATED_DATE        = models.DateTimeField(auto_now_add=True,null=True)
    UPDATED_DATE        = models.DateTimeField(auto_now=True)
    class Meta:
            verbose_name = 'KYC Logs'
            verbose_name_plural = 'KYC Logs'



# rushikesh
class Mobile_belongs_to(models.Model):
    CODE            = models.CharField(max_length=200,null=True,blank=True)
    NAME            = models.CharField(max_length=500,null=True,blank=True)

    IS_DELETED      = models.BooleanField(default=False)
    CREATED_DATE    = models.DateTimeField(auto_now_add=True)
    UPDATED_DATE    = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.NAME 
    
    class Meta:
        verbose_name = 'Mobile & Email Belongs To'
        verbose_name_plural = 'Mobile & Email Belongs To'

class Nominee_Relation(models.Model):
    NOM_REL_CODE        = models.CharField(max_length=200,null=True,blank=True) # Nominee Relation
    NOM_GURI_REL_CODE   = models.CharField(max_length=200,null=True,blank=True) # Nominee Guardian Relation
    NAME                = models.CharField(max_length=500,null=True,blank=True)

    IS_DELETED          = models.BooleanField(default=False)
    CREATED_DATE        = models.DateTimeField(auto_now_add=True)
    UPDATED_DATE        = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.NAME 
    
    class Meta:
        verbose_name = 'Nominee & Guardian Relation with Client'
        verbose_name_plural = 'Nominee & Guardian Relation with Client'
