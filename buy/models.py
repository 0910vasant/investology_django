from typing import Iterable, Optional
from urllib import request
from django.db import models
from django.contrib.auth.hashers import make_password
from django.core.exceptions import ValidationError
import logging
logger = logging.getLogger()

# Create your models here.
class Buy(models.Model):
    USER                    = models.ForeignKey("app.Registration_personal_details",blank=True,null=True,on_delete=models.CASCADE)
    SENDRESPONSEFORMAT      = models.CharField(max_length=100,blank=True,null=True)
    SESSIONCONTEXT          = models.CharField(max_length=100,blank=True,null=True)
    SENDERSUBID             = models.CharField(max_length=100,blank=True,null=True)
    LOGTP                   = models.CharField(max_length=100,blank=True,null=True)
    VERSIONNO               = models.CharField(max_length=100,blank=True,null=True)
    ACTIONTYPE              = models.CharField(max_length=100,blank=True,null=True)
    TXNTYPE                 = models.CharField(max_length=100,blank=True,null=True)
    ORDERMODE               = models.CharField(max_length=100,blank=True,null=True)
    TRANSOURCE              = models.CharField(max_length=100,blank=True,null=True)
    FOLIOTXNFLAG            = models.CharField(max_length=100,blank=True,null=True)
    TXNEVENT                = models.CharField(max_length=100,blank=True,null=True)
    PAGEFORROLE             = models.CharField(max_length=100,blank=True,null=True)
    CAN                     = models.CharField(max_length=100,blank=True,null=True)
    JOINTHOLDERFLAG         = models.CharField(max_length=100,blank=True,null=True)
    HOLDERDETAIL            = models.CharField(max_length=100,blank=True,null=True)

    DIRECTFLAG              = models.CharField(max_length=100,blank=True,null=True)
    RIAFLAG                 = models.CharField(max_length=100,blank=True,null=True)
    RIACODE                 = models.CharField(max_length=100,blank=True,null=True)
    ARNTYPE                 = models.CharField(max_length=100,blank=True,null=True)
    ARNCODE                 = models.CharField(max_length=100,blank=True,null=True)
    SUBBRKARNLABEL          = models.CharField(max_length=100,blank=True,null=True)
    SUBBRKARNTYPE           = models.CharField(max_length=100,blank=True,null=True)
    SUBBRKARNCODE           = models.CharField(max_length=100,blank=True,null=True)
    SUBBROKCODE             = models.CharField(max_length=100,blank=True,null=True)
    BRANCHRMINTERNALCODE    = models.CharField(max_length=100,blank=True,null=True)
    EUINCODE                = models.CharField(max_length=100,blank=True,null=True)
    EUINDECLARATION         = models.CharField(max_length=100,blank=True,null=True)
    DEPOSITORYFLAG          = models.CharField(max_length=100,blank=True,null=True)
    DPTYPE                  = models.CharField(max_length=100,blank=True,null=True)
    INVDPACCNO              = models.CharField(max_length=100,blank=True,null=True)
    PAYMENTFLAG             = models.CharField(max_length=100,blank=True,null=True)
    PAYMENT_INSTRUMENTTYPE  = models.CharField(max_length=100,blank=True,null=True)
    PAYMENT_BANKID          = models.CharField(max_length=100,blank=True,null=True)
    PAYMENT_INVACCTYPE      = models.CharField(max_length=100,blank=True,null=True)
    PAYMENT_MICRNO          = models.CharField(max_length=100,blank=True,null=True)
    PAYMENT_IFSCCODE        = models.CharField(max_length=100,blank=True,null=True)
    INSTDATE                = models.CharField(max_length=100,blank=True,null=True)
    PAYMENT_INVACCNO        = models.CharField(max_length=100,blank=True,null=True)
    PAYMENT_TXNDONEFLAG     = models.CharField(max_length=100,blank=True,null=True)
    PAYMENTREFNO            = models.CharField(max_length=100,blank=True,null=True)
    PAYMENT_NEWVANFLAG      = models.CharField(max_length=100,blank=True,null=True)
    PAYMENT_VIRTACCNO       = models.CharField(max_length=100,blank=True,null=True)
    PAYMENTAMOUNT           = models.CharField(max_length=100,blank=True,null=True)
    TOTALAMOUNT             = models.CharField(max_length=100,blank=True,null=True)
    EXTGROUPREFNO           = models.CharField(max_length=100,blank=True,null=True)
    NOOFSCHEMES             = models.CharField(max_length=100,blank=True,null=True)

    SUBSEQUENTPAYMENTFLAG   = models.CharField(max_length=100,blank=True,null=True)
    SUBSEQ_EXISTOTMFLAG     = models.CharField(max_length=100,blank=True,null=True)
    SUBSEQ_INVACCTYPE       = models.CharField(max_length=100,blank=True,null=True)
    SUBSEQ_INVACCNO         = models.CharField(max_length=100,blank=True,null=True)
    SUBSEQ_MICRNO           = models.CharField(max_length=100,blank=True,null=True)
    SUBSEQ_IFSCCODE         = models.CharField(max_length=100,blank=True,null=True)
    SUBSEQ_BANKID           = models.CharField(max_length=100,blank=True,null=True)
    SUBSEQ_INSTRUMENTTYPE   = models.CharField(max_length=100,blank=True,null=True)
    SUBSEQ_MAXIMUMAMOUNT    = models.CharField(max_length=100,blank=True,null=True)
    SUBSEQ_PERPETUALFLAG    = models.CharField(max_length=100,blank=True,null=True)
    SUBSEQ_STARTDATE        = models.CharField(max_length=100,blank=True,null=True)
    SUBSEQ_ENDDATE          = models.CharField(max_length=100,blank=True,null=True)
    SUBSEQ_PAYMENTREFNO     = models.CharField(max_length=100,blank=True,null=True)

    HOLDNAT                 = models.CharField(max_length=100,blank=True,null=True)
    TAXSTATUS               = models.CharField(max_length=100,blank=True,null=True)
    PRIPANORPEKRN           = models.CharField(max_length=100,blank=True,null=True)
    SECPANORPEKRN           = models.CharField(max_length=100,blank=True,null=True)
    THRPANORPEKRN           = models.CharField(max_length=100,blank=True,null=True)
    GURPANORPEKRN           = models.CharField(max_length=100,blank=True,null=True)
    GROUPORDERNO            = models.CharField(max_length=100,blank=True,null=True)
    APPLINKPRIM             = models.TextField(blank=True,null=True)
    NETBANKINGLINK          = models.TextField(blank=True,null=True)
    FOLIONUMBER             = models.TextField(blank=True,null=True)

    IS_DELETED   = models.BooleanField(default=False)
    CREATED_DATE = models.DateTimeField(auto_now_add=True,null=True)
    UPDATED_DATE = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name_plural = 'Buy'

class Buy_schemes(models.Model):
    BUY                     = models.ForeignKey("buy.Buy",blank=True,null=True,on_delete=models.CASCADE)
    CART                    = models.ForeignKey("app.Cart",blank=True,null=True,on_delete=models.CASCADE)
    RECORDNO                = models.CharField(max_length=100,blank=True,null=True)
    EXTUNIQUEREFID          = models.CharField(max_length=100,blank=True,null=True)
    FOLIOACCNO              = models.CharField(max_length=100,blank=True,null=True)
    FOLIOCHECKDIGIT         = models.CharField(max_length=100,blank=True,null=True)
    RTAAMCCODE              = models.CharField(max_length=100,blank=True,null=True)
    RTASCHEMECODE           = models.CharField(max_length=100,blank=True,null=True)
    SRCSCHEMECODE           = models.CharField(max_length=500,null=True,blank=True,verbose_name="Src Scheme Code")
    TARSCHEMECODE           = models.CharField(max_length=500,null=True,blank=True,verbose_name="Tar Scheme Code")
    DIVIDENDOPTION          = models.CharField(max_length=100,blank=True,null=True)
    TXNVOLUME_TYPE          = models.CharField(max_length=100,blank=True,null=True)
    TXNVOLUME               = models.CharField(max_length=100,blank=True,null=True)
    FREQUENCY               = models.CharField(max_length=100,blank=True,null=True)
    DAY                     = models.CharField(max_length=100,blank=True,null=True)
    START_MONTH             = models.CharField(max_length=100,blank=True,null=True)
    START_YEAR              = models.CharField(max_length=100,blank=True,null=True)
    END_MONTH               = models.CharField(max_length=100,blank=True,null=True)
    END_YEAR                = models.CharField(max_length=100,blank=True,null=True)

class Redeem(models.Model):
    USER                = models.ForeignKey("app.Registration_personal_details",blank=True,null=True,on_delete=models.CASCADE)
    SENDRESPONSEFORMAT  = models.CharField(max_length=100,blank=True,null=True)
    SESSIONCONTEXT      = models.CharField(max_length=100,blank=True,null=True)
    SENDERSUBID         = models.CharField(max_length=100,blank=True,null=True)
    LOGTP               = models.CharField(max_length=100,blank=True,null=True)
    VERSIONNO           = models.CharField(max_length=100,blank=True,null=True)

    TXNTYPE             = models.CharField(max_length=100,blank=True,null=True)
    ORDERMODE           = models.CharField(max_length=100,blank=True,null=True)

    TRANSOURCE          = models.CharField(max_length=100,blank=True,null=True)
    ACTIONTYPE          = models.CharField(max_length=100,blank=True,null=True)
    FOLIOTXNFLAG        = models.CharField(max_length=100,blank=True,null=True)
    TXNEVENT            = models.CharField(max_length=100,blank=True,null=True)
    PAGEFORROLE         = models.CharField(max_length=100,blank=True,null=True)
    CAN                 = models.CharField(max_length=100,blank=True,null=True)
    JOINTHOLDERFLAG     = models.CharField(max_length=100,blank=True,null=True)
    HOLDERDETAIL        = models.CharField(max_length=100,blank=True,null=True)
    NOOFSCHEMES         = models.CharField(max_length=100,blank=True,null=True)
    GROUPORDERNO        = models.CharField(max_length=100,blank=True,null=True)

    IS_DELETED          = models.BooleanField(default=False)
    CREATED_DATE        = models.DateTimeField(auto_now_add=True,null=True)
    UPDATED_DATE        = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name_plural = 'Redeem'

class Redeem_schemes(models.Model):
    REDEEM              = models.ForeignKey("buy.Redeem",blank=True,null=True,on_delete=models.CASCADE)
    RECORDNO            = models.CharField(max_length=100,blank=True,null=True)
    EXTUNIQUEREFID      = models.CharField(max_length=100,blank=True,null=True)
    FOLIOACCNO          = models.CharField(max_length=100,blank=True,null=True)
    FOLIOCHECKDIGIT     = models.CharField(max_length=100,blank=True,null=True)
    RTAAMCCODE          = models.CharField(max_length=100,blank=True,null=True)
    RTASCHEMECODE       = models.CharField(max_length=100,blank=True,null=True)

    TXNVOLUMETYPE       = models.CharField(max_length=100,blank=True,null=True)
    TXNVOLUME           = models.CharField(max_length=100,blank=True,null=True)
    PAYOUTFLAG          = models.CharField(max_length=100,blank=True,null=True)
    INVACCNO            = models.CharField(max_length=100,blank=True,null=True)
    MICRNO              = models.CharField(max_length=100,blank=True,null=True)
    IFSCCODE            = models.CharField(max_length=100,blank=True,null=True)

    FREQUENCY           = models.CharField(max_length=100,blank=True,null=True)
    DAY                 = models.CharField(max_length=100,blank=True,null=True)
    START_MONTH         = models.CharField(max_length=100,blank=True,null=True)
    START_YEAR          = models.CharField(max_length=100,blank=True,null=True)
    END_MONTH           = models.CharField(max_length=100,blank=True,null=True)
    END_YEAR            = models.CharField(max_length=100,blank=True,null=True)

    IS_DELETED          = models.BooleanField(default=False)
    CREATED_DATE        = models.DateTimeField(auto_now_add=True,null=True)
    UPDATED_DATE        = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name_plural = 'Redeem Schemes'
