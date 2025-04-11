from typing import Iterable, Optional
from urllib import request
from django.db import models
from django.contrib.auth.hashers import make_password
from django.core.exceptions import ValidationError
import logging
logger = logging.getLogger()
import os

# Create your models here.

class User(models.Model):
    EMPLOYEE_CODE = models.CharField(max_length=50,blank=True,null=True)
    EMPLOYEE_NUMBER = models.CharField(max_length=50,blank=True,null=True)
    BM        = models.ForeignKey("crm.Branch_Manager",blank=True,null=True, on_delete=models.CASCADE,verbose_name="Branch Manager")
    RM        = models.ForeignKey("crm.Relationship_Manager",blank=True,null=True, on_delete=models.CASCADE,verbose_name="Relationship Manager")
    EP        = models.ForeignKey("crm.Easy_Partner",blank=True,null=True, on_delete=models.CASCADE,verbose_name="Sub Broker")
    BO        = models.ForeignKey("crm.Back_Office",blank=True,null=True, on_delete=models.CASCADE)
    USER_ID   = models.TextField(blank=True,null=True,verbose_name="User id")
    NAME      = models.CharField(max_length=500,blank=True,null=True,verbose_name="Name")
    USERNAME  = models.CharField(max_length=500,null=True,verbose_name="Username")
    PASSWORD  = models.CharField(max_length=500,null=True,verbose_name="Password")
    utc = [
        ("superadmin","Superadmin"),
        ("admin","Admin"),
        ("bm","Branch Manager"),
        ("rm","Relationship Manager"),
        ("ep","Easy Partner"),
        ("bo","Back Office"),
    ]
    USER_TYPE = models.CharField(max_length=150,choices=utc)

    OWNER = models.BooleanField(default=False)

    # # below fields is used for role based permission of admin,bm,rm,ep
    # ALLOWED_MODULES = models.CharField(max_length=500,null=True,blank=True)
    # HIDDEN_MODULES = models.CharField(max_length=500,null=True,blank=True)

    IS_DELETED   = models.BooleanField(default=False)
    CREATED_DATE = models.DateTimeField(auto_now_add=True,null=True)
    UPDATED_DATE = models.DateTimeField(auto_now=True)
    CREATED_BY = models.ForeignKey("crm.User",blank=True,null=True, on_delete=models.CASCADE,verbose_name="created_by", related_name='user_created_by')
    MODIFIED_BY = models.ForeignKey("crm.User",blank=True,null=True, on_delete=models.CASCADE,verbose_name="modified_by", related_name='user_modified_by')
    
    class Meta:
        verbose_name = 'User Details'
        verbose_name_plural = 'User Details'
    
    def clean(self):
        if User.objects.exclude(id=self.id).filter(USERNAME=self.USERNAME).exists():
            raise ValidationError('This Username Name is already exists. Please Enter New user')

    def save(self, *args, **kwargs):
        if User.objects.filter(USERNAME=self.USERNAME).exists():
            a = User.objects.get(USERNAME = self.USERNAME)
            if a.PASSWORD == self.PASSWORD:
                return super().save(*args, **kwargs)
            else:
                self.PASSWORD=make_password(self.PASSWORD)
                return super().save(*args, **kwargs)
        else:
            self.PASSWORD=make_password(self.PASSWORD)
            return super().save(*args, **kwargs)
        
    def __str__(self):
        if self.USER_TYPE == "ep":
            return f"id = {self.id} | Name = {self.NAME} | Pan Number = {self.EP.PAN_NO}"
        else:
            return f"id = {self.id} | Name = {self.NAME} "
        
class LoginLogs(models.Model):
    USER_ID = models.CharField(max_length=16,blank=True,null=True)
    utc = [
            ("superadmin","Superadmin"),
            ("admin","Admin"),
            ("bm","BM"),
            ("rm","Relationship Manager"),
            ("ep","Easy Partner"),
        ]
    USER_TYPE = models.CharField(max_length=150,choices=utc)
    # USER_TYPE = models.CharField(max_length=16,blank=True,null=True)
    LOGIN_DATETIME = models.DateTimeField(null=True,blank=True)
    LOGOUT_DATETIME = models.DateTimeField(null=True,blank=True)
    LOGIN_SESSION = models.TextField(blank=True,null=True)
    IP_ADDRESS =models.CharField(max_length=16,blank=True,null=True)
    LOGIN_STATUS = models.BooleanField(default=True)

    IS_DELETED = models.BooleanField(default=False,null=True)
    CREATED_DATE = models.DateTimeField(auto_now_add=True,null=True)
    UPDATED_DATE = models.DateTimeField(auto_now=True,null=True)

    class Meta:
        verbose_name_plural="Login Logs"

# master
class Customer_types(models.Model):
    TYPE = models.CharField(max_length=50)

    IS_DELETED = models.BooleanField(default=False)
    CREATED_DATE = models.DateTimeField(auto_now_add=True,null=True)
    UPDATED_DATE = models.DateTimeField(auto_now=True)

    def __str__(self) -> str:
        return f"{self.TYPE}"

class Branch_location_master(models.Model):
    NAME = models.CharField(max_length=500,blank=True,null=True,verbose_name="Branch Name Location")

    IS_DELETED = models.BooleanField(default=False)
    CREATED_DATE = models.DateTimeField(auto_now_add=True,null=True)
    UPDATED_DATE = models.DateTimeField(auto_now=True)
    CREATED_BY = models.ForeignKey("crm.User",blank=True,null=True, on_delete=models.CASCADE,verbose_name="created_by", related_name='branch_location_master_c_by')
    MODIFIED_BY = models.ForeignKey("crm.User",blank=True,null=True, on_delete=models.CASCADE,verbose_name="modified_by", related_name='branch_location_master_m_by')
    
    class Meta:
        verbose_name = 'Branch Location Master'
        verbose_name_plural = 'Branch Location Master'



class Back_Office(models.Model):
    LOGIN = models.ForeignKey("crm.User",blank=True,null=True,on_delete=models.CASCADE ,verbose_name="Login Details", related_name='bo_login')
    CODE = models.CharField(max_length=500,blank=True,null=True,verbose_name="Code")
    NAME = models.CharField(max_length=500,blank=True,null=True,verbose_name="Name")
    ADD1 = models.CharField(max_length=1000,blank=True,null=True,verbose_name="Address 1")
    ADD2 = models.CharField(max_length=1000,blank=True,null=True,verbose_name="Address 2")
    DOB = models.DateField()
    PHONE = models.CharField(max_length=500,blank=True,null=True,verbose_name="Phone Number")
    MOB_NO = models.CharField(max_length=500,blank=True,null=True,verbose_name="Mobile Number")
    EMAIL = models.CharField(max_length=500,blank=True,null=True,verbose_name="Email Id")
    BANK_NAME = models.CharField(max_length=500,blank=True,null=True,verbose_name="Bank Name")
    ACC_NO = models.CharField(max_length=500,blank=True,null=True,verbose_name="Account Number")
    IFSC_CODE = models.CharField(max_length=500,blank=True,null=True,verbose_name="IFSC Code")
    PAN_NO = models.CharField(max_length=500,blank=True,null=True,verbose_name="Pan No")
    AADHAAR_NO = models.CharField(max_length=500,blank=True,null=True,verbose_name="Aadhaar Card No")
    CREATE_LOGIN = models.BooleanField(default=False)

    PAN_IMG                     = models.FileField(upload_to="BO_PAN_IMAGE",max_length=500,blank=True,null=True,verbose_name= "Back Office Pan Image")
    AADHAAR_IMG                 = models.FileField(upload_to="BO_AADHAR_IMAGE",max_length=500,blank=True,null=True,verbose_name="Back Office Aadhar Image")
    RELIEVING_LETTER_IMG        = models.FileField(upload_to="BO_RELIEVING_LETTER_IMG",max_length=500,blank=True,null=True,verbose_name="Back Office Relieving Letter Image")
    CHEQUE_IMG                  = models.FileField(upload_to="BO_CHEQUE_IMG",max_length=500,blank=True,null=True,verbose_name="Back Office Cheque Image")
    EDUCATION_CERIFICATE_IMG    = models.FileField(upload_to="BO_EDUCATION_CERIFICATE_IMG",max_length=500,blank=True,null=True,verbose_name="Back Office Education Certificate Image")

    CREATED_BY = models.ForeignKey("crm.User",blank=True,null=True, on_delete=models.CASCADE,verbose_name="created_by", related_name='bo_c_by')
    MODIFIED_BY = models.ForeignKey("crm.User",blank=True,null=True, on_delete=models.CASCADE,verbose_name="modified_by", related_name='bo_m_by')

    IS_DELETED = models.BooleanField(default=False)
    CREATED_DATE = models.DateTimeField(auto_now_add=True,null=True)
    UPDATED_DATE = models.DateTimeField(auto_now=True)
    
    class Meta:
        verbose_name = 'Back Office Employee Detail'
        verbose_name_plural = 'Back Office Employee Details'

class Branch_Manager(models.Model):
    LOGIN = models.ForeignKey("crm.User",blank=True,null=True,on_delete=models.CASCADE ,verbose_name="Login Details", related_name='bm_login')
    CODE = models.CharField(max_length=500,blank=True,null=True,verbose_name="BM Code")
    NAME = models.CharField(max_length=500,blank=True,null=True,verbose_name="BM Name")
    ADD1 = models.CharField(max_length=1000,blank=True,null=True,verbose_name="BM Address 1")
    ADD2 = models.CharField(max_length=1000,blank=True,null=True,verbose_name="BM Address 2")
    DOB = models.DateField()
    PHONE = models.CharField(max_length=500,blank=True,null=True,verbose_name="BM Phone Number")
    MOB_NO = models.CharField(max_length=500,blank=True,null=True,verbose_name="BM Mobile Number")
    EMAIL = models.CharField(max_length=500,blank=True,null=True,verbose_name="BM Email Id")
    BANK_NAME = models.CharField(max_length=500,blank=True,null=True,verbose_name="BM Bank Name")
    ACC_NO = models.CharField(max_length=500,blank=True,null=True,verbose_name="BM Account Number")
    IFSC_CODE = models.CharField(max_length=500,blank=True,null=True,verbose_name="BM IFSC Code")
    BRANCH_LOC = models.ForeignKey("crm.Branch_location_master",blank=True,null=True, on_delete=models.CASCADE)
    PAN_NO = models.CharField(max_length=500,blank=True,null=True,verbose_name="BM Pan No")
    AADHAAR_NO = models.CharField(max_length=500,blank=True,null=True,verbose_name="BM Aadhaar Card No")
    CREATE_LOGIN = models.BooleanField(default=False)
    CREATED_BY = models.ForeignKey("crm.User",blank=True,null=True, on_delete=models.CASCADE,verbose_name="created_by", related_name='bm_c_by')
    MODIFIED_BY = models.ForeignKey("crm.User",blank=True,null=True, on_delete=models.CASCADE,verbose_name="modified_by", related_name='bm_m_by')

    OWNER = models.BooleanField(default=False)

    IS_DELETED = models.BooleanField(default=False)
    CREATED_DATE = models.DateTimeField(auto_now_add=True,null=True)
    UPDATED_DATE = models.DateTimeField(auto_now=True)
    
    class Meta:
        verbose_name = 'Branch Manager Details'
        verbose_name_plural = 'Branch Manager Details'

    def __str__(self):
        return f"{self.NAME}"

    # def __str__(self):
        # return f"{self.id} - {self.USER.NAME}"

class Relationship_Manager(models.Model):
    LOGIN = models.ForeignKey("crm.User",blank=True,null=True,on_delete=models.CASCADE ,verbose_name="Login Details", related_name='rm_login')
    BRANCH = models.ForeignKey("crm.Branch_Manager",blank=True,null=True, on_delete=models.CASCADE,verbose_name="Branch Manager")
    # USER = models.ForeignKey("crm.Branch_Manager", on_delete=models.CASCADE)
    CODE = models.CharField(max_length=500,blank=True,null=True,verbose_name="Relationship_Manager Code")
    NAME = models.CharField(max_length=500,blank=True,null=True,verbose_name="Relationship_Manager Name")
    ADD1 = models.CharField(max_length=1000,blank=True,null=True,verbose_name="Relationship_Manager Address 1")
    ADD2 = models.CharField(max_length=1000,blank=True,null=True,verbose_name="Relationship_Manager Address 2")
    DOB = models.DateField()
    PHONE = models.CharField(max_length=500,blank=True,null=True,verbose_name="Relationship_Manager Phone Number")
    MOB_NO = models.CharField(max_length=500,blank=True,null=True,verbose_name="Relationship_Manager Mobile Number")
    EMAIL = models.CharField(max_length=500,blank=True,null=True,verbose_name="Relationship_Manager Email Id")
    BANK_NAME = models.CharField(max_length=500,blank=True,null=True,verbose_name="Relationship_Manager Bank Name")
    ACC_NO = models.CharField(max_length=500,blank=True,null=True,verbose_name="Relationship_Manager Account Number")
    IFSC_CODE = models.CharField(max_length=500,blank=True,null=True,verbose_name="Relationship_Manager IFSC Code")
    # BANK = models.ForeignKey("app.Bank_master",blank=True,null=True, on_delete=models.CASCADE,verbose_name="Bank Name")
    PAN_NO = models.CharField(max_length=500,blank=True,null=True,verbose_name="Relationship_Manager Pan No")
    AADHAAR_NO = models.CharField(max_length=500,blank=True,null=True,verbose_name="Relationship_Manager Aadhaar Card No")

    PAN_IMG                     = models.FileField(upload_to="RM_PAN_IMAGE",max_length=500,blank=True,null=True,verbose_name= "Relationship_Manager Pan Image")
    AADHAAR_IMG                 = models.FileField(upload_to="RM_AADHAR_IMAGE",max_length=500,blank=True,null=True,verbose_name="Relationship_Manager Aadhar Image")
    RELIEVING_LETTER_IMG        = models.FileField(upload_to="RM_RELIEVING_LETTER_IMG",max_length=500,blank=True,null=True,verbose_name="Relationship_Manager Relieving Letter Image")
    CHEQUE_IMG                  = models.FileField(upload_to="RM_CHEQUE_IMG",max_length=500,blank=True,null=True,verbose_name="Relationship_Manager Cheque Image")
    EDUCATION_CERIFICATE_IMG    = models.FileField(upload_to="RM_EDUCATION_CERIFICATE_IMG",max_length=500,blank=True,null=True,verbose_name="Relationship_Manager Education Certificate Image")

    CREATE_LOGIN = models.BooleanField(default=False)
    OWNER = models.BooleanField(default=False)

    CREATED_BY = models.ForeignKey("crm.User",blank=True,null=True, on_delete=models.CASCADE,verbose_name="created_by", related_name='rm_c_by')
    MODIFIED_BY = models.ForeignKey("crm.User",blank=True,null=True, on_delete=models.CASCADE,verbose_name="modified_by", related_name='rm_m_by')

    IS_DELETED = models.BooleanField(default=False)
    CREATED_DATE = models.DateTimeField(auto_now_add=True,null=True)
    UPDATED_DATE = models.DateTimeField(auto_now=True)
    
    class Meta:
        verbose_name = 'Relationship Manager Details'
        verbose_name_plural = 'Relationship Manager Details'

class Easy_Partner(models.Model):
    LOGIN               = models.ForeignKey("crm.User",blank=True,null=True,on_delete=models.CASCADE ,verbose_name="Login Details", related_name='ep_login')
    RM                  = models.ForeignKey("crm.Relationship_Manager",blank=True,null=True, on_delete=models.CASCADE,verbose_name="Relationship Manager")
    CODE                = models.CharField(max_length=500,blank=True,null=True,verbose_name="Easy_Partner Code")
    NAME                = models.CharField(max_length=500,blank=True,null=True,verbose_name="Easy_Partner Name")
    ADD1                = models.CharField(max_length=1000,blank=True,null=True,verbose_name="Easy_Partner Address 1")
    ADD2                = models.CharField(max_length=1000,blank=True,null=True,verbose_name="Easy_Partner Address 2")
    DOB                 = models.DateField(null=True)
    PHONE               = models.CharField(max_length=500,blank=True,null=True,verbose_name="Easy_Partner Phone Number")
    MOB_NO              = models.CharField(max_length=500,blank=True,null=True,verbose_name="Easy_Partner Mobile Number")
    EMAIL               = models.CharField(max_length=500,blank=True,null=True,verbose_name="Easy_Partner Email Id")

    PAN_NO              = models.CharField(max_length=500,blank=True,null=True,verbose_name="Easy_Partner Pan No")
    AADHAAR_NO          = models.CharField(max_length=500,blank=True,null=True,verbose_name="Easy_Partner Aadhaar Card No")

    PAN_IMG             = models.FileField(upload_to="EP_PAN_IMAGE",max_length=500,blank=True,null=True,verbose_name= "Easy_Partner Pan Image")
    AADHAAR_IMG         = models.FileField(upload_to="EP_AADHAR_IMAGE",max_length=500,blank=True,null=True,verbose_name="Easy_Partner Aadhaar Aadhar Image")
    CHEQUE_IMG          = models.FileField(upload_to="EP_CHEQUE_IMAGE",max_length=500,blank=True,null=True,verbose_name="Easy_Partner Aadhaar Cheque Image")
    NOMINEE_IMG         = models.FileField(upload_to="EP_NOMINEE_IMAGE",max_length=500,blank=True,null=True,verbose_name="Easy_Partner Nominee Image")
    
    BANK_NAME           = models.CharField(max_length=500,blank=True,null=True,verbose_name="Easy_Partner Bank Name")
    ACC_NO              = models.CharField(max_length=500,blank=True,null=True,verbose_name="Relationship_Manager Account Number")
    IFSC_CODE           = models.CharField(max_length=500,blank=True,null=True,verbose_name="Easy_Partner IFSC Code")
    NOMINEE_NAME        = models.CharField(max_length=500,blank=True,null=True,verbose_name="Easy_Partner Nominee Name")
    CHEQUE_NO           = models.CharField(max_length=500,blank=True,null=True,verbose_name="Easy_Partner Cheque No")

    # BANK = models.ForeignKey("app.Bank_master",blank=True,null=True, on_delete=models.CASCADE,verbose_name="Bank Name")
    
    MF_C_P              = models.CharField(max_length=500,blank=True,null=True,verbose_name="Mutual Fund Commission Percentage")

    CREATE_LOGIN        = models.BooleanField(default=False)

    CREATED_BY          = models.ForeignKey("crm.User",blank=True,null=True, on_delete=models.CASCADE,verbose_name="created_by", related_name='ep_c_by')
    MODIFIED_BY         = models.ForeignKey("crm.User",blank=True,null=True, on_delete=models.CASCADE,verbose_name="modified_by", related_name='ep_m_by')

    IS_DELETED          = models.BooleanField(default=False)
    CREATED_DATE        = models.DateTimeField(auto_now_add=True,null=True)
    UPDATED_DATE        = models.DateTimeField(auto_now=True)
    
    class Meta:
        verbose_name = 'Easy Partner Details'
        verbose_name_plural = 'Easy Partner Details'

    def __str__(self):
        return f"id = {self.id} | Name = {self.NAME} | Pan Number = {self.PAN_NO}"
        # NAME User

# class Easy_Partner(models.Model):
    
#     DOB = models.DateField()
#     # USER = models.ForeignKey("app.Branch_Manager", on_delete=models.CASCADE)
#     BM_NAME = models.ForeignKey("crm.Branch_Manager", on_delete=models.CASCADE)
#     AMC_NAME = models.CharField(max_length=500,blank=True,null=True,verbose_name="BM AMC_NAME")
#     TRAIL = models.CharField(max_length=1000,blank=True,null=True,verbose_name="BM Trai")

#     IS_DELETED = models.BooleanField(default=False)
#     CREATED_DATE = models.DateTimeField(auto_now_add=True,null=True)
#     UPDATED_DATE = models.DateTimeField(auto_now=True)
    
#     class Meta:
#         verbose_name = 'Add BM Brokerage'
#         verbose_name_plural = 'Add BM Brokerage'

class BM_Brokerage(models.Model):
    DOB = models.DateField()
    BM_NAME = models.ForeignKey("crm.Branch_Manager", on_delete=models.CASCADE)
    AMC_NAME = models.CharField(max_length=500,blank=True,null=True,verbose_name="BM AMC_NAME")
    TRAIL = models.CharField(max_length=1000,blank=True,null=True,verbose_name="BM Trail")

    CREATED_BY = models.ForeignKey("crm.User",blank=True,null=True, on_delete=models.CASCADE,verbose_name="created_by", related_name='bm_br_c_by')
    MODIFIED_BY = models.ForeignKey("crm.User",blank=True,null=True, on_delete=models.CASCADE,verbose_name="modified_by", related_name='bm_br_m_by')

    IS_DELETED = models.BooleanField(default=False)
    CREATED_DATE = models.DateTimeField(auto_now_add=True,null=True)
    UPDATED_DATE = models.DateTimeField(auto_now=True)
    
    class Meta:
        verbose_name = 'Branch Manager Brokerage'
        verbose_name_plural = 'Branch Manager Brokerage'

class RM_Brokerage(models.Model):
    DOB = models.DateField()
    RM_NAME = models.ForeignKey("crm.Relationship_Manager", on_delete=models.CASCADE)
    AMC_NAME = models.CharField(max_length=500,blank=True,null=True,verbose_name="Relationship Manager AMC NAME")
    TRAIL = models.CharField(max_length=1000,blank=True,null=True,verbose_name="Relationship Manager Trail")

    CREATED_BY = models.ForeignKey("crm.User",blank=True,null=True, on_delete=models.CASCADE,verbose_name="created_by", related_name='rm_br_c_by')
    MODIFIED_BY = models.ForeignKey("crm.User",blank=True,null=True, on_delete=models.CASCADE,verbose_name="modified_by", related_name='rm_br_m_by')

    IS_DELETED = models.BooleanField(default=False)
    CREATED_DATE = models.DateTimeField(auto_now_add=True,null=True)
    UPDATED_DATE = models.DateTimeField(auto_now=True)
    
    class Meta:
        verbose_name = 'Relationship Manager Brokerage'
        verbose_name_plural = 'Relationship Manager Brokerage'

class Easy_Partner_Brokerage(models.Model):
    EFFECTIVE_DATE = models.DateField()
    # USER = models.ForeignKey("crm.Branch_Manager", on_delete=models.CASCADE)
    PARTNER_NAME = models.ForeignKey("crm.Easy_Partner", on_delete=models.CASCADE,blank=True,null=True)
    AMC_NAME = models.CharField(max_length=500,blank=True,null=True,verbose_name="Sub Broker AMC NAME")
    TRAIL = models.CharField(max_length=1000,blank=True,null=True,verbose_name="Sub Broker Trai")
    ADD_INCENTIVE = models.CharField(max_length=1000,blank=True,null=True,verbose_name="Sub Broker Trai")
    TYPE = models.CharField(max_length=1000,blank=True,null=True,verbose_name="Sub Brokerage Type")
    NOTE = models.CharField(max_length=1000,blank=True,null=True,verbose_name="Sub Broker Trai")

    CREATED_BY = models.ForeignKey("crm.User",blank=True,null=True, on_delete=models.CASCADE,verbose_name="created_by", related_name='ep_br_c_by')
    MODIFIED_BY = models.ForeignKey("crm.User",blank=True,null=True, on_delete=models.CASCADE,verbose_name="modified_by", related_name='ep_br_m_by')

    IS_DELETED = models.BooleanField(default=False)
    CREATED_DATE = models.DateTimeField(auto_now_add=True,null=True)
    UPDATED_DATE = models.DateTimeField(auto_now=True)
    
    class Meta:
        verbose_name = 'Easy Partner Brokerage'
        verbose_name_plural = 'Easy Partner Brokerage'

class Insurance_master(models.Model):
    INSURER = models.CharField(max_length=500,blank=True,null=True,verbose_name="Insurer")
    PRODUCT = models.CharField(max_length=500,blank=True,null=True,verbose_name="Product")
    # plan_type = [
    #     ("rm","Relationship Manager"),
    #     ("ep","Easy Partner"),
    # ]
    PLAN_TYPE = models.CharField(max_length=150,blank=True,null=True,verbose_name="Plan Type")
    PPT = models.CharField(max_length=500,blank=True,null=True,verbose_name="ppt")
    PT = models.CharField(max_length=500,blank=True,null=True,verbose_name="pt")
    PB_G_OFF = models.CharField(max_length=500,blank=True,null=True,verbose_name="Pb Grind Offline")
    PB_G_OFF_PERCENT = models.CharField(max_length=500,blank=True,null=True,verbose_name="Pb Grind Offline percentage")
    PB_RENEW_OFF = models.CharField(max_length=500,blank=True,null=True,verbose_name="PB Grid Renewal")
    PB_RENEW_OFF_PERCENT = models.CharField(max_length=500,blank=True,null=True,verbose_name="PB Grid Renewal Percentage")
    PB_GRID_ON = models.CharField(max_length=500,blank=True,null=True,verbose_name="PB Grid Online ")
    PB_GRID_ON_PERCENT = models.CharField(max_length=500,blank=True,null=True,verbose_name="PB Grid Online Percentage")

    CREATED_BY = models.ForeignKey("crm.User",blank=True,null=True, on_delete=models.CASCADE,verbose_name="created_by", related_name='im_c_by')
    MODIFIED_BY = models.ForeignKey("crm.User",blank=True,null=True, on_delete=models.CASCADE,verbose_name="modified_by", related_name='im_m_by')
    C_DATE = models.DateField(auto_now_add=True,null=True)

    IS_DELETED = models.BooleanField(default=False)
    CREATED_DATE = models.DateTimeField(auto_now_add=True,null=True)
    UPDATED_DATE = models.DateTimeField(auto_now=True)
    
    class Meta:
        verbose_name = 'Insurance Master'
        verbose_name_plural = 'Insurance Master'


class UploadInsuranceMaster(models.Model):
    EXCEL = models.FileField(upload_to="insurance_Master",max_length=500,blank=True,null=True,verbose_name= "Upload Insurance Master")
    # SHEET_NAME = models.CharField(max_length=100,null=True,verbose_name="Sheet Name")
    
    IS_DELETED=models.BooleanField(default=False,null=True)
    CREATED_DATE = models.DateTimeField(auto_now_add=True,null=True)
    UPDATED_DATE = models.DateTimeField(auto_now=True,null=True)

    def delete(self,*args,**kwargs):
        logger.info(f"delete PAth = {self.EXCEL.path}")
        logger.info(f"Enter delete")
        if os.path.isfile(self.EXCEL.path):
            os.remove(self.EXCEL.path)
        super(UploadInsuranceMaster, self).delete(*args,**kwargs)
    class Meta:
        verbose_name_plural = "Upload Insurance Master"

class UploadMFMaster(models.Model):
    EXCEL = models.FileField(upload_to="insurance_MF_Master",max_length=500,blank=True,null=True,verbose_name= "Upload Insurance MF Master")
    # SHEET_NAME = models.CharField(max_length=100,null=True,verbose_name="Sheet Name")
    
    IS_DELETED=models.BooleanField(default=False,null=True)
    CREATED_DATE = models.DateTimeField(auto_now_add=True,null=True)
    UPDATED_DATE = models.DateTimeField(auto_now=True,null=True)

    def delete(self,*args,**kwargs):
        logger.info(f"delete PAth = {self.EXCEL.path}")
        logger.info(f"Enter delete")
        if os.path.isfile(self.EXCEL.path):
            os.remove(self.EXCEL.path)
        super(UploadMFMaster, self).delete(*args,**kwargs)
    class Meta:
        verbose_name_plural = "Upload MF Master"

class MF_master(models.Model):
    SCHEME = models.CharField(max_length=500,blank=True,null=True,verbose_name="Scheme Name")
    E_C_P = models.CharField(max_length=500,blank=True,null=True,verbose_name="Easy Company Payout")
    # plan_type = [
    #     ("rm","Relationship Manager"),
    #     ("ep","Easy Partner"),
    # ]
    NET_A_GST = models.CharField(max_length=150,blank=True,null=True,verbose_name="Net After GST")
    EP_PAYOUT = models.CharField(max_length=500,blank=True,null=True,verbose_name="Easy Partner Payout")

    CREATED_BY = models.ForeignKey("crm.User",blank=True,null=True, on_delete=models.CASCADE,verbose_name="created_by", related_name='mfm_c_by')
    MODIFIED_BY = models.ForeignKey("crm.User",blank=True,null=True, on_delete=models.CASCADE,verbose_name="modified_by", related_name='mfm_m_by')
    C_DATE = models.DateField(auto_now_add=True,null=True)

    IS_DELETED = models.BooleanField(default=False)
    CREATED_DATE = models.DateTimeField(auto_now_add=True,null=True)
    UPDATED_DATE = models.DateTimeField(auto_now=True)
    
    class Meta:
        verbose_name = 'Mutual Fund Master'
        verbose_name_plural = 'Mutual Fund Master'


class Insurance_type_master(models.Model):
    NAME = models.CharField(max_length=500,blank=True,null=True,verbose_name="Insurance Name Location")

    IS_DELETED = models.BooleanField(default=False)
    CREATED_DATE = models.DateTimeField(auto_now_add=True,null=True)
    UPDATED_DATE = models.DateTimeField(auto_now=True)

    CREATED_BY = models.ForeignKey("crm.User",blank=True,null=True, on_delete=models.CASCADE,verbose_name="created_by", related_name='itm_c_by')
    MODIFIED_BY = models.ForeignKey("crm.User",blank=True,null=True, on_delete=models.CASCADE,verbose_name="modified_by", related_name='itm_m_by')
    
    # def save(self, *args, **kwargs):
    #     if not self.id:
    #         logger.info(f" request.session['LOGIN_ID'] = {request.session['LOGIN_ID']}")
    #         self.created_by = User.objects.get(id= request.session['LOGIN_ID'])
    #         super(Insurance_Customer_Master, self).save(*args, **kwargs)
    #     else:
    #         self.modified_by = User.objects.get(id= request.session['LOGIN_ID'])
    #         super(Insurance_Customer_Master, self).save(*args, **kwargs)

    class Meta:
        verbose_name = 'Insurace Type Master'
        verbose_name_plural = 'Insurace Type Master'

class Customer(models.Model):
    RM_EP               = models.ForeignKey("crm.User",blank=True,null=True, on_delete=models.CASCADE,verbose_name="Customer Under this user",related_name='user_customer')
    BM                  = models.ForeignKey("crm.Branch_Manager",blank=True,null=True, on_delete=models.CASCADE,verbose_name="Branch Manager")
    RM                  = models.ForeignKey("crm.Relationship_Manager",blank=True,null=True, on_delete=models.CASCADE,verbose_name="Relationship Manager")
    EP                  = models.ForeignKey("crm.Easy_Partner",blank=True,null=True, on_delete=models.CASCADE,verbose_name="Easy Partner")
    utc                 = [
                            ("bm","Branch Manager"),
                            ("rm","Relationship Manager"),
                            ("ep","Easy Partner"),
                        ]
    TYPE                = models.CharField(max_length=150,blank=True,null=True,choices=utc)
    PAN_NO              = models.CharField(max_length=500,blank=True,null=True,verbose_name="Pan Card")
    AADHAAR_NO          = models.CharField(max_length=500,blank=True,null=True,verbose_name="Aadhaar Card No")
    C_NAME              = models.CharField(max_length=500,blank=True,null=True,verbose_name="Customer Name")
    M_NAME              = models.CharField(max_length=500,blank=True,null=True,verbose_name="Mother Name")
    F_NAME              = models.CharField(max_length=500,blank=True,null=True,verbose_name="Father Number")
    CUST_DOB            = models.DateField(blank=True,null=True,verbose_name="Customer DOB")
    QUALIFICATION       = models.CharField(max_length=500,blank=True,null=True,verbose_name="QUALIFICATION")
    MOB_NO              = models.CharField(max_length=500,blank=True,null=True,verbose_name="Mobile Number")
    COMP_NAME           = models.CharField(max_length=500,blank=True,null=True,verbose_name="Company Name")
    INDUSTRY_TYPE       = models.CharField(max_length=500,blank=True,null=True,verbose_name="Industry Type")
    ANNUAL_CTC          = models.CharField(max_length=500,blank=True,null=True,verbose_name="Annual Ctc")
    HEIGHT              = models.CharField(max_length=500,blank=True,null=True,verbose_name="Height")
    WEIGHT              = models.CharField(max_length=500,blank=True,null=True,verbose_name="Weight")
    EMAIL               = models.CharField(max_length=500,blank=True,null=True,verbose_name="Email")
    TOBACCO_USER        = models.BooleanField(default=False,verbose_name="Tobacco User")
    TOBACCO_QTY         = models.CharField(max_length=500,blank=True,null=True,verbose_name="Tobacco Qty")
    TOBACCO_CONSUME     = models.CharField(max_length=500,blank=True,null=True,verbose_name="Tobacco Consume")
    ALCOHOL_USER        = models.BooleanField(default=False,verbose_name="Alcohol User")
    ALCOHOL_QTY         = models.CharField(max_length=500,blank=True,null=True,verbose_name="Alcohol Qty")
    ALCOHOL_CONSUME     = models.CharField(max_length=500,blank=True,null=True,verbose_name="Alcohol Consume")
    MEDICAL_HISTORY     = models.BooleanField(default=False,verbose_name="Medical History Available")
    MEDICAL_DTL         = models.CharField(max_length=500,blank=True,null=True,verbose_name="Medical Details")
    OLD_COMP_NAME       = models.CharField(max_length=500,blank=True,null=True,verbose_name="Old Company Name")
    SUM_ASSURED         = models.CharField(max_length=500,blank=True,null=True,verbose_name="Sum Assured")
    NOMINEE_NAME        = models.CharField(max_length=500,blank=True,null=True,verbose_name="Nominee Name")
    NOMINEE_DOB         = models.DateField(blank=True,null=True,verbose_name="Nominee DOB")
    RELATIONSHIP        = models.CharField(max_length=500,blank=True,null=True,verbose_name="Relationship")
    MARITAL_STATUS      = models.CharField(max_length=500,blank=True,null=True,verbose_name="Marital status")
    VACCINATION_IMG     = models.FileField(upload_to="Vaccination Image",blank=True,null=True,verbose_name="Vaccination img")
    PAN_IMG             = models.FileField(upload_to="Insurance Pan Image",blank=True,null=True,verbose_name="Pan img")
    AADHAR_IMG          = models.FileField(upload_to="Insurance Adharcard Image",blank=True,null=True,verbose_name="Aadhar Card img")
    CC_IMG              = models.FileField(upload_to="Cancel Cheque Image",blank=True,null=True,verbose_name="Cancel Cheque img")
    PROFILE_IMG         = models.FileField(upload_to="Profile Image",blank=True,null=True,verbose_name="Profile Img")
    LAST_EDU            = models.FileField(upload_to="Last Education Image",blank=True,null=True,verbose_name="Last Education Certificate")
    SALARYSLIP_IMG      = models.FileField(upload_to="Salaryslip Image",blank=True,null=True,verbose_name="Salaryslip Img")
    # newly added after 7 july client meeting
    COMBINE_DOC         = models.FileField(upload_to="Combine Documents",blank=True,null=True,verbose_name="Combine Documents")
    CUSTOMER_TYPES      = models.CharField(max_length=500,null=True)

    IS_DELETED          = models.BooleanField(default=False)
    CREATED_DATE        = models.DateTimeField(auto_now_add=True,null=True)
    UPDATED_DATE        = models.DateTimeField(auto_now=True)

    CREATED_BY          = models.ForeignKey("crm.User",blank=True,null=True, on_delete=models.CASCADE,verbose_name="created_by", related_name='icm_c_by')
    MODIFIED_BY         = models.ForeignKey("crm.User",blank=True,null=True, on_delete=models.CASCADE,verbose_name="modified_by", related_name='icm_m_by')
    
    class Meta:
        verbose_name = 'Customer'
        verbose_name_plural = 'Customer'

class INSURANCE_PPT_YEAR(models.Model):
    INSURANCE_ID = models.BigIntegerField(blank=True,null=True,verbose_name="insurance id")
    YEAR = models.CharField(max_length=1,blank=True,null=True,verbose_name="ppt year")
    CREATED_DATE = models.DateField(auto_now_add=True,null=True)
    UPDATED_DATE = models.DateField(auto_now_add=True,null=True)
    IS_DELETED   = models.BooleanField(default=False)
    PPT_AMOUNT          = models.CharField(max_length=500,blank=True,null=True,verbose_name="ppt ammount")

    class Meta:
        verbose_name = 'Customer'
        verbose_name_plural = 'Customer'

class New_Insurance(models.Model):
    TYPE_INSURANCE   = models.CharField(max_length=1,blank=True,null=True,verbose_name="insurance type")

    NUMBER_OF_INSURED = models.CharField(max_length=1,blank=True,null=True,verbose_name="Number of insured")
    LIFE_TO_INSURED_ONE = models.CharField(max_length=1,blank=True,null=True,verbose_name="Life to insured one")
    LIFE_TO_INSURED_DOB_ONE = models.DateField(max_length=1,blank=True,null=True,verbose_name="Life to insured dob one")
    LIFE_TO_INSURED_TWO = models.CharField(max_length=1,blank=True,null=True,verbose_name="Life to insured two")
    LIFE_TO_INSURED_DOB_TWO = models.DateField(max_length=1,blank=True,null=True,verbose_name="Life to insured dob two")
    LIFE_TO_INSURED_THREE = models.CharField(max_length=1,blank=True,null=True,verbose_name="Life to insured three")
    LIFE_TO_INSURED_DOB_THREE = models.DateField(max_length=1,blank=True,null=True,verbose_name="Life to insured dob three")
    LIFE_TO_INSURED_FOUR = models.CharField(max_length=1,blank=True,null=True,verbose_name="Life to insured four")
    LIFE_TO_INSURED_DOB_FOUR = models.DateField(max_length=1,blank=True,null=True,verbose_name="Life to insured dob four")
    POLICY_BROKER = models.CharField(max_length=1,blank=True,null=True,verbose_name="Policy broker")
    PRODUCT_ISSUANCE_DATE = models.DateField(blank=True,null=True,verbose_name="Product issuance date")

    INSURANCE_COMPANY_NAME   = models.CharField(max_length=500,blank=True,null=True,verbose_name="Insurance Name")
    INSURANCE_NAME   = models.CharField(max_length=500,blank=True,null=True,verbose_name="Insurance Name")
    INSURANCE_PERIOD = models.CharField(max_length=500,blank=True,null=True,verbose_name="Insurance Period")

    POLICY_FIRST_INCEPTION_DATE = models.DateField(blank=True,null=True,verbose_name="Policy first inception Date")

    VEHICLE_REGISTRATION_NUMBER = models.CharField(max_length=500,blank=True,null=True,verbose_name="Vehicle Regisration number")
    VEHICLE_TYPE = models.CharField(max_length=500,blank=True,null=True,verbose_name="Vehicle type")
    CHASIS_NUMBER = models.CharField(max_length=500,blank=True,null=True,verbose_name="Vehicle chasis number")
    IDV_VALUE = models.CharField(max_length=500,blank=True,null=True,verbose_name="Vehicle idv value")
    VEHICLE_MODEL = models.CharField(max_length=500,blank=True,null=True,verbose_name="Vehicle model")

    TRAVEL_DATE = models.DateField(blank=True,null=True,verbose_name="Travel Date")
    TRAVEL_LOCATION = models.CharField(max_length=500,blank=True,null=True,verbose_name="TRAVEL LOCATION")
    TRAVEL_PRODUCT = models.CharField(max_length=500,blank=True,null=True,verbose_name="TRAVEL PRODUCT")

    PRODUCT = models.CharField(max_length=500,blank=True,null=True,verbose_name="Product")
    MODE = models.CharField(max_length=500,blank=True,null=True,verbose_name="mode")
    SUB_MODE = models.CharField(max_length=500,blank=True,null=True,verbose_name="Sub mode")

    START_DATE       = models.DateField(blank=True,null=True,verbose_name="Start Date")

    MATURITY_DATE    =  models.DateField(blank=True,null=True,verbose_name="MATURITY Date")

    SUM_ASSURED      = models.CharField(max_length=500,blank=True,null=True,verbose_name="Vehicle model")
    POLICY_NUMBER    = models.CharField(max_length=500,blank=True,null=True,verbose_name="Policy number")

    RENEWAL_DATE     = models.DateField(blank=True,null=True,verbose_name="Renewal Date")
    PPT              = models.CharField(max_length=500,blank=True,null=True,verbose_name="Premium Payment Term")
    PT               = models.CharField(max_length=500,blank=True,null=True,verbose_name="Policy Term")
    PB               = models.CharField(max_length=500,blank=True,null=True,verbose_name="Policy Broker")
    NET_AMT          = models.CharField(max_length=500,blank=True,null=True,verbose_name="Net Amount")
    GROSS_AMT        = models.CharField(max_length=500,blank=True,null=True,verbose_name="Gross Amount")
    COMMISSION       = models.CharField(max_length=500,blank=True,null=True,verbose_name="Commission Percentage")
    COMMISSION_AMT   = models.CharField(max_length=500,blank=True,null=True,verbose_name="Commission Amount")
    TABLE_NAME       = models.CharField(max_length=50,blank=True,null=True,verbose_name="table name")
    CUSTOMER_id      = models.CharField(max_length=500,blank=True,null=True,verbose_name="Customer id")
    IS_DELETED       = models.BooleanField(default=False)
    CREATED_DATE     = models.DateField(auto_now_add=True,null=True)
    UPDATED_DATE     = models.DateField(auto_now=True)                  

    # CREATED_BY = models.ForeignKey("crm.User",blank=True,null=True, on_delete=models.CASCADE,verbose_name="new_created_by", related_name='new_i_c_by')
    # MODIFIED_BY = models.ForeignKey("crm.User",blank=True,null=True, on_delete=models.CASCADE,verbose_name="new_i_m_by", related_name='_new_insurance_modified_by')

    class Meta:
        verbose_name = 'New Insurance Alert'
        verbose_name_plural = 'New Insurance Alert'

class Insurance(models.Model):
    CUSTOMER         = models.ForeignKey("crm.Customer", on_delete=models.CASCADE,blank=True,null=True)
    TYPE_INSURANCE   = models.ForeignKey("crm.Insurance_type_master", on_delete=models.CASCADE,blank=True,null=True)
    INSURANCE_NAME   = models.CharField(max_length=500,blank=True,null=True,verbose_name="Insurance Name")
    INSURANCE_PERIOD = models.CharField(max_length=500,blank=True,null=True,verbose_name="Insurance Period")
    START_DATE       = models.DateField(blank=True,null=True,verbose_name="Start Date")
    RENEWAL_DATE     = models.DateField(blank=True,null=True,verbose_name="Renewal Date")
    PPT              = models.CharField(max_length=500,blank=True,null=True,verbose_name="Premium Payment Term")
    PT               = models.CharField(max_length=500,blank=True,null=True,verbose_name="Policy Term")
    PB               = models.ForeignKey("crm.Policy_broker_master",on_delete=models.CASCADE ,blank =True,null=True)
    NET_AMT          = models.CharField(max_length=500,blank=True,null=True,verbose_name="Net Amount")
    GROSS_AMT        = models.CharField(max_length=500,blank=True,null=True,verbose_name="Gross Amount")
    COMMISSION       = models.CharField(max_length=500,blank=True,null=True,verbose_name="Commission Percentage")
    COMMISSION_AMT   = models.CharField(max_length=500,blank=True,null=True,verbose_name="Commission Amount")
    TABLE_NAME       = models.CharField(max_length=50,default="insurance")

    IS_DELETED       = models.BooleanField(default=False)
    CREATED_DATE     = models.DateTimeField(auto_now_add=True,null=True)
    UPDATED_DATE     = models.DateTimeField(auto_now=True)

    CREATED_BY = models.ForeignKey("crm.User",blank=True,null=True, on_delete=models.CASCADE,verbose_name="created_by", related_name='i_c_by')
    MODIFIED_BY = models.ForeignKey("crm.User",blank=True,null=True, on_delete=models.CASCADE,verbose_name="i_m_by", related_name='insurance_modified_by')

    class Meta:
        verbose_name = 'Insurance Alert'
        verbose_name_plural = 'Insurance Alert'

class Update_insurance_alert(models.Model):
    INSURACE         = models.ForeignKey("crm.Insurance", on_delete=models.CASCADE,blank=True,null=True,verbose_name="Insurance Details")
    INSURANCE_PERIOD = models.CharField(max_length=500,blank=True,null=True,verbose_name="Insurance Period")
    START_DATE       = models.DateField(blank=True,null=True,verbose_name="Start Date")
    RENEWAL_DATE     = models.DateField(blank=True,null=True,verbose_name="Renewal Date")

    IS_DELETED       = models.BooleanField(default=False)
    CREATED_DATE     = models.DateTimeField(auto_now_add=True,null=True)
    UPDATED_DATE     = models.DateTimeField(auto_now=True)
    
    class Meta:
        verbose_name = 'Old Insurance Alert'
        verbose_name_plural = 'Old Insurance Alert'


class Attendance_user(models.Model):
    USER         = models.ForeignKey("crm.User", on_delete=models.CASCADE,blank=True,null=True)
    DATE         = models.DateField(blank=True,null=True)
    PUNCH_IN     = models.TimeField(blank=True,null=True)
    PUNCH_OUT    = models.TimeField(blank=True,null=True)
    REMARK       = models.CharField(max_length=500,null=True,blank=True)

    IS_DELETED   = models.BooleanField(default=False)
    CREATED_DATE = models.DateTimeField(auto_now_add=True,null=True)
    UPDATED_DATE = models.DateTimeField(auto_now=True)

    CREATED_BY = models.ForeignKey("crm.User",blank=True,null=True, on_delete=models.CASCADE,verbose_name="created_by", related_name='attendace_created_by')
    MODIFIED_BY = models.ForeignKey("crm.User",blank=True,null=True, on_delete=models.CASCADE,verbose_name="modified_by", related_name='attendace_modified_by')
    
    class Meta:
        verbose_name = 'Attendance'
        verbose_name_plural = 'Attendance'


class Leads(models.Model):
    RM_EP = models.ForeignKey("crm.User",blank=True,null=True, on_delete=models.CASCADE,verbose_name="Customer Under this user",related_name='user_lead')
    BM = models.ForeignKey("crm.Branch_Manager",blank=True,null=True, on_delete=models.CASCADE,verbose_name="Branch Manager")
    RM = models.ForeignKey("crm.Relationship_Manager",blank=True,null=True, on_delete=models.CASCADE,verbose_name="Relationship Manager")
    EP = models.ForeignKey("crm.Easy_Partner",blank=True,null=True, on_delete=models.CASCADE,verbose_name="Easy Partner")
    utc = [
            ("bm","Branch Manager"),
            ("rm","Relationship Manager"),
            ("ep","Easy Partner"),
        ]
    PAN_NO = models.CharField(max_length=500,blank=True,null=True,verbose_name="Pan Card")
    # AADHAAR_NO = models.CharField(max_length=500,blank=True,null=True,verbose_name="Aadhaar Card No")
    LEAD_TYPE = models.CharField(max_length=150,blank=True,null=True,choices=utc)
    REQUIRE = models.CharField(max_length=500,blank=True,null=True,verbose_name="Requirements")
    C_NAME = models.CharField(max_length=500,blank=True,null=True,verbose_name="Customer Name")
    M_NAME = models.CharField(max_length=500,blank=True,null=True,verbose_name="Mother Name")
    F_NAME = models.CharField(max_length=500,blank=True,null=True,verbose_name="Father Number")
    CUST_DOB = models.DateField(blank=True,null=True,verbose_name="Customer DOB")
    QUALIFICATION = models.CharField(max_length=500,blank=True,null=True,verbose_name="QUALIFICATION")
    MOB_NO = models.CharField(max_length=500,blank=True,null=True,verbose_name="Mobile Number")
    ANNUAL_CTC = models.CharField(max_length=500,blank=True,null=True,verbose_name="Annual Ctc")
    EMAIL = models.CharField(max_length=500,blank=True,null=True,verbose_name="Email")
    MARITAL_STATUS = models.CharField(max_length=500,blank=True,null=True,verbose_name="Marital status")
    TOBACCO_USER = models.BooleanField(default=False,verbose_name="Tobacco User")
    TOBACCO_QTY = models.CharField(max_length=500,blank=True,null=True,verbose_name="Tobacco Qty")
    TOBACCO_CONSUME = models.CharField(max_length=500,blank=True,null=True,verbose_name="Tobacco Consume")
    ALCOHOL_USER = models.BooleanField(default=False,verbose_name="Alcohol User")
    ALCOHOL_QTY = models.CharField(max_length=500,blank=True,null=True,verbose_name="Alcohol Qty")
    ALCOHOL_CONSUME = models.CharField(max_length=500,blank=True,null=True,verbose_name="Alcohol Consume")
    MEDICAL_HISTORY = models.BooleanField(default=False,verbose_name="Medical History Available")
    MEDICAL_DTL = models.CharField(max_length=500,blank=True,null=True,verbose_name="Medical Details")

    IS_DELETED = models.BooleanField(default=False)
    CREATED_DATE = models.DateTimeField(auto_now_add=True,null=True)
    UPDATED_DATE = models.DateTimeField(auto_now=True)

    CREATED_BY = models.ForeignKey("crm.User",blank=True,null=True, on_delete=models.CASCADE,verbose_name="created_by", related_name='lead_created_by')
    MODIFIED_BY = models.ForeignKey("crm.User",blank=True,null=True, on_delete=models.CASCADE,verbose_name="modified_by", related_name='lead_modified_by')
    
    class Meta:
        verbose_name = 'Leads'
        verbose_name_plural = 'Leads'

class Followups(models.Model):
    RM_EP = models.ForeignKey("crm.User",blank=True,null=True, on_delete=models.CASCADE,verbose_name="Customer Under this user",related_name='user_followups')
    # BM = models.ForeignKey("crm.Branch_Manager",blank=True,null=True, on_delete=models.CASCADE,verbose_name="Branch Manager")
    utc = [
        ("bm","Branch Manager"),
        ("rm","Relationship Manager"),
        ("ep","Easy Partner"),
    ]
    TYPE = models.CharField(max_length=150,blank=True,null=True,choices=utc)

    LEADS  = models.ForeignKey("crm.Leads",blank=True,null=True, on_delete=models.CASCADE,verbose_name="Relationship Manager")
    DATE   = models.DateField(blank=True,null=True,verbose_name="Follow up date")
    TIME   = models.TimeField(blank=True,null=True,verbose_name="Follow up time")
    REMARK = models.CharField(max_length=500,blank=True,null=True,verbose_name="Follow Remark")

    IS_DELETED = models.BooleanField(default=False)
    CREATED_DATE = models.DateTimeField(auto_now_add=True,null=True)
    UPDATED_DATE = models.DateTimeField(auto_now=True)

    CREATED_BY = models.ForeignKey("crm.User",blank=True,null=True, on_delete=models.CASCADE,verbose_name="created_by", related_name='followup_created_by')
    MODIFIED_BY = models.ForeignKey("crm.User",blank=True,null=True, on_delete=models.CASCADE,verbose_name="modified_by", related_name='followup_modified_by')
    
    class Meta:
        verbose_name = 'Follows Up'
        verbose_name_plural = 'Follows Up'

class Meetings(models.Model):
    RM_EP = models.ForeignKey("crm.User",blank=True,null=True, on_delete=models.CASCADE,verbose_name="Customer Under this user",related_name='user_meeting')
    LEADS   = models.ForeignKey("crm.Leads",blank=True,null=True, on_delete=models.CASCADE,verbose_name="Lead")
    # MF_CUST = models.ForeignKey("app.Registration_personal_details",blank=True,null=True, on_delete=models.CASCADE,verbose_name="MF Customer")
    I_CUST  = models.ForeignKey("crm.Customer",blank=True,null=True, on_delete=models.CASCADE,verbose_name="Insurance Customer")
    type = [
            ("lead","Lead Customer"),
            # ("mf_customer","MF Customer"),
            ("customer","Customer"),
        ]
    utc = [
        ("bm","Branch Manager"),
        ("rm","Relationship Manager"),
        ("ep","Easy Partner"),
        ]
    TYPE   = models.CharField(max_length=150,blank=True,null=True,choices=type)
    DATE   = models.DateField(blank=True,null=True,verbose_name="Follow up date")
    TIME   = models.TimeField(blank=True,null=True,verbose_name="Follow up time")
    REMARK = models.CharField(max_length=500,blank=True,null=True,verbose_name="Follow Remark")

    USER_TYPE = models.CharField(max_length=50,null=True, choices=utc)
    USER = models.CharField(max_length=50,null=True)

    IS_DELETED = models.BooleanField(default=False)
    CREATED_DATE = models.DateTimeField(auto_now_add=True,null=True)
    UPDATED_DATE = models.DateTimeField(auto_now=True)

    CREATED_BY = models.ForeignKey("crm.User",blank=True,null=True, on_delete=models.CASCADE,verbose_name="created_by", related_name='meeting_created_by')
    MODIFIED_BY = models.ForeignKey("crm.User",blank=True,null=True, on_delete=models.CASCADE,verbose_name="modified_by", related_name='meeting_modified_by')
    
    class Meta:
        verbose_name = 'Meeting'
        verbose_name_plural = 'Meeting'

class Notifications(models.Model):
    type = [
            ("lead","Lead"),
            ("customer","Customer"),
        ]
    
    utc = [
            ("bm","Branch Manager"),
            ("rm","Relationship Manager"),
            ("ep","Easy Partner"),
        ]

    CUSTOMER_IDS = models.CharField(max_length=150,blank=True,null=True,verbose_name="Customer Id")
    TYPE = models.CharField(max_length=150,blank=True,null=True,choices=type)
    TITLE = models.CharField(max_length=500,blank=True,null=True,verbose_name="Title")
    DESCRIPTION = models.CharField(max_length=500,blank=True,null=True,verbose_name="Description")

    USER_TYPE = models.CharField(max_length=50,null=True, choices=utc)
    USER = models.CharField(max_length=50,null=True)

    IS_DELETED = models.BooleanField(default=False)
    CREATED_DATE = models.DateTimeField(auto_now_add=True,null=True)
    UPDATED_DATE = models.DateTimeField(auto_now=True)

    CREATED_BY = models.ForeignKey("crm.User",blank=True,null=True, on_delete=models.CASCADE,verbose_name="created_by", related_name='notification_created_by')
    MODIFIED_BY = models.ForeignKey("crm.User",blank=True,null=True, on_delete=models.CASCADE,verbose_name="modified_by", related_name='notification_modified_by')
    
    class Meta:
        verbose_name = 'Notifications'
        verbose_name_plural = 'Notifications'

class Policy_broker_master(models.Model):
    NAME = models.CharField(max_length=500,blank=True,null=True,verbose_name="Broker Name")

    IS_DELETED = models.BooleanField(default=False)
    CREATED_DATE = models.DateTimeField(auto_now_add=True,null=True)
    UPDATED_DATE = models.DateTimeField(auto_now=True)

    CREATED_BY = models.ForeignKey("crm.User",blank=True,null=True, on_delete=models.CASCADE,verbose_name="created_by", related_name='policy_broker_created_by')
    MODIFIED_BY = models.ForeignKey("crm.User",blank=True,null=True, on_delete=models.CASCADE,verbose_name="modified_by", related_name='policy_broker_modified_by')
    
    class Meta:
        verbose_name = 'Policy Broker Master'
        verbose_name_plural = 'Policy Broker Master'


class Modules(models.Model):
    NAME = models.CharField(max_length=500)
    URL = models.CharField(max_length=500,null=True,blank=True)

    IS_DELETED = models.BooleanField(default=False)
    CREATED_DATE = models.DateTimeField(auto_now_add=True,null=True)
    UPDATED_DATE = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = 'Sidebar Modules'
        verbose_name_plural = 'Sidebar Modules'

    # def __init__(self, *args, **kwargs):
    #     self.NAME = self.NAME.lower()

    def save(self, *args, **kwargs):
        self.NAME = self.NAME.lower()
        return super().save(*args, **kwargs)

    def clean(self):
        if Modules.objects.exclude(id=self.id).filter(NAME=self.NAME).exists():
            logger.info(f"name = {self.NAME}")
            raise ValidationError('This Modules Name is already exists. Please Enter New Module')


class Buy_FD(models.Model):
    EP_RM = models.ForeignKey("crm.User", on_delete=models.CASCADE)
    utc = [
        ("bm","Branch Manager"),
        ("rm","Relationship Manager"),
        ("ep","Easy Partner"),
    ]
    USER_TYPE = models.CharField(max_length=50,null=True, choices=utc)
    buy_choices = [
        ("fd","FD"),
        ("bond","Bond"),
        ("ncd","NCD"),
        ("pms","PMS"),
        ("aif","AIF"),
    ]
    BUY_TYPE = models.CharField(max_length=500,choices=buy_choices)
    CUSTOMER = models.ForeignKey("crm.Customer", on_delete=models.CASCADE)
    START_DATE = models.DateField()
    END_DATE = models.DateField()
    COMPANY_NAME = models.CharField(max_length=500)
    TENURE = models.CharField(max_length=500)
    INTEREST_RATE = models.CharField(max_length=500)
    AMOUNT = models.CharField(max_length=500)
    BROKERAGE_PERCENTAGE = models.CharField(max_length=500)
    BROKERAGE_AMOUNT = models.CharField(max_length=500)
    TABLE_NAME = models.CharField(max_length=50,default="buy_fd")

    IS_DELETED = models.BooleanField(default=False)
    CREATED_DATE = models.DateTimeField(auto_now_add=True,null=True)
    UPDATED_DATE = models.DateTimeField(auto_now=True)
    

    CREATED_BY = models.ForeignKey("crm.User",blank=True,null=True, on_delete=models.CASCADE,verbose_name="created_by", related_name='buy_fd_created_by')
    MODIFIED_BY = models.ForeignKey("crm.User",blank=True,null=True, on_delete=models.CASCADE,verbose_name="modified_by", related_name='buy_fd_modified_by')

class User_Role_Permission(models.Model):
    utc = [
        ("superadmin","Superadmin"),
        ("admin","Admin"),
        ("bm","Branch Manager"),
        ("rm","Relationship Manager"),
        ("ep","Easy Partner"),
        ("bo","Back Office"),
    ]
    USER_TYPE = models.CharField(max_length=150,choices=utc)

    # below fields is used for role based permission of admin,bm,rm,ep
    ALLOWED_MODULES = models.CharField(max_length=500,null=True,blank=True)
    # ALLOWED_URL = models.CharField(max_length=500,null=True,blank=True)

    # HIDDEN_MODULES = models.CharField(max_length=500,null=True,blank=True)

    IS_DELETED = models.BooleanField(default=False)
    CREATED_DATE = models.DateTimeField(auto_now_add=True,null=True)
    UPDATED_DATE = models.DateTimeField(auto_now=True)

    CREATED_BY = models.ForeignKey("crm.User",blank=True,null=True, on_delete=models.CASCADE,verbose_name="created_by", related_name='user_role_created_by')
    MODIFIED_BY = models.ForeignKey("crm.User",blank=True,null=True, on_delete=models.CASCADE,verbose_name="modified_by", related_name='user_role_modified_by')

    class Meta:
        verbose_name = 'User Role Permission'
        verbose_name_plural = 'User Role Permission'

class Commission_paid(models.Model):
    EP = models.ForeignKey("crm.User",on_delete=models.CASCADE)
    AMOUNT = models.CharField(max_length=50)
    TRANSACTION_DATE = models.DateField()
    TRANSACTION_CHECK_NO = models.CharField(max_length=500)

    IS_DELETED = models.BooleanField(default=False)
    CREATED_DATE = models.DateTimeField(auto_now_add=True,null=True)
    UPDATED_DATE = models.DateTimeField(auto_now=True)

    CREATED_BY = models.ForeignKey("crm.User",blank=True,null=True, on_delete=models.CASCADE,verbose_name="created_by", related_name='commission_paid_created_by')
    MODIFIED_BY = models.ForeignKey("crm.User",blank=True,null=True, on_delete=models.CASCADE,verbose_name="modified_by", related_name='commission_paid_modified_by')


class Buy_MF(models.Model):
    utc = [
        ("bm","Branch Manager"),
        ("rm","Relationship Manager"),
        ("ep","Easy Partner"),
    ]

    cust_status_choices = [
        ("Existing","Existing"),
        ("New","New")
    ]

    buy_mode_choices = [
        ("Online","Online"),
        ("Offline","Offline")
    ]

    buy_type_choices = [
        ("Lumpsum","Lumpsum"),
        ("Sip","SIP")
    ]

    EP_RM = models.ForeignKey("crm.User",on_delete=models.CASCADE)
    USER_TYPE = models.CharField(max_length=50,null=True, choices=utc)
    DATE = models.DateField()
    CUSTOMER = models.ForeignKey("crm.Customer", on_delete=models.CASCADE)
    CUSTOMER_STATUS = models.CharField(max_length=50, choices=cust_status_choices)
    SCHEME_NAME = models.CharField(max_length=500)
    AMOUNT_INVESTED = models.CharField(max_length=50)
    MODE = models.CharField(max_length=50,choices=buy_mode_choices)
    BUY_TYPE = models.CharField(max_length=50,choices=buy_type_choices)
    EI_PERCENT = models.CharField(max_length=500,blank=True,null=True,verbose_name="Easy Investology Commission Percentage")
    EI_AMT = models.CharField(max_length=500,blank=True,null=True,verbose_name="Easy Investology Commission Amount")
    EP_PERCENT = models.CharField(max_length=500,blank=True,null=True,verbose_name="Easy Partner Commission Percentage")
    EP_AMT = models.CharField(max_length=500,blank=True,null=True,verbose_name="Easy Partner Commission Amount")
    TABLE_NAME = models.CharField(max_length=50,default="buy_mf")

    IS_DELETED = models.BooleanField(default=False)
    CREATED_DATE = models.DateTimeField(auto_now_add=True,null=True)
    UPDATED_DATE = models.DateTimeField(auto_now=True)

    CREATED_BY = models.ForeignKey("crm.User",blank=True,null=True, on_delete=models.CASCADE,verbose_name="created_by", related_name="buy_mf_created_by")
    MODIFIED_BY = models.ForeignKey("crm.User",blank=True,null=True, on_delete=models.CASCADE,verbose_name="modified_by", related_name="buy_mf_modified_by")


class Demat_account(models.Model):
    DEMAT_CUST              = models.ForeignKey("crm.Customer",blank=True,null=True, on_delete=models.CASCADE,verbose_name="Demat Customer")
    depository_choices      = (
        ("nsdl", "NSDL"),
        ("cdsl", "CDSL"),

    )
    DEPOSITORY_TYPE         = models.CharField(choices=depository_choices, max_length=50,null=True,blank=True,verbose_name="Depository Type")
    ACC_NO                  = models.CharField(max_length=150,blank=True,null=True ,verbose_name="Account Number")
    CLIENT_ID               = models.CharField(max_length=150,blank=True,null=True ,verbose_name="Client Id")
    ACC_DATE                = models.DateField(null=True,blank=True,verbose_name="Account Opening date")
    COMMISSION              = models.CharField(max_length=500,blank=True,null=True,verbose_name="Commission")

    TABLE_NAME              = models.CharField(max_length=50,default="demat")

    IS_DELETED              = models.BooleanField(default=False)
    CREATED_DATE            = models.DateTimeField(auto_now_add=True,null=True)
    UPDATED_DATE            = models.DateTimeField(auto_now=True)

    CREATED_BY              = models.ForeignKey("crm.User",blank=True,null=True, on_delete=models.CASCADE,verbose_name="created_by", related_name='demat_created_by')
    MODIFIED_BY             = models.ForeignKey("crm.User",blank=True,null=True, on_delete=models.CASCADE,verbose_name="modified_by", related_name='demat_modified_by')
    
    class Meta:
        verbose_name = 'Demat Account'
        verbose_name_plural = 'Demat Account'
