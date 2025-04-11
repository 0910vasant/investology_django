import os
from datetime import date, timedelta
from django.http import JsonResponse
from django.shortcuts import render
from django.contrib.auth.hashers import make_password
from app.pass_enc import encrypt,decrypt
from rest_framework.decorators import api_view
from app.models import *
from crm.models import User,Branch_Manager,Relationship_Manager,Easy_Partner
from admin_panel.models import *
from PIL import Image
from django.contrib import messages
import pytesseract
import re
import logging
from .registration_xml import can_registration_api
from .registration_file_upload import file_upload
import requests
import xmltodict
import json
logger = logging.getLogger(__name__)
import pandas as pd
from django.db.models import Sum
from datetime import datetime
from dateutil.relativedelta import relativedelta
from app.serializers import *
from django.contrib.auth.hashers import check_password
import random
import base64

from django.db.models import F, Subquery, OuterRef , Max ,Min
from django.db import transaction
import time
from babel.numbers import format_number

# from admin_panel.views import calculated_xirr
# Create your views here.



def delete_customer_page(request):
    return render(request,"delete_customer.html")

def privacy_policy_page(request):
    return render(request,"privacy_policy.html")

# masters
def get_holding_nature(request):
    try:
        data = list(Holding_nature_master.objects.values())
        return JsonResponse(data,safe=False)
    except Exception as e:
        logger.exception(e)
        return JsonResponse("something went wrong",safe=False,status=500)

def get_bank_account_type(request):
    try:
        tax_status_id      = request.GET.get("tax_status_id")
        logger.info(f"tax_status_id = {tax_status_id}")
        
        data = Tax_status_master_Serializer(Tax_status_master.objects.get(id=tax_status_id),many=False).data
        # data = list(Bank_account_type_master.objects.values())
        return JsonResponse(data,safe=False)
    except Exception as e:
        logger.exception(f"{e}")
        return JsonResponse(f"{e}",safe=False,status=500)

def get_investor_category(request):
    data = list(Investor_category_master.objects.values())
    return JsonResponse(data,safe=False)

def get_tax_status(request):
    try:
        investor_category_id = request.GET.get("investor_category_id")
        data = list(Tax_status_master.objects.filter(INVESTOR_CATGORY=investor_category_id).values().order_by('-id'))
        return JsonResponse(data,safe=False)
    except Exception as e:
        logger.exception(f"{e}")
        return JsonResponse(f"{e}",safe=False,status=500)

def get_bank_proof(request):
    try:
        data = list(Bank_proof_master.objects.values())
        return JsonResponse(data,safe=False)
    except Exception as e:
        logger.exception(f"{e}")
        return JsonResponse(f"{e}",safe=False,status=500)

def get_gross_annual_income(request):
    try:
        data = list(Gross_annual_income_master.objects.values())
        return JsonResponse(data,safe=False)
    except Exception as e:
        logger.exception(f"{e}")
        return JsonResponse(f"{e}",safe=False,status=500)

def get_source_of_wealth(request):
    try:
        data = list(Source_of_wealth_master.objects.values())
        return JsonResponse(data,safe=False)
    except Exception as e:
        logger.exception(f"{e}")
        return JsonResponse(f"{e}",safe=False,status=500)

def get_kra_address_type(request):
    try:
        data = list(Kra_address_type_master.objects.values())
        return JsonResponse(data,safe=False)
    except Exception as e:
        logger.exception(f"{e}")
        return JsonResponse(f"{e}",safe=False,status=500)

def get_occupation(request):
    try:
        data = list(Occupation_master.objects.values())
        return JsonResponse(data,safe=False)
    except Exception as e:
        logger.exception(f"{e}")
        return JsonResponse(f"{e}",safe=False,status=500)

def get_pep_status(request):
    try:
        data = list(Pep_status_master.objects.values())
        return JsonResponse(data,safe=False)
    except Exception as e:
        logger.exception(f"{e}")
        return JsonResponse(f"{e}",safe=False,status=500)

def get_country(request):
    try:
        data = list(Country_master.objects.values('id','NAME','CODE'))
        return JsonResponse(data,safe=False)
    except Exception as e:
        logger.exception(f"{e}")
        return JsonResponse(f"{e}",safe=False,status=500)

def get_state(request):
    try:
        data = list(State_master.objects.values('id','NAME','CODE'))
        return JsonResponse(data,safe=False)
    except Exception as e:
        logger.exception(f"{e}")
        return JsonResponse(f"{e}",safe=False,status=500)

def get_city(request,state):
    try:
        # logger.info(f"state = {state}")
        data = list(Pincode_master.objects.filter(STATE=state).values('CITY').distinct())
        # logger.info(f"data = {data}")
        return JsonResponse(data,safe=False)
    except Exception as e:
        logger.exception(f"{e}")
        return JsonResponse(f"{e}",safe=False,status=500)

def get_pincode(request,city):
    try:
        # logger.info(f"city = {city}")
        data = list(Pincode_master.objects.filter(CITY__iexact=city).values('id','CITY','PINCODE'))
        return JsonResponse(data,safe=False)
    except Exception as e:
        logger.exception(f"{e}")
        return JsonResponse(f"{e}",safe=False,status=500)


def get_identification_type(request):
    try:
        data = list(Identification_type_master.objects.values('id','NAME','CODE'))
        return JsonResponse(data,safe=False)
    except Exception as e:
        logger.exception(f"{e}")
        return JsonResponse(f"{e}",safe=False,status=500)


def get_bank(request):
    try:
        data = list(Bank_master.objects.values('id','NAME','CODE').order_by('NAME'))
        return JsonResponse(data,safe=False)
    except Exception as e:
        logger.exception(f"{e}")
        return JsonResponse(f"{e}",safe=False,status=500)


@api_view(['POST'])
def get_enc_password(request):
    try:
        data = Enc_password.objects.last().ENC_PASSWORD
        return JsonResponse(data,safe=False)
    except Exception as e:
        logger.exception(f"{e}")
        return JsonResponse(f"{e}",safe=False,status=500)

def header_checklist_data(app_type,use_for):
    data    = Header_Checklist.objects.get(APP_TYPE=app_type,CHECKLIST_USE_FOR=use_for,IS_DELETED=False)
    return data


@api_view(["POST"])
def scan_pan(request):
    try:
        pan_img = request.data.get("pan_img")
        pan_no = request.data.get("pan_no")

        logger.info(f"pan_img = {pan_img}")
        regex = "[A-Z]{5}[0-9]{4}[A-Z]{1}"
        p = re.compile(regex)
        
        if pan_img and pan_no is not None:
            logger.info(f"both")
            regex_result = re.search(p,pan_no)
            if regex_result:
                a = Scan_pan.objects.create(
                    PAN = pan_no,
                    PAN_IMAGE = pan_img
                )
                return JsonResponse({"message":"pan number and image recorded successfully"},status=200)
            else:
                return JsonResponse({"message":"Invalid pan number"},status=412)

        # all_string = pytesseract.image_to_string(Image.open('mayur_pan1.jpg')).strip()
        # all_string = pytesseract.image_to_string(Image.open(f"media/{a.PAN_IMAGE}")).strip()
        all_string = pytesseract.image_to_string(Image.open(pan_img)).strip()
        a = all_string.split("\n")
        logger.info(f"a = {a}")
        pan_no_str = ""
        for i in a:
            regex_result = re.search(p,i)
            if regex_result:
                pan_no_str = regex_result.group()
                break
        if len(pan_no_str) == 10:
            logger.info(f"record exists = {Scan_pan.objects.filter(PAN = pan_no).exists()}")
            if  Scan_pan.objects.filter(PAN = pan_no_str).exists() == False:
                a = Scan_pan.objects.create(
                    PAN = pan_no_str,
                    PAN_IMAGE = pan_img
                )
            return JsonResponse({"pan_no": pan_no_str},status=200)
        else:
            return JsonResponse({"message":"image is not readable or invalid please upload correct and clear image or enter pan number manually"},safe=False,status=412)
    except Exception as e:
        logger.exception(f"{e}")
        return JsonResponse(f"{e}",safe=False,status=500)

@api_view(["POST"])
def app_login(request):
    try:
        mobile_no   = request.data.get("mobile_no")
        password    = request.data.get("password")
        
        if Registration_personal_details.objects.filter(MOBILE=mobile_no).exists():
            user = Registration_personal_details.objects.get(MOBILE=mobile_no)
            if(check_password(password,user.PASSWORD)):
                # data = {
                #     "sendResponseFormat"    : "JSON",
                #     "loginid"               : "EASYINVUAT",
                #     "password"              : "T7BO43drYUA0WrCASXo75g==",
                #     "entityId"              : "40007K",
                #     "logTp"                 : "A",
                #     "versionNo"             : "1.00"
                # }
                data = list(Registration_personal_details.objects.filter(MOBILE=mobile_no).exclude(IS_DELETED=True).values())
                if data[0]['CAN']:
                    can = True
                else:
                    can = False
                logger.info(f"""
                    username : {mobile_no}
                    password : {password}
                """)
                return JsonResponse({"message":"Login Successfully","data":data,"can":can},safe=False,status=200)
            else:
                return JsonResponse("Invalid credentials",safe=False,status=412)
        else:
            # messages.error(request,"User Does Not Exist")
            # return redirect("/login")
            return JsonResponse("User Does Not Exist. Please Contact To Administrator",safe=False,status=412)
    except Exception as e:
        logger.exception(e)
        return JsonResponse("Something went wrong",safe=False,status=500)

@api_view(["POST"])
def mfu_user_login_data(request):
    try:
        user_id     = request.data.get("user_id")
        app_type    = request.data.get("app_type") # uat , prod
        
        # logger.info(f"""
        #     login_id = {user_id}
        #     app_type = {app_type}
        #     """)
        user_data = Registration_personal_details.objects.get(id=user_id)
        data = {
            "can_No"        : user_data.CAN,
            "pay_pan_no"    : user_data.PAN_NO,
            "bank_details"  : list(Registration_bank_details.objects.filter(USER=user_id,IS_DELETED=False,DEFAULT_BANK=True).values("ACC_NO","ACC_TYPE__BANK_ACCOUNT_TYPE","ACC_TYPE__ACC_TYPE_FULL_FORM","BANK_NAME__NAME","BANK_NAME__CODE", "MICR_NO","IFSC_CODE","TRANSACTION_LIMIT","MANDATE_START_DATE","MANDATE_END_DATE","MMRN_AGGR_STATUS","PRN")),
            "checklist"     : list(Header_Checklist.objects.filter(APP_TYPE=app_type,CHECKLIST_USE_FOR="transaction").values())
        }
        return JsonResponse(data,safe=False,status=200)
    except Exception as e:
        logger.exception(e)
        return JsonResponse("Something went wrong",safe=False,status=500)

@api_view(["POST"]) 
def mfu_login_session(request):
    try:
        app_type    = request.data.get("app_type") # uat , prod
        logger.info(f"""
                        app_type = {app_type}
                    """)
        data = list(investology_login_session.objects.filter(APP_TYPE=app_type).values().order_by("-id")[:1])
        return JsonResponse(data,safe=False,status=200)
    except Exception as e:
        logger.exception(e)
        return JsonResponse("Something went wrong",safe=False,status=500)


@api_view(["POST"])
def update_mfu_login_session_api(request):
    try:
        app_type            = request.data.get("app_type")
        lastlogondate       = request.data.get("lastlogondate")
        pwdexpdateindat     = request.data.get("pwdexpdateindat")
        forceaddauthflg     = request.data.get("forceaddauthflg")
        participantid       = request.data.get("participantid")
        officeid            = request.data.get("officeid")
        sessioncontext      = request.data.get("sessioncontext")
        sendersubid         = request.data.get("sendersubid")
        app_type            = request.data.get("app_type")


        logger.info(f"""
            lastlogondate       = {lastlogondate}
            pwdexpdateindat     = {pwdexpdateindat}
            forceaddauthflg     = {forceaddauthflg}
            participantid       = {participantid}
            officeid            = {officeid}
            sessioncontext      = {sessioncontext}
            sendersubid         = {sendersubid}
            app_type            = {app_type}
        """)
        session = investology_login_session.objects.get(APP_TYPE=app_type)
        session.LASTLOGONDATE       = lastlogondate
        session.PWDEXPDATEINDAT     = pwdexpdateindat
        session.FORCEADDAUTHFLG     = forceaddauthflg
        session.PARTICIPANTID       = participantid
        session.OFFICEID            = officeid
        session.SESSIONCONTEXT      = sessioncontext
        session.SENDERSUBID         = sendersubid
        session.save()

        return JsonResponse("Session Renew Successfully",safe=False,status=200)
    except Exception as e:
        logger.exception(e)
        return JsonResponse("Something went wrong",safe=False,status=500)

@api_view(["POST"]) 
def load_under_customer(request):
    try:
        login_id            = request.data.get("login_id")
        login_user_type     = request.data.get("login_user_type")
        data = list(Registration_personal_details.objects.filter(RM_EP=login_id,TYPE=login_user_type).values("id","NAME","MOBILE","PAN_NO","CAN","EMAIL").order_by("-id"))
        return JsonResponse({"data":data},safe=False,status=200)
    except Exception as e:
        logger.exception(f"{e}")
        return JsonResponse(f"{e}",safe=False,status=500)


# --------------------------------------- MFU Can Creation Start -----------------------------------
def pan_validation(request):
    try:
        pan_no          = request.GET.get("pan_no")
        user_id         = request.GET.get("user_id")
        app_type        = request.GET.get("app_type")
        logger.info(f"""
            pan_no      = {pan_no}
            user_id     = {user_id}
            app_type    = {app_type}
        """)
        # if pan_no:
        #     if user_id != "undefined":
        #         if Registration_personal_details.objects.filter(PAN_NO = pan_no,APP_TYPE=app_type).exclude(id=user_id).exists():
        #             # if
        #             return JsonResponse("Pan card can not be verified as the pan number is already exist",safe=False,status=412)
        #         else:
        #             return JsonResponse({"pan_no":pan_no},safe=False,status=200)
        #     return JsonResponse("Please Fill Sign up Form",safe=False)
        # return JsonResponse("Please Enter Pan No",safe=False,status=412)
        return JsonResponse({"pan_no":pan_no},safe=False,status=200)
    except Exception as e:
        logger.exception(f"{e}")
        return JsonResponse(f"{e}",safe=False,status=500)
    
@api_view(["POST"])  
def send_kyc_link(request):
    try:
        cust_mobile = request.data.get("cust_mobile")
        cust_name = request.data.get("cust_name")
        cust_mail = request.data.get("cust_mail")
        cust_pan = request.data.get("cust_pan")
        encoded_credentials = convert_to_base64()
        headers = {
            'authorization':f'Basic {encoded_credentials}',
            'Content-Type': 'application/json'
        }
        url = "https://ext.digio.in:444/client/kyc/v2/request/with_template"
        payload =   {
                        "customer_identifier": cust_mobile, 
                        "customer_name": cust_name, 
                        "reference_id": "", 
                        "template_name": os.environ["TEMPLATE_NAME"],
                        "notify_customer": True, 
                        "request_details": {
                            "Pan_Number":cust_pan
                        },
                        "generate_access_token": False
                    }
                        
        response = requests.request("POST", url, headers=headers, json=payload, verify=False)
        # logger.info(f"""
        #             type          = {type(response.text)}
        #             response.text = {response.text['id']}
        #             """)
        if response.status_code == 200:
            response = json.loads(response.text)

            KYC_data_logs.objects.create(
                REQUEST_ID              = response["id"],
                CLIENT_REF_ID           = response["reference_id"],
                CUSTOMER_IDENTIFIER     = response["customer_identifier"],
                WORKFLOW_NAME           = response["workflow_name"],
            )
            return JsonResponse({"message": "KYC is not done for given pan Please Do Kyc "}, status=200)
        else:
            return JsonResponse({"error": "External API returned an error"}, status=response.status_code)
        
    except Exception as e:
        logger.exception(e)
        return JsonResponse({"error":"something went wrong"},status=500)


@api_view(['POST'])
def registration1(request):
    # if request.method == 'POST':
    try:
        # logger.info(f"request body = {request.body}")
        user_id         = request.data.get('user_id')
        acc_type        = request.data.get('acc_type')
        pan_no          = request.data.get('pan_no')
        name            = request.data.get('name')
        email           = request.data.get('email')
        mobile          = request.data.get('mobile')
        # username = request.data.get('username')
        password        = request.data.get('password')
        app_type        = request.data.get('app_type')


        login_id        = request.data.get('login_id')
        login_user_id   = request.data.get('login_user_id')
        login_user_type = request.data.get('login_user_type')

        logger.info(f'''
            user_id         = {user_id}
            acc_type        = {acc_type}
            pan_no          = {pan_no}
            name            = {name}
            email           = {email}
            mobile          = {mobile}
            password        = {password}
            app_type        = {app_type}

            login_id        = {login_id}
            login_user_id   = {login_user_id}
            login_user_type = {login_user_type}
        ''')
        if user_id != "":
            a = Registration_personal_details.objects.get(id = user_id)
            if Registration_personal_details.objects.filter(MOBILE=mobile,APP_TYPE=app_type).exclude(id = user_id).exists():
                return JsonResponse("Mobile No already exists",safe=False,status=412)
            a.PASSWORD        = password
        else:
            if Registration_personal_details.objects.filter(MOBILE=mobile,APP_TYPE=app_type).exists():
                return JsonResponse("Mobile No already exists",safe=False,status=412)
            a = Registration_personal_details.objects.create(APP_TYPE=app_type)
            if(check_password(password,a.PASSWORD)):
                pass
            else:
                a.PASSWORD        = password

        if login_id and login_user_id and login_user_type:
            a.RM_EP           = User.objects.get(id=login_id)
            a.TYPE            = login_user_type
            if login_user_type == "bm":
                a.BM = Branch_Manager.objects.get(id=login_user_id)
            if login_user_type == "rm":
                a.RM = Relationship_Manager.objects.get(id=login_user_id)
            if login_user_type == "ep":
                a.EP = Easy_Partner.objects.get(id=login_user_id)
        
        # a.ACCOUNT_TYPE    = Holding_nature_master.objects.get(id=acc_type)
        a.PAN_NO          = pan_no
        a.NAME            = name
        a.EMAIL           = email
        a.MOBILE          = mobile
        a.save()
        return JsonResponse({"user_id":a.id,"message":"User Successfully Registered"},safe=False,status=200)
    except Exception as e:
        logger.exception(e)
        return JsonResponse("something went wrong",safe=False,status=500)

@api_view(['POST'])
def registration2(request):
    try:
        user_id                 = request.data.get("user_id")
        investor_category       = request.data.get("investor_category")
        tax_status              = request.data.get("tax_status")
        holding_nature          = request.data.get("holding_nature")
        holding_count           = request.data.get("holding_count")

        # Basic Details Start
#         RESIDENCE_ISD
# MOB_ISD_CODE
# OFF_ISD
# RESIDENCE_ISD
# MOB_ISD_CODE
# OFF_ISD

# Residence_isd
# mob_isd_code
# off_isd
        holder_type             = request.data.getlist('holder_type')
        holder_name             = request.data.getlist('holder_name')
        holder_dob              = request.data.getlist('holder_dob')
        pan_no                  = request.data.getlist('pan_no')
        holder_pan_img          = request.FILES.getlist('holder_pan_img')
        minor_birth_certificate = request.FILES.get('minor_birth_certificate_proof')

        residence_isd           = request.data.getlist('residence_isd')
        residence_std           = request.data.getlist('residence_std')
        residence_phone_no      = request.data.getlist('residence_phone_no')

        mob_isd_code            = request.data.getlist('mob_isd_code')
        pri_mob_no              = request.data.getlist('pri_mob_no')
        pri_mob_belongsto       = request.data.getlist('pri_mob_belongsto')
        alt_mob_no              = request.data.getlist('alt_mob_no')
        pri_email               = request.data.getlist('pri_email')
        pri_email_belongsto     = request.data.getlist('pri_email_belongsto')
        alt_email               = request.data.getlist('alt_email')
        relationship_with_minor = request.data.getlist('relationship_with_minor')
        proof_of_relationship   = request.data.getlist('proof_of_relationship')
        relationship_proof_doc  = request.data.getlist('relationship_proof_doc')

        # Additional KYC Details
        income                  = request.data.getlist('income')
        gross_annual_income     = request.data.getlist('gross_annual_income')
        networth_in_rupees      = request.data.getlist('networth_in_rupees')
        networth_as_on_date     = request.data.getlist('networth_as_on_date')
        source_of_wealth        = request.data.getlist('source_of_wealth')
        source_of_wealth_others = request.data.getlist('source_of_wealth_others')
        kra_address_type        = request.data.getlist('kra_address_type')
        occupation              = request.data.getlist('occupation')
        occupation_others       = request.data.getlist('occupation_others')
        pep_status              = request.data.getlist('pep_status')
        any_other_information   = request.data.getlist('any_other_information')
        # FATCA Details
        placeofbirth            = request.data.getlist('placeofbirth')
        country_of_birth        = request.data.getlist('country_of_birth')
        other_country           = request.data.getlist('other_country')
        citizenship             = request.data.getlist('citizenship')
        other_citizenship       = request.data.getlist('other_citizenship')
        nationality             = request.data.getlist('nationality')
        other_nationality       = request.data.getlist('other_nationality')
        tax_resident_of_any_other_country = request.data.getlist('tax_resident_of_any_other_country')
        # tax Country
        tax_country             = request.data.getlist('tax_country')
        tax_country_other       = request.data.getlist('tax_country_other')
        tax_ref_no              = request.data.getlist('tax_ref_no')
        identity_type           = request.data.getlist('identity_type')
        identity_type_oth       = request.data.getlist('identity_type_oth')

        logger.info(f"""
            user_id                 = {user_id}
            investor_category       = {investor_category}
            tax_status              = {tax_status}
            holding_nature          = {holding_nature}
            holding_count           = {holding_count}
            # Basic Details
            holder_type             = {holder_type}
            holder_name             = {holder_name}
            holder_dob              = {holder_dob}
            pan_no                  = {pan_no}
            holder_pan_img          = {holder_pan_img}
            minor_birth_certificate = {minor_birth_certificate}
            residence_isd           = {residence_isd}
            
            residence_std           = {residence_std}
            residence_phone_no      = {residence_phone_no}
            mob_isd_code            = {mob_isd_code}
            pri_mob_no              = {pri_mob_no}
            pri_mob_belongsto       = {pri_mob_belongsto}
            alt_mob_no              = {alt_mob_no}
            pri_email               = {pri_email}
            pri_email_belongsto     = {pri_email_belongsto}
            alt_email               = {alt_email}
            relationship_with_minor = {relationship_with_minor}
            proof_of_relationship   = {proof_of_relationship}
            relationship_proof_doc  = {relationship_proof_doc}

            # Additional KYC Details
            income                  = {income}
            gross_annual_income     = {gross_annual_income}
            networth_in_rupees      = {networth_in_rupees}
            networth_as_on_date     = {networth_as_on_date}
            source_of_wealth        = {source_of_wealth}
            source_of_wealth_others = {source_of_wealth_others}
            kra_address_type        = {kra_address_type}
            occupation              = {occupation}
            occupation_others       = {occupation_others}
            pep_status              = {pep_status}
            any_other_information   = {any_other_information}

            # FATCA Details
            placeofbirth        = {placeofbirth}
            country_of_birth    = {country_of_birth}
            other_country       = {other_country}
            citizenship         = {citizenship}
            other_citizenship   = {other_citizenship}
            nationality         = {nationality}
            other_nationality   = {other_nationality}
            tax_resident_of_any_other_country = {tax_resident_of_any_other_country}

            tax_country         = {tax_country}
            tax_country_other   = {tax_country_other}
            tax_ref_no          = {tax_ref_no}
            identity_type       = {identity_type}
            identity_type_oth   = {identity_type_oth}
        """)
        if user_id and user_id != "undefined":
            if len(holder_pan_img) == 0:
                return JsonResponse("Pan holder image not found",safe=False,status=412)
            user_obj = Registration_personal_details.objects.get(id=user_id)
            if Registration_mfu_details.objects.filter(USER=user_id).exists():
                mfu = Registration_mfu_details.objects.get(USER=user_id)
            else:
                mfu = Registration_mfu_details.objects.create(
                    USER = user_obj
                )

            mfu.HOLDING_NATURE              = Holding_nature_master.objects.get(id=holding_nature)
            mfu.INVESTOR_CATEGORY           = Investor_category_master.objects.get(id=investor_category)
            mfu.TAX_STATUS                  = Tax_status_master.objects.get(id=tax_status)
            mfu.HOLDING_COUNT               = holding_count
            mfu.save()

            Registration_holder_details.objects.filter(USER=user_id).update(IS_DELETED=True)
            for i in range(len(holder_type)):
                if holder_name[i] and holder_dob[i]:
                    holder = Registration_holder_details.objects.create(
                        USER = user_obj
                    )
                    # Basic Details Start
                    holder.HOLDER_TYPE              = holder_type[i]
                    holder.HOLDER_NAME              = holder_name[i]
                    holder.HOLDER_DOB               = holder_dob[i]
                    holder.PAN_NO                   = pan_no[i]
                    if holder_type[i] == "PR":
                        #Can is created on the Base Of This Pan
                        user_obj.PAN_NO             = pan_no[i]
                        user_obj.save()
                    if (holder_type[i] == "GU" and mfu.INVESTOR_CATEGORY.CODE == "M"):
                        holder.HOLDER_PAN_IMG       = holder_pan_img[0]
                        #Can is created on the Base Of This Pan
                        user_obj.PAN_NO             = pan_no[i]
                        user_obj.save()
                    if mfu.INVESTOR_CATEGORY.CODE != "M":
                        holder.HOLDER_PAN_IMG       = holder_pan_img[i]
                
                    holder.RESIDENCE_ISD            = residence_isd[i]
                    holder.RESIDENCE_STD            = residence_std[i]
                    holder.RESIDENCE_PHONE_NO       = residence_phone_no[i]

                    holder.MOB_ISD_CODE       = mob_isd_code[i]
                    holder.PRI_MOB_NO               = pri_mob_no[i]
                    holder.PRI_MOB_BELONGSTO        = pri_mob_belongsto[i]
                    holder.ALT_MOB_NO               = alt_mob_no[i]
                    holder.PRI_EMAIL                = pri_email[i]
                    holder.PRI_EMAIL_BELONGSTO      = pri_email_belongsto[i]
                    holder.ALT_EMAIL                = alt_email[i]
                    # MINOR_BIRTH_CERTIFICATE
                    if (mfu.INVESTOR_CATEGORY.CODE == "M" and holder_type[i] == "PR"):
                        holder.MINOR_BIRTH_CERTIFICATE  = minor_birth_certificate

                    if holder_type[i] == "GU":
                        holder.RELATIONSHIP_WITH_MINOR  = relationship_with_minor[0]
                        holder.PROOF_OF_RELATIONSHIP    = proof_of_relationship[0]
                        holder.RELATIONSHIP_PROOF_DOC   = relationship_proof_doc[0]
                    #        Additional KYC Details
                    # logger.info(f"""
                    #     mfu.INVESTOR_CATEGORY.CODE  = {mfu.INVESTOR_CATEGORY.CODE}
                    #     holder_type[i]              = {holder_type[i]}
                    # """)
                    

                    # if mfu.INVESTOR_CATEGORY.CODE != "M" and holder_type[i] != "PR":
                        # logger.info(f"enter kyc form")
                    if income[i] == "gross_annual_income":
                        holder.INCOME_TYPE          = income[i]
                        holder.GROSS_ANNUAL_INCOME  = Gross_annual_income_master.objects.get(id=gross_annual_income[i])
                    if income[i] == "networth":
                        holder.INCOME_TYPE          = income[i]
                        holder.NETWORTH_IN_RUPEES   = networth_in_rupees[i]
                        holder.NETWORTH_AS_ON_DATE  = networth_as_on_date[i]
                    # if source_of_wealth[i]:
                    if source_of_wealth[i] and source_of_wealth[i] not in ['null', '']:
                        holder.SOURCE_OF_WEALTH     = Source_of_wealth_master.objects.get(id=source_of_wealth[i])
                    holder.SOURCE_OF_WEALTH_OTHERS  = source_of_wealth_others[i]
                    holder.KRA_ADDRESS_TYPE         = Kra_address_type_master.objects.get(id=kra_address_type[i])
                    holder.OCCUPATION               = Occupation_master.objects.get(id=occupation[i])
                    holder.OCCUPATION_OTHERS        = occupation_others[i]
                    holder.PEP_STATUS               = Pep_status_master.objects.get(id=pep_status[i])
                    holder.ANY_OTHER_INFORMATION    = any_other_information[i]
                    #       FATCA Details
                    holder.BIRTH_CITY               = placeofbirth[i]
                    holder.BIRTH_COUNTRY            = Country_master.objects.get(id=country_of_birth[i])
                    holder.BIRTH_COUNTRY_OTH        = other_country[i]
                    holder.CITIZENSHIP              = Country_master.objects.get(id=citizenship[i])
                    holder.CITIZENSHIP_OTH          = other_citizenship[i]
                    holder.NATIONALITY              = Country_master.objects.get(id=nationality[i])
                    holder.NATIONALITY_OTH          = other_nationality[i]
                    holder.TAX_RES_FLAG             = tax_resident_of_any_other_country[i]
                    
                    if tax_resident_of_any_other_country[i] == "Y":
                        holder.TAX_COUNTRY          = Country_master.objects.get(id=tax_country[i])
                        holder.TAX_COUNTRY_OTH      = tax_country_other[i]
                        holder.TAX_REF_NO           = tax_ref_no[i]
                        holder.IDENTI_TYPE          = Identification_type_master.objects.get(id=identity_type[i])
                        holder.IDENTI_TYPE_OTH      = identity_type_oth[i]
                    holder.save()
            return JsonResponse("Holder Details Added Successfully",safe=False,status=200)
        return JsonResponse("Please Contact Administrator",safe=False,status=412)
    except Exception as e:
        logger.exception(e)
        return JsonResponse("something went wrong",safe=False,status=500)

# @api_view(['POST'])
# def registration2(request):
#     try:
#         user_id                     = request.data.get('user_id')
#         client_code                 = request.data.get('client_code')
#         investor_category           = request.data.get('investor_category')
#         tax_status                  = request.data.get('tax_status')
#         holding_nature              = request.data.get('holding_nature')
#         primary_holder_name         = request.data.get('primary_holder_name')
#         primary_holder_dob          = request.data.get('primary_holder_dob')
#         # if Holding_nature_master.objects.get(id=holding_nature).CODE == "SI":

#         secondary_holder_name       = request.data.get('secondary_holder_name')
#         secondary_holder_dob        = request.data.get('secondary_holder_dob')
#         secondary_pan_holder        = request.data.get('secondary_pan_holder')

#         third_holder_name           = request.data.get('third_holder_name')
#         third_holder_dob            = request.data.get('third_holder_dob')
#         third_pan_holder            = request.data.get('third_pan_holder')
#         status                      = request.data.get('status')
#         gender                      = request.data.get('gender')
#         occupation_code             = request.data.get('occupation_code')

#         logger.info(f'''
#             user_id                 : {user_id}
#             client_code             : {client_code}
#             investor_category       : {investor_category}
#             tax_status              : {tax_status}
#             holding_nature          : {holding_nature}
#             primary_holder_name     : {primary_holder_name}
#             primary_holder_dob      : {primary_holder_dob}

#             secondary_holder_name   : {secondary_holder_name}
#             secondary_holder_dob    : {secondary_holder_dob}
#             secondary_pan_holder    : {secondary_pan_holder}
            
#             third_holder_name       : {third_holder_name}
#             third_holder_dob        : {third_holder_dob}
#             third_pan_holder        : {third_pan_holder}
#             status                  : {status}
#             gender                  : {gender}
#             occupation_code         : {occupation_code}
#         ''')
#         if Registration_mfu_details.objects.filter(USER=user_id).exists():
#             a = Registration_mfu_details.objects.get(USER=user_id)
#         else:
#             a = Registration_mfu_details.objects.create(
#                 USER = Registration_personal_details.objects.get(id=user_id),
#             )
#         a.CLIENT_CODE           = client_code
#         a.INVESTOR_CATEGORY     = Investor_category_master.objects.get(id=investor_category)
#         a.TAX_STATUS            = Tax_status_master.objects.get(id=tax_status)
#         a.HOLDING_NATURE        = Holding_nature_master.objects.get(id=holding_nature)
#         a.PRIMARY_HOLDER_NAME   = primary_holder_name
#         a.PRIMARY_HOLDER_DOB    = primary_holder_dob
#         a.STATUS                = status
#         a.GENDER                = gender
#         a.OCCUPATION_CODE       = Occupation_master.objects.get(id=occupation_code)
    
#         if Holding_nature_master.objects.get(id=holding_nature).CODE != "SI":
#             logger.info(f"enterHolding_nature")
#             a.SECONDARY_PAN_HOLDER  = request.data.get('secondary_pan_holder')
#             a.SECONDARY_HOLDER_NAME = request.data.get('secondary_holder_name')
#             a.SECONDARY_HOLDER_DOB  = request.data.get('secondary_holder_dob')
#             a.THIRD_PAN_HOLDER      = request.data.get('third_pan_holder')
#             a.THIRD_HOLDER_NAME     = request.data.get('third_holder_name')
#             a.THIRD_HOLDER_DOB      = request.data.get('third_holder_dob')
#         a.save()
#         return JsonResponse("success",safe=False,status=200)
#     except Exception as e:
#         logger.exception(e)
#         return JsonResponse("something went wrong",safe=False,status=500)

@api_view(['POST'])
def registration3(request):
    try:
        user_id             = request.data.get("user_id")
        app_type            = request.data.get("app_type")
        api_use             = request.data.get("api_use")
        # cancelled_check = request.data.getlist('[cancelled_check[]')
        # cancelled_check = request.data.getlist('cancelled_check[]')
        # latest_account_statement = request.data.getlist('latest_account_statement[]')
        # signature           = request.data.getlist('signature[]')
        acc_no              = request.data.getlist('acc_no')
        acc_type            = request.data.getlist('acc_type')
        bank                = request.data.getlist('bank')
        micr_no             = request.data.getlist('micr_no')
        neft_ifsc           = request.data.getlist('ifsc_code')
        # neft_ifsc           = request.data.getlist('neft_ifsc[]')
        # bank_name = request.data.getlist('bank_name[]')
        bank_proof          = request.data.getlist('bank_proof')
        bank_proof_file     = request.FILES.getlist('bank_proof_file')
        # bank_proof_file     = request.data.getlist('bank_proof_file')
        default             = request.data.get('default')

        logger.info(f'''
            api_use         = {api_use}
            user_id         = {user_id}
            app_type        = {app_type}
            acc_no          = {acc_no}
            acc_type        = {acc_type}
            bank            = {bank}
            micr_no         = {micr_no}
            neft_ifsc       = {neft_ifsc}
            bank_proof      = {bank_proof}
            bank_proof_file = {bank_proof_file}

            default         = {default}
        ''')
        
        if user_id and user_id != "undefined":
            Registration_bank_details.objects.filter(USER=user_id).update(IS_DELETED=True)
            # a = Registration_bank_details.objects.create(
            #     USER = Registration_personal_details.objects.get(id=user_id)
            # )
            for i in range(len(bank)):
                if acc_no[i] != "" and acc_type[i] and bank[i] != "" and micr_no[i] != "" and neft_ifsc[i] != "" and bank_proof[i] != "":
                    b = Registration_bank_details.objects.create(
                        # REG_BANK        = a,
                        USER            = Registration_personal_details.objects.get(id=user_id),
                        # CANCELLED_CHECK = cancelled_check[i],
                        # LATEST_ACCOUNT_STATEMENT = latest_account_statement[i],
                        # SIGNATURE       = signature[i],
                        ACC_NO          = acc_no[i],
                        ACC_TYPE        = Bank_account_type_master.objects.get(id=acc_type[i]),
                        BANK_NAME       = Bank_master.objects.get(id=bank[i]),
                        MICR_NO         = micr_no[i],
                        IFSC_CODE       = neft_ifsc[i],
                        # BANK_NAME = bank_name[i],
                        BANK_PROOF      = Bank_proof_master.objects.get(CODE=bank_proof[i]),
                        BANK_PROOF_FILE = bank_proof_file[i],
                    )
                    
                    # logger.info(f"iiii = i {i+1}")
                    if int(default) == i+1:
                        b.DEFAULT_BANK = True
                        b.save()
                # else:
                #     logger.info(f"Please fill require field")
            mfu = Registration_mfu_details.objects.get(USER=user_id)
            if mfu.INVESTOR_CATEGORY.CODE == "M":
                if api_use == "CM":
                    api_use = "CM"
                else:
                    api_use = "CR"
                data , status = mfu_registration(user_id,app_type,api_use)
                if status == 404:
                    return JsonResponse("Some error occurred. Please try again after some time. If problem persists; Contact Administrator.",safe=False,status=412)
                else:
                    return JsonResponse({"data":data},safe=False,status=200)
            return JsonResponse("Bank Details Added Successfully",safe=False,status=200)
        return JsonResponse("Please Contact Administrator",safe=False,status=412)
    except Exception as e:
        logger.exception(e)
        return JsonResponse("something went wrong",safe=False,status=500)

@api_view(["POST"])
def registration4(request):
    try:
        #nominee registartion
        user_id                     = request.data.get("user_id")
        nominee_option              = request.data.get('want_nominee')
        nominee_verification_type   = request.data.get('nominee_verification_type')
        nominees                    = request.data.get('nominees')
        app_type                    = request.data.get('app_type')
        api_use                     = request.data.get('api_use')
        

        logger.info(f'''

            user_id                     = {user_id}
            nominee_option              = {nominee_option}
            nominee_verification_type   = {nominee_verification_type}
            nominees                    = {nominees}
            app_type                    = {app_type}
        ''')
        # Registration_nominee_details.objects.filter(USER=user_id).update(IS_DELETED=True)
        if user_id and user_id != "undefined":

            Nominee_details.objects.filter(USER=user_id).update(IS_DELETED=True)
            
            if nominee_option == "Y":
                # logger.info(f"1")
                # if type(nominees) is str:
                #     logger.info(f"2")
                #     nominees = json.loads(nominees)
                for i in range(len(nominees)):
                    # logger.info(f"3")
                    logger.info(f"nominee{i} = {nominees[i]}")
                    if nominees[i]['nominee_name'] is not None:
                        b = Nominee_details.objects.create(
                            USER                        = Registration_personal_details.objects.get(id=user_id),
                            NOMINEE_NAME                = nominees[i]['nominee_name'],
                            RELATIONSHIP_WITH_CLIENT    = nominees[i]['relationship_with_client'],
                            NOMINEE_PERCENTAGE          = nominees[i]['nominee_percentage'],
                            NOMINEE_DOB                 = nominees[i]['nominee_dob'],
                        )
                        
                        if nominees[i]['nominee_is_minor'] == "yes":
                            b.NOMINEE_IS_MINOR = True
                            b.GUARDIAN_NAME               = nominees[i]['guardian_name']
                            b.GUARDIAN_RELATION           = nominees[i]['guardian_relation']
                            b.GUARDIAN_DOB                = nominees[i]['guardian_dob']
                            
                        else:
                            b.NOMINEE_IS_MINOR = False
                        b.save()
            if Registration_nominee_details.objects.filter(USER=user_id).exists():
                    a = Registration_nominee_details.objects.get(USER=user_id)
            else:
                a = Registration_nominee_details.objects.create(
                    USER                        = Registration_personal_details.objects.get(id=user_id),
                )
            a.NOMINEE_OPTION              = nominee_option
            if nominee_option == "X":
                a.NOMINEE_VERIFICATION_TYPE   = "X"
            else:
                a.NOMINEE_VERIFICATION_TYPE   = nominee_verification_type
            a.save()

            # return JsonResponse("Success",safe=False,status=200)
            if api_use == "CM":
                api_use = "CM"
            else:
                api_use = "CR"
            logger.info(f"""
                user_id = {user_id}
                app_type = {app_type}
                api_use = {api_use}
            """)
            data , status = mfu_registration(user_id,app_type,api_use)
            if status == 404:
                return JsonResponse("Some error occurred. Please try again after some time. If problem persists; Contact Administrator.",safe=False,status=412)
            else:
                return JsonResponse({"data":data},safe=False,status=200)
        return JsonResponse("Please Contact Administrator",safe=False,status=412)
    except Exception as e:
        logger.exception(e)
        return JsonResponse("something went wrong",safe=False,status=500)
    
def manual_mfu_registration(request,id):
    try:
        app_type = "uat"
        api_use = "CM"
        mfu_registration(id,app_type,api_use)
        return JsonResponse("Suceess",safe=False,status=200)
    except Exception as e:
        logger.exception(f"{e}")
        return JsonResponse(f"{e}",safe=False,status=500)

def manual_file_upload(request,id):
    try:
        app_type = "prod"
        file_upload(id,app_type)
        return JsonResponse("Suceess",safe=False,status=200)
    except Exception as e:
        logger.exception(f"{e}")
        return JsonResponse(f"{e}",safe=False,status=500)

def mfu_registration(id,app_type,api_use):
    try:
        payload = can_registration_api(id,app_type,api_use)
        logger.info(f"payload = {payload}")
        header_checklist    = Header_Checklist.objects.get(APP_TYPE=app_type,CHECKLIST_USE_FOR="can",IS_DELETED=False)
        headers = {
            'Content-Type': 'application/xml'
        }
        url = f"{header_checklist.BASE_URL}/MFUCanFillEezzService"
        response = requests.request("POST", url, headers=headers, data=payload, verify=False)
        status = response.status_code
        if status == 404:
            data = []
        else:
            # logger.info(f"response = {response.status_code}")
            if response.text:
                temp = xmltodict.parse(response.text)
                json_data = json.dumps(temp,indent = 2)
                data = json.loads(json_data)

                # logger.info(f"mfu_registration response = \n{json_data}")
                # logger.info(f"mfu_registration response new = \n{data}")
                dict = data["CANIndFillEezzResp"]["RESP_BODY"]
                r = Registration_personal_details.objects.get(id=id)
                if data["CANIndFillEezzResp"]["RESP_HEADER"]["RES_MSG"] == "Success":
                    logger.info(f"""
                                if Sucess
                        can_no      = {dict['CAN'] }
                        NOM_LINK_1 = {dict['NOM_VER_LINK_H1']}
                        NOM_LINK_2 = {dict['NOM_VER_LINK_H2']}
                        NOM_LINK_3 = {dict['NOM_VER_LINK_H3']}
                    """)
                    
                    r.CAN           = dict["CAN"]
                    r.NOM_LINK_1    = dict['NOM_VER_LINK_H1']
                    r.NOM_LINK_2    = dict['NOM_VER_LINK_H2']
                    r.NOM_LINK_3    = dict['NOM_VER_LINK_H3']
                    r.APP_TYPE      = app_type
                    r.save()
                    if api_use != "CM":
                        file_upload(id,app_type)
                elif data["CANIndFillEezzResp"]["RESP_HEADER"]["RES_MSG"] == "Your Data Will Update Soon":
                    add_res, created = can_creation_request_response.objects.get_or_create(
                        USER        = r
                    )
                    add_res.REQUEST     = payload
                    add_res.RESPONSE    = data
                    add_res.save()
                    logger.info(f"""
                                Your Data Will Update Soon
                                can_no = {dict['CAN'] }
                                NOM_LINK_1 = {dict['NOM_VER_LINK_H1']}
                                NOM_LINK_2 = {dict['NOM_VER_LINK_H2']}
                                NOM_LINK_3 = {dict['NOM_VER_LINK_H3']}
                                """)
                else:
                    logger.info(f"mfu_registration response = \n{data}")
            else:
                data = []
        return data,status

        # return JsonResponse(data,safe=False,status=200)
        # return data
        # if file_upload(id):
        #     # return JsonResponse(data,safe=False,status=200)
        #     return True,data
        # else:
        #     return False,data
        
        # return JsonResponse("hellow",safe=False,status=200)
    except Exception as e:
        logger.exception(e)
        return JsonResponse("something went wrong",safe=False,status=500)

    
# --------------------------------------- MFU Can Creation End -----------------------------------
# def mfu_file_upload(request,id):
# def mfu_file_upload(id,app_type):
#     try:
#         file_upload(id,app_type)
#         return True
#     except Exception as e:
#         logger.exception(e)
#         return JsonResponse("something went wrong",safe=False,status=500)
@api_view(['POST'])
def user_banks(request):
    try:
        user_id = request.data.get("user_id")
        logger.info(f"entere user_banks  = {user_id}")
        data =  list(Registration_bank_details.objects.filter(USER=user_id,IS_DELETED=False).values('id',"ACC_NO","BANK_NAME__CODE","BANK_NAME__NAME","BANK_NAME__PD","BANK_NAME__PN"))
        
        return JsonResponse(data,safe=False,status=200)
    except Exception as e:
        logger.exception(e)
        return JsonResponse("something went wrong",safe=False,status=500)
 #logger.info(f"date = {today_date} , timedelta(days=2) = {timedelta(days=2)}")

    
    # tmp = [
    #     f"sessioncontext={session.SESSIONCONTEXT}",
    #     f"sendersubid={session.SENDERSUBID}",
    #     f"logTp=A",
    #     f"regMode=PD",
    #     f"entityId=40007K",
    #     f"reqType=A",
    #     f"can=14162ANA02",
    #     f"riaNo=",
    #     f"arnNo=ARN-5001",
    #     f"subBrokArn=",
    #     f"subBrokCode=",
    #     f"euincode=E249588",
    #     f"bankId=240",
    #     f"bankName=HDFC BANK LTD",
    #     f"micrCode=400240003",
    #     f"ifscCode=HDFC0000001",
    #     f"accNo=50100015780210",
    #     f"accType=SB",
    #     f"maxAmt=1000",
    #     f"perpetualFlag=Y",
    #     f"startDate={today_date}",
    #     f"endDate="
    # ]
    # {profile.CAN}

@api_view(['POST'])
def mfu_payeezz_registration(request):
    try:
        user_id         = request.data.get("user_id")
        app_type        = request.data.get("app_type")
        mandate_bank    = request.data.get("mandate_bank")
        account_type    = request.data.get("account_type")
        auth_mode       = request.data.get("auth_mode")
        max_amount      = request.data.get("max_amount")
        start_date      = request.data.get("start_date")
        end_date        = request.data.get("end_date")

        logger.info(f"""
            user_id         = {user_id}
            app_type        = {app_type}
            account_type    = {account_type}
            mandate_bank    = {mandate_bank}
            auth_mode       = {auth_mode}
            max_amount      = {max_amount}
            start_date      = {start_date}
            end_date        = {end_date}
        """)
        if user_id:
            header_data = header_checklist_data(app_type,'transaction')
            profile         = Registration_personal_details.objects.get(id=user_id)
            Bank_dtl        = Registration_bank_details.objects.get(id=mandate_bank)
            session         = investology_login_session.objects.get(APP_TYPE=app_type)
            
            # today_date = date.today() + timedelta(days=2)
            headers = {
                'Content-Type': 'application/xml'
            }
            url = f"{header_data.BASE_URL}/APIePayEezzService.do?sendResponseFormat=JSON&"
            tmp = [
                f"sessioncontext={session.SESSIONCONTEXT}",
                f"sendersubid={session.SENDERSUBID}",
                "logTp=A",
                f"regMode={auth_mode}",
                f"entityId={header_data.ENTITY_ID}",
                "reqType=A",
                f"can={profile.CAN}",
                "riaNo=",
                "arnNo=ARN-195775",
                "subBrokArn=",
                "subBrokCode=",
                "euincode=",
                f"accNo={Bank_dtl.ACC_NO}",
                f"accType={Bank_dtl.ACC_TYPE.BANK_ACCOUNT_TYPE}",
                f"bankId={Bank_dtl.BANK_NAME.CODE}",
                f"ifscCode={Bank_dtl.IFSC_CODE}",
                f"micrCode={Bank_dtl.MICR_NO}",
                f"bankName={Bank_dtl.BANK_NAME.NAME}",
                f"maxAmt={max_amount}",
                "perpetualFlag=N",
                f"startDate={start_date}",
                f"endDate={end_date}"
            ]

            url = url + "&".join(tmp)
            response = requests.get(url, headers=headers, verify=False)
            text = json.loads(response.text)
            logger.info(f'response_text = {text}')

            if text["respStatus"] == "0":
                success = text["addResp"]
                data_response = {
                    "mmrn"          : success["mmrn"],
                    "approveLink"   : success["approveLink"],
                    "uniqueRefNo"   : success["uniqueRefNo"]
                }
                edit                    = Registration_bank_details.objects.get(id=mandate_bank)
                edit.MANDATE_BANK       = True
                edit.MMRN               = success["mmrn"]
                edit.APPROVELINK        = success["approveLink"]
                edit.UNIQUEREFNO        = success["uniqueRefNo"]
                edit.TRANSACTION_LIMIT  = max_amount
                edit.MANDATE_START_DATE = start_date
                edit.MANDATE_END_DATE   = end_date
                edit.save()
                
            else:
                data_response = {
                    "errorMessage" : text["errorMessage"]
                }

            logger.info(f"data_response = {data_response}")
            return JsonResponse(data_response,safe=False,status=200)
        return JsonResponse("User id not fetching",safe=False,status=500)
    except Exception as e:
        logger.exception(e)
        return JsonResponse("something went wrong",safe=False,status=500)

# @api_view(['POST'])
# def mfu_payeezz_validation(request):
def mfu_payeezz_validation(user_id,app_type):
    try:
        header_data     = header_checklist_data(app_type,'transaction')
        profile         = Registration_personal_details.objects.get(id=user_id)
        session         = investology_login_session.objects.get(APP_TYPE=app_type)
        mandate_bank_data = Registration_bank_details.objects.filter(USER_id=user_id,IS_DELETED=False,MANDATE_BANK=True)

        if mandate_bank_data.count() > 0:
            for i in mandate_bank_data:
                if i.MMRN_REG_STATUS != "PA" and i.MMRN_AGGR_STATUS != "AK" and i.MANDATE_BANK is True:
                # logger.info("ifif")
                    headers = {
                        'Content-Type': 'application/xml'
                    }
                    url = f"{header_data.BASE_URL}/APIEPayEezzStatusService.do?sendResponseFormat=JSON&"
                    tmp = [
                        f"sessioncontext={session.SESSIONCONTEXT}",
                        f"sendersubid={session.SENDERSUBID}",
                        "logTp=A",
                        f"can={profile.CAN}",
                        f"mmrn={i.MMRN}"
                    ]
                    url = url + "&".join(tmp)
                    
                    response = requests.get(url, headers=headers, verify=False)
                    text = json.loads(response.text)
                    logger.info(f"text = {text}")
                    if text["respStatus"] == "0":
                        success = text["epayStatusResponse"][0]

                        i.MMRN_REG_STATUS   = success["mmrnRegStatus"]
                        i.MMRN_AGGR_STATUS  = success["mmrnAggrStatus"]
                        i.PRN               = success["prn"]
                        i.save()
                    else:
                        data_response = {
                            "errorMessage" : text["errorMessage"]
                        }
                        logger.info(f"""
                            can             = {profile.CAN}
                            mmrn            = {i.MMRN}
                            data_response   = {data_response}
                            """)
        return True
    except Exception as e:
        logger.exception(f"{e}")
        return JsonResponse(f"{e}",safe=False,status=500)

def mfu_can_validation(user_id,app_type):
    try:
        profile         = Registration_personal_details.objects.get(id=user_id)
        # can_status_choices = (
        #     ('AP','Approved'),
        #     ('PE','Pending'),
        #     ('RJ','Rejected')
        # )
        if profile.CAN_STATUS != "AP":
            header_data     = header_checklist_data(app_type,'transaction')
            
            session         = investology_login_session.objects.get(APP_TYPE=app_type)
            mfu             = Registration_mfu_details.objects.get(USER=user_id)

            if mfu.INVESTOR_CATEGORY.CODE == "M":
                holder = Registration_holder_details.objects.get(USER=user_id,HOLDER_TYPE="GU",IS_DELETED=False)  
            else:
                holder = Registration_holder_details.objects.get(USER=user_id,HOLDER_TYPE="PR",IS_DELETED=False)
            
            
            headers = {
                'Content-Type': 'application/xml'
            }
            url = f"{header_data.BASE_URL}/APICANValidationService.do?sendResponseFormat=JSON&"
            tmp = [
                f"sessioncontext={session.SESSIONCONTEXT}",
                f"sendersubid={session.SENDERSUBID}",
                "logTp=A",
                f"can={profile.CAN}",
                f"entityId={header_data.ENTITY_ID}",
                f"pan={profile.PAN_NO}",
                f"dob={holder.HOLDER_DOB}",
                f"emailId={holder.PRI_EMAIL}",
            ]
            url = url + "&".join(tmp)
            
            response = requests.get(url, headers=headers, verify=False)
            text = json.loads(response.text)
            logger.info(f"text = {text}")
            if text["respStatus"] == "0":
                # if text["responseList"]["canStatus"] != "OH":
                status = text["responseList"]["canStatus"]
                profile.CAN_STATUS = status
                profile.save()
            # else:
            #     data_response = {
            #         "errorMessage" : text["errorMessage"]
            #     }
        return True
    except Exception as e:
        logger.exception(e)
        return JsonResponse("something went wrong",safe=False,status=500)


def load_scheme_category(request):
    try:
        data = list(Scheme_category.objects.values("id","CATEGORY"))
        return JsonResponse(data,safe=False,status=200)
    except Exception as e:
        logger.exception(f"{e}")
        return JsonResponse(f"{e}",safe=False,status=500)

def load_scheme_sub_category(request):
    try:
        category = request.GET.get("category")
        # category1 = request.data.get("category")
        logger.info(f"category = {category}")
        # logger.info(f"category1 = {category1}")
        data = list(Scheme_sub_category.objects.filter(CATEGORY=category).values("id","SUB_CATEGORY"))
        return JsonResponse(data,safe=False,status=200)
    except Exception as e:
        logger.exception(e)
        return JsonResponse("something went wrong",safe=False,status=500)

def scheme_name_api(request):
    try:
        amc_name            = request.GET.get("amc_name")
        sub_category        = request.GET.get("sub_category")
        kwargs = {}
        kwargs['PLAN_TYPE']         = "REG"
        if amc_name is not None:
            kwargs['FUND_CODE__FUND_CODE']       = amc_name
        if sub_category is not None:
            kwargs['CATEGORY__id']  = sub_category
        data = list(Schemes.objects.filter(**kwargs).values("id","PLAN_NAME"))
        return JsonResponse(data,safe=False,status=200)
    except Exception as e:
        logger.exception(f"{e}")
        return JsonResponse(f"{e}",safe=False,status=500)


def search_funds(request):
    try:
        amc_name            = request.GET.get("amc_name")
        category            = request.GET.get("category")
        sub_category        = request.GET.get("sub_category")
        scheme_name         = request.GET.get("scheme_name")
        plan_type           = request.GET.get("plan_type")

        exclude_scheme_id   = request.GET.get("exclude_scheme_id")
        # scheme_type     = "DIV"
        # plan_type       = "DIR"
        # skip            = request.GET.get("skip")
        # limit           = request.GET.get("limit")
        # count           = request.GET.get("count")

        scheme_for      = request.GET.get("scheme_for")
        # PUR_ALLOWED
        # REDEEM_ALLOWED
        # SIP_ALLOWED
        # SWITCH_OUT_ALLOWED
        # SWITCH_IN_ALLOWED
        # STP_OUT_ALLOWED
        # STP_IN_ALLOWED
        # SWP_ALLOWED
        # skip            = {skip}
            # limit           = {limit}
            # count           = {count}

        logger.info(f"""
            amc             = {amc_name}
            category        = {category}
            sub_category    = {sub_category}
            scheme_name     = {scheme_name}
            plan_type     = {plan_type}
            exclude_scheme_id     = {exclude_scheme_id}
            scheme_for      = {scheme_for}
            """)
        kwargs = {}
        exclude = {}
        kwargs['PLAN_TYPE__exact']          = "REG"
        kwargs['FUND_CODE__FUND_CODE']      = amc_name
        kwargs['SCHEME_TYPE']               = "OE"
        kwargs['NFO_ALLOWED']               = "N"

        

        threshold_schme = {}
        threshold_schme['FUND_CODE__FUND_CODE'] = amc_name
        
        if scheme_for  == "purchase":
            kwargs['PUR_ALLOWED']       = "Y"
            txn_type = "B"
        if scheme_for  == "redeem":
            kwargs['REDEEM_ALLOWED']    = "Y"
        if scheme_for  == "sip":
            kwargs['SIP_ALLOWED']       = "Y"
            txn_type = "V"
            threshold_schme['SYS_FREQ__icontains'] = "M"

        if scheme_for  == "switch":
            kwargs['SWITCH_IN_ALLOWED']    = "Y"
            exclude['id']                  = exclude_scheme_id
            txn_type = "S"

        if scheme_for  == "stp":
            kwargs['STP_IN_ALLOWED']    = "Y"
            exclude['id']                  = exclude_scheme_id
            txn_type = "E"


        if category and category != "":
            kwargs['CATEGORY__CATEGORY__id']  = category
        if sub_category and sub_category != "":
            kwargs['CATEGORY__id']  = sub_category
        if scheme_name:
            kwargs['PLAN_NAME__icontains']            = scheme_name
        if plan_type:
            kwargs['PLAN_OPT__icontains']      = plan_type

        # if txn_type:
        if txn_type:
            threshold_schme['TXN_TYPE'] = txn_type
        # Fetch all the relevant min amounts per SCHEME_CODE for the given txn_type
            threshold_data = Threshold.objects.filter(
                FUND_CODE__FUND_CODE=amc_name,
                TXN_TYPE=txn_type,
            ).values('SCHEME_CODE').annotate(min_amt=Min('MIN_AMT'))

        # Create a mapping of SCHEME_CODE -> MIN_AMT
            threshold_mapping = {item['SCHEME_CODE'].strip(): item['min_amt'] for item in threshold_data}
        else:
            threshold_mapping = {}
            # threshold_subquery = Subquery(
            #     Threshold.objects.filter(
            #         FUND_CODE__FUND_CODE=amc_name,
            #         SCHEME_CODE=OuterRef('SCHEME_CODE'),
            #         TXN_TYPE=txn_type
            #     # ).values('MIN_AMT')
            #     # ).values('MIN_AMT').order_by("-MIN_AMT")
            #     ).annotate(max_amt=Min('MIN_AMT')).values('max_amt')[:-1]
            # )
            # threshold_subquery = Subquery(
            #     Threshold.objects.filter(
            #         FUND_CODE__FUND_CODE=amc_name,
            #         SCHEME_CODE=OuterRef('SCHEME_CODE'),
            #         TXN_TYPE=txn_type
            #     ).order_by('-MIN_AMT')  # Ordering by MIN_AMT to get the smallest
            #     .values('MIN_AMT')[:1]  # Fetching only the first value (smallest)
            # )
        # else:
        #     threshold_subquery = 0
        
        v = ["id","CATEGORY__CATEGORY__CATEGORY","CATEGORY__SUB_CATEGORY","FUND_CODE__FUND_NAME","FUND_CODE__FUND_CODE","PLAN_NAME","SCHEME_CODE","DIV_OPT","REOPEN_DATE"]

        schemes_data = Schemes.objects.filter(**kwargs).values(*v).exclude(**exclude).order_by("-id")

        result_data = []
        for scheme in schemes_data:
            scheme_code = scheme['SCHEME_CODE'].strip()
            min_amt = threshold_mapping.get(scheme_code, 0)  # Get MIN_AMT if exists, else 0
            scheme['MIN_AMT'] = min_amt
            result_data.append(scheme)
        # if threshold_subquery:
        #     data = list(Schemes.objects.filter(**kwargs).annotate(
        #         MIN_AMT=threshold_subquery
        #     ).values(*v, 'MIN_AMT').order_by("-id"))
        # else:
        #     data = list(Schemes.objects.filter(**kwargs).values(*v).order_by("-id"))

        return JsonResponse(result_data,safe=False,status=200)
    except Exception as e:
        logger.exception(e)
        return JsonResponse("something went wrong",safe=False,status=500)
    
# def get_nfo_data(request):
#     kwargs                              = {}
#     exclude                             = {}
#     today_date                          = datetime.today()
#     threshold_schme                     = {}
#     txn_type                            = "N"
#     kwargs['PLAN_TYPE__exact']          = "REG"
#     # kwargs['FUND_CODE__FUND_CODE']      = amc_name
#     kwargs['SCHEME_TYPE']               = "OE"
#     kwargs['NFO_ALLOWED']         = "Y"
#     threshold_schme['TXN_TYPE'] = txn_type
# # Fetch all the relevant min amounts per SCHEME_CODE for the given txn_type
#     threshold_data = Threshold.objects.filter(
#         # FUND_CODE__FUND_CODE=amc_name,
#         TXN_TYPE=txn_type
#     ).values('SCHEME_CODE').annotate(min_amt=Min('MIN_AMT'))

#     # Create a mapping of SCHEME_CODE -> MIN_AMT
#     threshold_mapping = {item['SCHEME_CODE']: item['min_amt'] for item in threshold_data}


#     v = ["id","CATEGORY__CATEGORY__CATEGORY","CATEGORY__SUB_CATEGORY","FUND_CODE__FUND_NAME","FUND_CODE__FUND_CODE","PLAN_NAME","SCHEME_CODE","DIV_OPT"]

#     schemes_data = Schemes.objects.filter(**kwargs,NFO_END__gte=today_date).values(*v).order_by("-id")

#     result_data = []
#     for scheme in schemes_data:
#         scheme_code = scheme['SCHEME_CODE']
#         min_amt = threshold_mapping.get(scheme_code, 0)  # Get MIN_AMT if exists, else 0
#         scheme['MIN_AMT'] = min_amt
#         result_data.append(scheme)
#     return JsonResponse(result_data,safe=False,status=200) 

def get_nfo_data(request):
    try:
        kwargs = {}
        exclude = {}
        today_date = datetime.today()
        threshold_schme = {}
        txn_type = "N"

        kwargs['PLAN_TYPE__exact'] = "REG"
        kwargs['SCHEME_TYPE'] = "OE"
        kwargs['NFO_ALLOWED'] = "Y"
        threshold_schme['TXN_TYPE'] = txn_type

        # Fetch all the relevant min amounts per SCHEME_CODE for the given txn_type
        threshold_data = Threshold.objects.filter(
            TXN_TYPE=txn_type
        ).values('SCHEME_CODE').annotate(min_amt=Min('MIN_AMT'))

        # Log threshold data for debugging
        # logger.info(f"Threshold Data: {list(threshold_data)}")

        # Create a mapping of SCHEME_CODE -> MIN_AMT
        threshold_mapping = {item['SCHEME_CODE'].strip(): item['min_amt'] for item in threshold_data}
        # logger.info(f"Threshold Mapping: {threshold_mapping}")

        v = [
            "id",
            "CATEGORY__CATEGORY__CATEGORY",
            "CATEGORY__SUB_CATEGORY",
            "FUND_CODE__FUND_NAME",
            "FUND_CODE__FUND_CODE",
            "PLAN_NAME",
            "SCHEME_CODE",
            "DIV_OPT",
            "REOPEN_DATE"
        ]

        schemes_data = Schemes.objects.filter(
            **kwargs, NFO_END__gte=today_date
        ).values(*v).order_by("-id")

        # logger.info(f"Fetched Schemes Data: {list(schemes_data)}")

        result_data = []
        for scheme in schemes_data:
            scheme_code = scheme['SCHEME_CODE']
            min_amt = threshold_mapping.get(scheme_code, 0)  # Get MIN_AMT if exists, else 0
            # logger.debug(f"Scheme Code: {scheme_code}, MIN_AMT: {min_amt}")
            scheme['MIN_AMT'] = min_amt
            result_data.append(scheme)

        # logger.info(f"Result Data: {result_data}")
        return JsonResponse(result_data, safe=False, status=200)
    except Exception as e:
        logger.exception(f"{e}")
        return JsonResponse(f"{e}",safe=False,status=500)

# Monthly Hundred sip
@api_view(["POST"])
def start_sip_hundred(request):
    try:
        kwargs = {}
        kwargs['PLAN_TYPE']         = "REG"
        kwargs['SIP_ALLOWED']       = "Y"
        kwargs['SIP_HUNDRED']       = True
        

        # Filter Threshold as before
        data = list(Threshold.objects.filter(
            TXN_TYPE__icontains="V",
            MIN_AMT=100.00,  # Minimum amount is 100
            SYS_FREQ__icontains='M'  # Filtering for monthly frequency
        ).values('FUND_CODE__FUND_NAME', 'SCHEME_CODE', 'MIN_AMT').order_by("FUND_CODE__FUND_NAME"))

        # Fetch all matching schemes in one query
        fund_names = [i["FUND_CODE__FUND_NAME"] for i in data]
        scheme_codes = [i["SCHEME_CODE"] for i in data]

        schemes = Schemes.objects.filter(
            FUND_CODE__FUND_NAME__in=fund_names,
            SCHEME_CODE__in=scheme_codes,
            **kwargs,
            
        ).values('id','DIV_OPT','FUND_CODE__FUND_NAME', 'SCHEME_CODE', 'CATEGORY__CATEGORY__CATEGORY', 'CATEGORY__SUB_CATEGORY', 'PLAN_NAME').order_by("-PLAN_NAME")

        ''' Create a lookup dictionary for fast access '''
        scheme_lookup = {
            (s['FUND_CODE__FUND_NAME'], s['SCHEME_CODE']): s for s in schemes
        }

        '''Update data based on scheme_lookup'''
        filtered_data = []
        for idx, i in enumerate(data):
            key = (i["FUND_CODE__FUND_NAME"], i["SCHEME_CODE"])
            if key in scheme_lookup:
                i["id"]         = scheme_lookup[key]["id"]
                i["DIV_OPT"]    = scheme_lookup[key]["DIV_OPT"]
                i["CATEGORY__CATEGORY__CATEGORY"] = scheme_lookup[key]["CATEGORY__CATEGORY__CATEGORY"]
                i["CATEGORY__SUB_CATEGORY"] = scheme_lookup[key]["CATEGORY__SUB_CATEGORY"]
                i["PLAN_NAME"] = scheme_lookup[key]["PLAN_NAME"]
                filtered_data.append(i)
        data = filtered_data
        logger.info(f"len filtered_data = {len(filtered_data)}")
        return JsonResponse(data,safe=False,status=200)
    except Exception as e:
        logger.exception(e)
        return JsonResponse("something went wrong",safe=False,status=500)



# def frequency_min_amt(request):
#     amc_name        = request.GET.get("amc_name")
#     frequency       = request.GET.get("frequency")
#     scheme_code     = request.GET.get("scheme_code")
#     txn_type        = request.GET.get("txn_type")
#     logger.info(f"""
#         amc_name    = {amc_name}
#         frequency   = {frequency}
#         scheme_code = {scheme_code}
#         txn_type    = {txn_type}
#     """)
#     data = list(Threshold.objects.filter(
#         FUND_CODE__FUND_CODE    = amc_name,
#         SCHEME_CODE             = scheme_code,
#         TXN_TYPE                = txn_type,
#         SYS_FREQ                = frequency
#     ).values("MIN_AMT","SYS_FREQ_OPT","SYS_DATES"))

#     return JsonResponse(data,safe=False,status=200)

# rushikesh



def load_divident(request):
    try:
        id = request.GET.get("plan_id")
        data = list(Schemes.objects.filter(id=id).values("DIV_OPT"))
        return JsonResponse(data,safe=False,status=200)
    except Exception as e:
        logger.exception(f"{e}")
        return JsonResponse(f"{e}",safe=False,status=500)

def user_payezz(request):
    try:
        data = investology_login_session.objects.last()
        logger.info(f"data = {data.SESSIONCONTEXT}")
        return JsonResponse("sucess",safe=False,status=200)
    except Exception as e:
        logger.exception(f"{e}")
        return JsonResponse(f"{e}",safe=False,status=500)

@api_view(["POST"])
def add_scheme_category(request):
    try:
        category = request.POST.get("category")
        category_id = request.POST.get("category_id")

        if Scheme_category.objects.filter(CATEGORY=category).exists():
            return JsonResponse("This Category Is Already Exist",safe=False,status=412)
        else:
            add = Scheme_category.objects.create(
                CATEGORY    = category,
                CATEGORY_ID = category_id
            )
            return JsonResponse("Category Add Successfully",safe=False,status=200)
    except Exception as e:
        logger.exception(e)
        return JsonResponse("something went wrong",safe=False,status=500)
    
def get_scheme_category(request,id):
    try:
        data = list(Scheme_category.objects.filter(id=id).values("id","CATEGORY","CATEGORY_ID"))
        return JsonResponse(data,safe=False)
    except Exception as e:
        logger.exception(f"{e}")
        return JsonResponse(f"{e}",safe=False,status=500)
    
@api_view(["POST"])
def edit_scheme_category(request,id):
    try:
        category = request.POST.get("category")
        category_id = request.POST.get("category_id")

        if Scheme_category.objects.filter(CATEGORY=category).exclude(id=id).exists():
            return JsonResponse("This Category Is Already Exist",safe=False,status=412)
        else:
            edit = Scheme_category.objects.get(id=id)
            edit.CATEGORY    = category
            edit.CATEGORY_ID = category_id
            edit.save()
            return JsonResponse("Category Edit Successfully",safe=False,status=200)
    except Exception as e:
        logger.exception(e)
        return JsonResponse("something went wrong",safe=False,status=500)

def load_scheme_category_table(request):
    try:
        data =  list(Scheme_category.objects.values("id","CATEGORY","CATEGORY_ID").order_by("-id"))
        return JsonResponse({"data":data},safe=False,status=200)
    except Exception as e:
        logger.exception(f"{e}")
        return JsonResponse(f"{e}",safe=False,status=500)

@api_view(["POST"])
def add_scheme_sub_category(request):
    try:
        category        = request.POST.get("category")
        sub_category    = request.POST.get("sub_category")
        sub_category_id = request.POST.get("sub_category_id")

        logger.info(f"""
            category            = {category}
            sub_category        = {sub_category}
            sub_category_id     = {sub_category_id}
        """)
        if Scheme_sub_category.objects.filter(CATEGORY__id=category,SUB_CATEGORY=sub_category).exists():
            return JsonResponse("This Sub Category Is Already Exist",safe=False,status=412)
        else:
            add = Scheme_sub_category.objects.create(
                CATEGORY    = Scheme_category.objects.get(id=category),
                SUB_CATEGORY = sub_category,
                SUB_CATEGORY_ID = sub_category_id
            )
        return JsonResponse("Category Add Successfully",safe=False,status=200)
    except Exception as e:
        logger.exception(e)
        return JsonResponse("something went wrong",safe=False,status=500)

def get_scheme_sub_category(request,id):
    try:
        data = list(Scheme_sub_category.objects.filter(id=id).values("id","CATEGORY","SUB_CATEGORY","SUB_CATEGORY_ID"))
        return JsonResponse(data,safe=False)
    except Exception as e:
        logger.exception(f"{e}")
        return JsonResponse(f"{e}",safe=False,status=500)

@api_view(["POST"])
def edit_scheme_sub_category(request,id):
    try:
        category        = request.POST.get("category")
        sub_category    = request.POST.get("sub_category")
        sub_category_id = request.POST.get("sub_category_id")

        if Scheme_sub_category.objects.filter(CATEGORY__id=category,SUB_CATEGORY=sub_category).exclude(id=id).exists():
            return JsonResponse("This Sub Category Is Already Exist",safe=False,status=412)
        else:
            edit = Scheme_sub_category.objects.get(id=id)
            edit.CATEGORY           = Scheme_category.objects.get(id=category)
            edit.SUB_CATEGORY       = sub_category
            edit.SUB_CATEGORY_ID    = sub_category_id
            edit.save()
        return JsonResponse("Sub Category Add Successfully",safe=False,status=200)
    except Exception as e:
        logger.exception(e)
        return JsonResponse("something went wrong",safe=False,status=500)
    
def load_sub_scheme_category(request):
    try:
        data =  list(Scheme_sub_category.objects.values("id","CATEGORY__CATEGORY","SUB_CATEGORY","SUB_CATEGORY_ID").order_by("-id"))
        return JsonResponse({"data":data},safe=False,status=200)
    except Exception as e:
        logger.exception(f"{e}")
        return JsonResponse(f"{e}",safe=False,status=500)


def calculate_quarterly_end_dates(input_date, no_of_installment):
    end_dates = [input_date]
    for i in range(1, int(no_of_installment) + 1):
        end_date = input_date + relativedelta(months=3*i)
        end_dates.append(end_date)
    # logger.info(f"end_dates = {end_dates}")
    return end_dates[-1]

@api_view(["POST"])
def add_cart_api(request):
    try:
        login_id            = request.data.get("login_id")
        buy_type            = request.data.get("buy_type")
        plan_name           = request.data.get("plan_name")
        follio_no           = request.data.get("follio_no") 
        goal                = request.data.get("goal")
        invest_amt          = request.data.get("invest_amt")
        day                 = request.data.get("day")
        start_month         = request.data.get("start_month")
        start_year          = request.data.get("start_year")
        end_month           = request.data.get("end_month")
        end_year            = request.data.get("end_year")
        nfo_allowed         = request.data.get("nfo_allowed")
        reopen_date         = request.data.get("reopen_date")
        
        
        # no_of_installment   = request.data.get("no_of_installment")
        frequency           = request.data.get("frequency")
        tarSchemeCode       = request.data.get("tarschemecode")
        dividendOption      = request.data.get("dividendoption")
        txnVolumeType       = request.data.get("txnvolumetype")
        
        logger.info(f"""
            login_id            = {login_id}
            buy_type            = {buy_type}
            plan_name           = {plan_name}
            follio_no           = {follio_no}
            goal                = {goal}
            dividendOption      = {dividendOption}
            invest_amt          = {invest_amt}
            frequency           = {frequency}
            day                 = {day}
            start_month         = {start_month}
            start_year          = {start_year}
            end_month           = {end_month}
            end_year            = {end_year}
            txnVolumeType       = {txnVolumeType}
            tarSchemeCode       = {tarSchemeCode}
            nfo_allowed         = {nfo_allowed}
        """)
        add = Cart.objects.create(
            USER                = Registration_personal_details.objects.get(id=login_id),
            PLAN_NAME           = Schemes.objects.get(id=plan_name),
            BUY_TYPE            = buy_type,
            FOLLIO_NO           = follio_no.split("/")[0],
            INVEST_AMT          = invest_amt,
            GOAL                = goal,
            DIVIDENDOPTION      = dividendOption
        )
        if nfo_allowed:
            add.NFO_ALLOWED     = True
            add.REOPEN_DATE     = reopen_date

        if buy_type == "sip" or buy_type == "swp" or buy_type == "stp":
            # input_date              = datetime(int(start_year), int(start_month), int(day))
            # if frequency == "M":
            #     end_date                = input_date + relativedelta(months=int(no_of_installment)-1)
            # if frequency == "Q":
            #     end_date                = calculate_quarterly_end_dates(input_date, no_of_installment)
            # logger.info(f"end_date = {end_date}")
                # end_date                = end_date[-1].strftime('%Y-%m-%d')
            add.FREQUENCY           = frequency
            add.DAY                 = day
            add.START_MONTH         = start_month
            add.START_YEAR          = start_year
            # add.NO_OF_INSTALLMENT   = no_of_installment
            add.END_MONTH           = end_month
            add.END_YEAR            = end_year

        if buy_type == "redemption" or buy_type == "switch" or buy_type == "stp":
            add.TXNVOLUMETYPE       = txnVolumeType

        if buy_type == "switch" or buy_type == "stp":
            add.TARSCHEMECODE       = Schemes.objects.get(id=tarSchemeCode)

        # if buy_type == "stp" :
        #     add.RTAAMCCODE          = rtaAmcCode
        #     add.TXNVOLUMETYPE       = txnVolumeType

        # if buy_type == "swp":
        #     add.RTASCHEMECODE       = rtaSchemeCode

        # if buy_type == "stp":
        #     add.TARSCHEMECODE       = tarSchemeCode
            # add.DIVIDENDOPTION      = dividendOption
            # add.EUINDECLARATION     = "Y"
        add.save()
        return JsonResponse("success",safe=False,status=200)
    except Exception as e:
        logger.info(e)
        return JsonResponse("something went wrong",safe=False,status=500)

@api_view(["POST"])
def edit_cart_api(request,id):
    try:
        buy_type    = request.data.get("buy_type")
        goal        = request.data.get("goal")
        invest_amt  = request.data.get("invest_amt")
        day         = request.data.get("day")
        frequency   = request.data.get("frequency")
        start_month = request.data.get("start_month")
        start_year  = request.data.get("start_year")
        end_month   = request.data.get("end_month")
        end_year    = request.data.get("end_year")
        txnvolumetype       = request.data.get("txnvolumetype")
        dividendOption      = request.data.get("dividendoption")
        # no_of_installment   = request.data.get("no_of_installment")
        # mutual_funds      # sip        # swp        # stp
        # logger.info(f"""
        #     buy_type   = {buy_type}
        #     goal       = {goal}
        #     min_amt    = {min_amt}
        # """)
        logger.info(f"dividendOption = {dividendOption}")
        edit = Cart.objects.get(id=id)
        edit.DIVIDENDOPTION      = dividendOption
        if buy_type == "mutual_funds" or buy_type == "additional_purchase":
            edit.GOAL        = goal
            edit.INVEST_AMT     = invest_amt
        if buy_type == "sip" or buy_type == "swp":
            # input_date = datetime(int(start_year), int(start_month), int(day))
            # end_date = input_date + relativedelta(months=int(no_of_installment)-1)
            edit.GOAL                = goal
            edit.INVEST_AMT          = invest_amt
            edit.DAY                 = day
            edit.FREQUENCY           = frequency
            edit.START_MONTH         = start_month
            edit.START_YEAR          = start_year
            # edit.NO_OF_INSTALLMENT   = no_of_installment
            edit.END_MONTH           = end_month
            edit.END_YEAR            = end_year
        if buy_type == "redemption":
            edit.TXNVOLUMETYPE       = txnvolumetype
        edit.save()
        return JsonResponse("success",safe=False,status=200)
    except Exception as e:
        logger.info(e)
        return JsonResponse("something went wrong",safe=False,status=500)

def fullform(data,buy_type):
    try:
        txn_volume_type_mapping = {
            "E": "All Units",
            "A": "Specific Amount",
            "U": "Specific Units",
        }
        frequency_mapping = {
            "D": "Daily",
            "W": "Weekly",
            "F": "Fortnightly",
            "M": "Monthly",
            "B": "Bi-Monthly",
            "Q": "Quarterly",
            "S": "Semi-Annually",
            "A": "Annually"
        }
        month_mapping = {
            1: "Jan",
            2: "Feb",
            3: "Mar",
            4: "Apr",
            5: "May",
            6: "Jun",
            7: "Jul",
            8: "Aug",
            9: "Sep",
            10: "Oct",
            11: "Nov",
            12: "Dec"
        }
        for idx, i in enumerate(data):
            data[idx]["FREQUENCY_NAME"] = frequency_mapping.get(i.get("FREQUENCY"), "Unknown")  # Default to "Unknown" if not found
            start_month = int(i.get("START_MONTH")) if i.get("START_MONTH") else None  # Convert to int
            end_month   = int(i.get("END_MONTH")) if i.get("END_MONTH") else None  # Convert to int

            data[idx]["START_MONTH_NAME"] = month_mapping.get(start_month, "Unknown")  # Default to "Unknown" if not found
            data[idx]["END_MONTH_NAME"] = month_mapping.get(end_month, "Unknown")  # Default to "Unknown" if not found
            if buy_type == "redemption" or buy_type == "switch" or buy_type == "stp":
                data[idx]["TXNVOLUMETYPE_NAME"] = txn_volume_type_mapping.get(i.get("TXNVOLUMETYPE"), "Unknown")  # Default to "Unknown" if not found
        return
    except Exception as e:
        logger.exception(f"{e}")
        return JsonResponse(f"{e}",safe=False,status=500)

def cart_details(request):
    try:
        login_id    = request.GET.get("login_id")
        buy_type    = request.GET.get("buy_type")

        kwargs = {}
        kwargs["USER"]          = login_id
        kwargs["BUY_TYPE"]      = buy_type
        kwargs["IS_DELETED"]    = False

        v               = ["id","BUY_TYPE","PLAN_NAME__id","PLAN_NAME__PLAN_NAME","PLAN_NAME__SCHEME_CODE","PLAN_NAME__FUND_CODE__FUND_CODE","PLAN_NAME__FUND_CODE__FUND_NAME","GOAL","FOLLIO_NO","PLAN_NAME__DIV_OPT","INVEST_AMT","DIVIDENDOPTION","NFO_ALLOWED"]
        tarscheme       = ["TARSCHEMECODE__id","TARSCHEMECODE__PLAN_NAME","TARSCHEMECODE__SCHEME_CODE"]
        other           = ["FREQUENCY","DAY","START_MONTH","START_YEAR","END_MONTH","END_YEAR"]
        if buy_type == "mutual_funds" or buy_type == "additional_purchase":
            data        = list(Cart.objects.filter(**kwargs).values(*v))
            total_amt   = Cart.objects.filter(**kwargs).aggregate(Sum("INVEST_AMT"))["INVEST_AMT__sum"]
        if buy_type == "sip" or buy_type == "swp":
            data        = list(Cart.objects.filter(**kwargs).values(*v,*other,"REOPEN_DATE"))
            fullform(data,buy_type)
            total_amt   = Cart.objects.filter(**kwargs).aggregate(Sum("INVEST_AMT"))["INVEST_AMT__sum"]
        
        if buy_type == "redemption" or buy_type == "switch" or buy_type == "stp":
            data        = list(Cart.objects.filter(**kwargs).values(*v,*tarscheme,*other,"TXNVOLUMETYPE"))
            fullform(data,buy_type)
            total_amt   = Cart.objects.filter(**kwargs).aggregate(Sum("INVEST_AMT"))["INVEST_AMT__sum"]

        return JsonResponse({"data":data,"count":len(data),"total_amt":total_amt},safe=False,status=200)
    except Exception as e:
        logger.info(e)
        return JsonResponse("something went wrong",safe=False,status=500)

def get_cart_api(request,id):
    try:
        # logger.info(f"cart_id = {id}")
        cart                            = Cart.objects.get(id=id)
        data                            = CartSerializer(cart,many=False).data
        if cart.BUY_TYPE == "mutual_funds" or cart.BUY_TYPE  == "sip":
            data["divident_option_load"]    = cart.PLAN_NAME.DIV_OPT
        return JsonResponse(data,safe=False,status=200)
    except Exception as e:
        logger.exception(e)
        return JsonResponse("Something went wrong",safe=False,status=500)

def load_frequency(request):
    try:
        # amc_name        = request.GET.get("amc_name")
        # scheme_code     = request.GET.get("scheme_code")
        plan_id         = request.GET.get("plan_id")
        txn_type        = request.GET.get("txn_type")
        logger.info(f"""
            plan_id    = {plan_id}
            txn_type    = {txn_type}
        """)
        frequency_mapping = {
            "D": "Daily",
            "W": "Weekly",
            "F": "Fortnightly",
            "M": "Monthly",
            "B": "Bi-Monthly",
            "Q": "Quarterly",
            "S": "Semi-Annually",
            "A": "Annually"
        }
        scheme_data = Schemes.objects.get(id=plan_id)
        data = list(Threshold.objects.filter(
            FUND_CODE__FUND_CODE    = scheme_data.FUND_CODE.FUND_CODE,
            SCHEME_CODE             = scheme_data.SCHEME_CODE,
            TXN_TYPE                = txn_type
        ).values("SYS_FREQ"))

        for idx, i in enumerate(data):
            sys_freq    = i.get("SYS_FREQ")
            
            data[idx]["FREQ_NAME"] = frequency_mapping.get(sys_freq, "Unknown")  # Default to "Unknown" if not found

        return JsonResponse(data,safe=False,status=200)
    except Exception as e:
        logger.exception(e)
        return JsonResponse("something went wrong",safe=False,status=500)

def frequency_min_amt(request):
    try:
        # amc_name        = request.GET.get("amc_name")
        # scheme_code     = request.GET.get("scheme_code")
        frequency       = request.GET.get("frequency")
        plan_id         = request.GET.get("plan_id")

        txn_type        = request.GET.get("txn_type")
        # logger.info(f"""
        #     frequency   = {frequency}
        #     plan_id     = {plan_id}
        #     txn_type    = {txn_type}
        # """)
        scheme_data = Schemes.objects.get(id=plan_id)
        data    = list(Threshold.objects.filter(
            FUND_CODE__FUND_CODE    = scheme_data.FUND_CODE.FUND_CODE,
            SCHEME_CODE             = scheme_data.SCHEME_CODE,
            SYS_FREQ                = frequency,
            TXN_TYPE                = txn_type,
        ).values("MIN_AMT","SYS_FREQ_OPT","SYS_DATES"))
        return JsonResponse(data,safe=False,status=200)
    except Exception as e:
        logger.exception(f"{e}")
        return JsonResponse(f"{e}",safe=False,status=500)

def get_min_amt(request):
    try:
        plan_id     = request.GET.get("plan_id")
        txn_type    = request.GET.get("txn_type")

        if txn_type  == "additional_purchase" or txn_type  == "mutual_funds":
            txn_type    = "B"
        elif txn_type  == "redemption":
            txn_type    = "R"
        else:
            txn_type = ""

        scheme_data     = Schemes.objects.get(id=plan_id)
        threshold_data  = Threshold.objects.filter(
            FUND_CODE__FUND_CODE    = scheme_data.FUND_CODE.FUND_CODE,
            TXN_TYPE                = txn_type,
            SCHEME_CODE             = scheme_data.SCHEME_CODE  # Specify the scheme code here
        ).aggregate(min_amt=Min('MIN_AMT'))

        min_amt = threshold_data.get('min_amt') or 0

        data = {
            "min_amt":min_amt
        }
        return JsonResponse(data,safe=False,status=200)
    except Exception as e:
        logger.exception(e)
        return JsonResponse("Something went wrong",safe=False,status=500)

@api_view(["POST"])
def delete_cart(request,id):
    try:
        logger.info(f"id = {id}")
        a = Cart.objects.get(id=id)
        a.delete()
        return JsonResponse("Cart Deleted successfully",safe=False,status=200)
    except Exception as e:
        logger.exception(e)
        return JsonResponse("Something went wrong",safe=False,status=500)
    

@api_view(["POST"])
def delete_success_cart(request):
    try:
        cart_id     = request.data.getlist("cart_id[]")
        logger.info(f"cart_id = {cart_id}")
        Cart.objects.filter(id__in=cart_id).update(IS_DELETED=True)
        return JsonResponse("Cart Deleted successfully",safe=False,status=200)
    except Exception as e:
        logger.exception(e)
        return JsonResponse("Something went wrong",safe=False,status=500)
    
from urllib.parse import urlencode, quote_plus
def test_mfu_login(request):
    try:
        # app_type = request.data.get("app_type")
        checklist = Header_Checklist.objects.get(APP_TYPE="prod",CHECKLIST_USE_FOR="transaction")
        url = f"{checklist.BASE_URL}/MfUtilityApiLogin.do"
        params = {
            "sendResponseFormat": "JSON",
            "loginid": checklist.LOGIN_ID,
            "password": checklist.EN_ENCR_PASSWORD,
            "entityId": checklist.ENTITY_ID,
            "logTp": "A",
            "versionNo": "1.00"
        }

        # URL-encode the query parameters
        encoded_params = urlencode(params, quote_via=quote_plus)

        # Construct the full URL
        encoded_url = f"{url}?{encoded_params}"

        # Print the encoded URL    logger.info(F"))
        logger.info(f"encode_url = {encoded_url}")
        headers = {
            'Content-Type': 'application/xml'
        }
        response = requests.get(url, headers=headers, verify=False)
        logger.info(f"text= {response.text}")
        return JsonResponse("Sucess",safe=False,status=200)
    except Exception as e:
        logger.exception(e)
        return JsonResponse("Something went wrong",safe=False,status=500)
    
# def change_countrymaster(request):
#     for i in Country_master.objects.all():
#         logger.info(i.id)
#         Country_master.objects.filter(id=i.id).update(CODE=str(i.CODE).zfill(3))
#         # str(i.CODE).zfill(3)
#         # i.save()
#     return JsonResponse("success",safe=False,status=200)


# def test_file_upload(request,id):
#     file_upload(id)
#         #     # return JsonResponse(data,safe=False,status=200)
#         #     return True,data

@api_view(["POST"])
def send_otp(request):
    try:
        mobile_no           = request.data.get("mobile_no")
        app_type            = request.data.get('app_type')
        otp_for             = request.data.get('otp_for')


        key = random.randint(1111,9999)
        send_sms = ""

        if otp_for == "mobile_no_verify":
          send_sms = "true"
          requests.get(f'https://sms.visionhlt.com/api/mt/SendSMS?apikey=j4dxea8CyUWirkzj0EcGng&senderid=ESINVT&channel=Trans&DCS=0&flashsms=0&number=91{mobile_no}&text=Your OTP for login is mobile VERIFICATION (MFU) is {key}. Regards Easy Investology Pvt Ltd')

        if otp_for == "reset_password":
            if Registration_personal_details.objects.filter(MOBILE=mobile_no,APP_TYPE=app_type).exists():
                send_sms = "true"
                requests.get(f'https://sms.visionhlt.com/api/mt/SendSMS?apikey=j4dxea8CyUWirkzj0EcGng&senderid=ESINVT&channel=Trans&DCS=0&flashsms=0&number=91{mobile_no}&text=OTP to Reset Your Password (MFU) is {key}. Regards, Easy Investology Pvt. Ltd.')
                
            else:
                return JsonResponse({"error":"This Mobile No is Does not exists Sign Up first"},status=412)
                
        if send_sms == "true":
            User_Otp.objects.create(MOBILE_NO=mobile_no,OTP=key)
            return JsonResponse({"message":"Otp Sent Successfully","OTP":key},status=200)
        else:
            return JsonResponse({"error":"Somethong went wrong"},status=500)
    except Exception as e:
        logger.exception(e)
        return JsonResponse({"error":"Somethong went wrong"},status=500)

@api_view(["POST"])  
def verify_otp(request):
    try:
        mobile_no   = request.data.get("mobile_no")
        otp         = request.data.get("otp")
        # logger.info(f"""
        #     mobile_no       = {mobile_no}
        #     otp             = {otp}
        # """)
        user_otp = User_Otp.objects.filter(MOBILE_NO=mobile_no).last()

        if otp == user_otp.OTP:
            user_otp.delete()
            return JsonResponse({"message":"Otp Verify Successfully"},status=200)
        return JsonResponse({"error":"Otp does not exist"},status=412) 
    except Exception as e:
        logger.exception(e)
        return JsonResponse({"error":"something went wrong"},status=500)

@api_view(["POST"])  
def change_app_password(request):
    try:
        mobile_no       = request.data.get("mobile_no")
        password        = request.data.get("password")
        app_type        = request.data.get('app_type')
        logger.info(f"""
            mobile_no      = {mobile_no}
            password       = {password}
            app_type       = {app_type}
        """)
        if Registration_personal_details.objects.filter(MOBILE=mobile_no,APP_TYPE=app_type).exists():
            user = Registration_personal_details.objects.get(MOBILE=mobile_no,APP_TYPE=app_type)
            user.PASSWORD = password
            user.save()
            return JsonResponse({"message":"Password Change Successfully"},status=200)
        else:
            return JsonResponse({"error":"This Mobile No is Does not exists Sign Up first"},status=412)
    except Exception as e:
        logger.exception(e)
        return JsonResponse({"error":"something went wrong"},status=500)

def convert_to_base64():
    credentials = f'{os.environ["KYC_CLIENT_ID"]}:{os.environ["KYC_CLIENT_SECRET"]}'
    encoded_credentials = base64.b64encode(credentials.encode()).decode()
    return encoded_credentials


import pandas as pd
import mysql.connector
def new_csv_download(request):
    try:

        # Establish a connection to your MySQL database
        conn = mysql.connector.connect(
            # db_name = 'lnt_db'
            # username = 'lnt'
            # password = 'Lnt@#2024'

            host='localhost', 
            user='lnt', 
            password='Lnt@#2024', 
            database='lnt_db'
        )

        # Define your SQL query
        query = """
        WITH LatestParent AS (
            SELECT
                parentId,
                childId,
                ROW_NUMBER() OVER (PARTITION BY parentId ORDER BY srId DESC) AS rn
            FROM parent_child_tbl
        )
        SELECT 
            CONCAT(u.first_name, ' ', u.last_name) AS `Electrician_Name`,
            u.username AS `Electrician_Phone_Number`,
            u.city AS `City`,
            u.state AS `State`,
            
            COALESCE(SUM(
                CASE 
                    WHEN DATE_FORMAT(rp.created_at, '%Y-%m') = '2024-09' 
                    THEN rp.point 
                    ELSE 0 
                END
            ), 0) AS `Points in Jan 2023`,

            COALESCE(u.first_name, '') AS `Iso Name`,
            COALESCE(u.username, '') AS `Iso Phone Number`,
            COALESCE(u.address_line_1, '') AS `Address`

        FROM 
            users u
        LEFT JOIN 
            register_promo_codes rp ON u.id = rp.user_id
        LEFT JOIN 
            LatestParent lp ON u.id = lp.childId AND lp.rn = 1

        WHERE 
            rp.created_at BETWEEN '2024-09-10' AND '2024-09-24'
            AND rp.status = 1
            AND rp.type = 1
            AND rp.refund != 1

        GROUP BY 
            u.id, u.first_name, u.last_name, u.username, u.city, u.state, u.address_line_1;
        """

        # Execute the SQL query and load the data into a pandas DataFrame
        df = pd.read_sql_query(query, conn)

        # Close the database connection
        conn.close()

        # Export the DataFrame to a CSV file
        df.to_csv('23_sept.csv', index=False)

        print("Data exported successfully to electricians_data.csv")
        return JsonResponse("sucess",safe=False,status=200)
    except Exception as e:
        logger.exception(e)
        return JsonResponse({"error":"something went wrong"},status=500)
    

def user_csv_download(request):
    try:

        # Establish a connection to your MySQL database
        conn = mysql.connector.connect(
            # db_name = 'lnt_db'
            # username = 'lnt'
            # password = 'Lnt@#2024'

            host='localhost', 
            user='lnt', 
            password='Lnt@#2024', 
            database='lnt_db'
        )

        # Define your SQL query
        query = """
        SELECT 
            *
        FROM 
            users u
        JOIN 
            model_has_roles mhr 
        ON 
            u.id = mhr.model_id
        WHERE 
            mhr.role_id = 4; 
        """

        # Execute the SQL query and load the data into a pandas DataFrame
        df = pd.read_sql_query(query, conn)

        # Close the database connection
        conn.close()

        # Export the DataFrame to a CSV file
        df.to_csv('ISO.csv', index=False)

        print("Data exported successfully to electricians_data.csv")
        return JsonResponse("sucess",safe=False,status=200)
    except Exception as e:
        logger.exception(e)
        return JsonResponse({"error":"something went wrong"},status=500)

@api_view(["POST"])
def bulk_candata_creation(request):
    try:
        excel_file      = request.FILES.get("excel_file")

        filename = excel_file.name
        # Extract the file extension
        extension = os.path.splitext(filename)[1]

        logger.info(f"excel_file = {extension}")
        
        if extension not in [".xls", ".xlsx"]:
            return JsonResponse("Upload Only .xls format", safe=False, status=412)
        
        start_time = time.time()
        
        df = pd.read_excel(excel_file)
        df.fillna("", inplace=True)
        # df = pd.read_excel(excel_file).fillna("")

        with transaction.atomic():

            for index, row in df.iterrows():
                # if Cams_kfintech_schemes_master.objects.filter(PRODCODE=row["prodcode"]).exists():
                if row['CAN Status'].strip() == "Approved":
                    if Registration_personal_details.objects.filter(PAN_NO=row['Primary PAN_PEKRN'].strip(),CAN=row['CAN'].strip()).exists():
                        pass
                    else:
                        '''     registration1 Start     '''
                        if row['Residential Status'].strip() == "01-RES.IND (Minor)":
                            pan_no          = row['Guardian PAN']
                        else:
                            pan_no          = row['Primary PAN_PEKRN']
                        add_user = Registration_personal_details.objects.create(
                            APP_TYPE                = "prod",
                            CUST_TYPE               = "mfu",
                            PAN_NO                  = pan_no,
                            NAME                    = row['Primary Holder Name'].strip(),
                            EMAIL                   = row['Primary Holder Primary Email ID'].strip(),
                            MOBILE                  = int(row['Primary Holder Primary Mobile No']),
                            PASSWORD                = "1234",
                            CAN                     = row['CAN'].strip(),
                            CAN_STATUS              = "AP"
                        )
                        '''     registration1 End     '''

                        '''     registration2 Start     '''
                        holding_count      = 1
                        if row['Holding Type'].strip() == "Joint" or row['Holding Type'].strip() == "Anyone or Survivor":
                            holding_count == 2
                        elif row['Holding Type'].strip() == "Single" and row['CAN Category'].strip() == "Minor":
                            holding_count      = 2


                        if row['Residential Status'].strip() == "01-RES.IND":
                            tax_status      = 2
                        elif row['Residential Status'].strip() == "01-RES.IND (Minor)":
                            tax_status      = 11
                        elif row['Residential Status'].strip() == "02-NRI-NRE":
                            tax_status      = 3
                        elif row['Residential Status'].strip() == "03-NRI-NRO":
                            tax_status      = 1

                        add_mfu = Registration_mfu_details.objects.create(
                            USER                    = add_user,
                            HOLDING_NATURE          = Holding_nature_master.objects.get(HOLDING_TYPE=row['Holding Type'].strip()),
                            INVESTOR_CATEGORY       = Investor_category_master.objects.get(NAME=row['CAN Category'].strip()),
                            TAX_STATUS              = Tax_status_master.objects.get(id=tax_status),
                            HOLDING_COUNT           = holding_count
                        )
                        
                        '''     registration2 End     '''
                    
                        for i in range(1,int(holding_count)+1):
                            if i == 1:
                                Registration_holder_details.objects.create(
                                    USER                = add_user,
                                    HOLDER_TYPE         = "PR",
                                    HOLDER_NAME         = row['Primary Holder Name'].strip(),
                                    HOLDER_DOB          = row['Primary Holder DOB'].date(),
                                    PAN_NO              = row['Primary PAN_PEKRN'].strip(),
                                    PRI_MOB_NO          = int(row['Primary Holder Primary Mobile No']),
                                    PRI_MOB_BELONGSTO   = "S",
                                    ALT_MOB_NO          = int(row['Primary Holder Alt Mobile No']) if row['Primary Holder Alt Mobile No'] else "",
                                    PRI_EMAIL           = row['Primary Holder Primary Email ID'].strip(),
                                    PRI_EMAIL_BELONGSTO = "S",
                                    ALT_EMAIL           = row['Primary Holder Alt Email ID'].strip(),
                                )

                            if i == 2:
                                if row['CAN Category'].strip() == "Minor":
                                    ''' Guardian '''
                                    Registration_holder_details.objects.create(
                                        USER                = add_user,
                                        HOLDER_TYPE         = "GU",
                                        HOLDER_NAME         = row['Guardian Name'].strip(),
                                        HOLDER_DOB          = row['Guardian DOB'].date(),
                                        PAN_NO              = row['Guardian PAN'].strip(),
                                    )
                                else:
                                    ''' Secondary Holder '''
                                    Registration_holder_details.objects.create(
                                        USER                = add_user,
                                        HOLDER_TYPE         = "SE",
                                        HOLDER_NAME         = row['Second Holder Name'].strip(),
                                        HOLDER_DOB          = row['Second Holder DOB'].date(),
                                        PAN_NO              = row['Second Holder PAN'].strip(),
                                        PRI_MOB_NO          = int(row['Second Holder Primary Mobile No']) if row['Second Holder Primary Mobile No'] else "",
                                        PRI_MOB_BELONGSTO   = "S",
                                        ALT_MOB_NO          = int(row['Second Holder Alt Mobile No']) if row['Second Holder Alt Mobile No'] else "",
                                        PRI_EMAIL           = row['Second Holder Primary Email ID'].strip(),
                                        PRI_EMAIL_BELONGSTO = "S",
                                        ALT_EMAIL           = row['Second Holder Alt Email ID'].strip(),
                                    )

                        '''     registration3 Start     '''
                        
                        
                        for i in range(1,3):
                            if row[f'Bank {i} Account Type'].strip() == "Savings":
                                acc_type = 5
                            elif row[f'Bank {i} Account Type'].strip() == "Current":
                                acc_type = 9
                            elif row[f'Bank {i} Account Type'].strip() == "Non Resident External":
                                acc_type = 6
                            elif row[f'Bank {i} Account Type'].strip() == "Non Resident Ordinary ":
                                acc_type = 7
    

                            if row[f'Bank {i} Name'].strip():
                                # logger.info(f"row[f'Bank {i} Name'].strip() = {row[f'Bank {i} Name'].strip()}")
                                Registration_bank_details.objects.create(
                                    USER                    = add_user,
                                    DEFAULT_BANK            = True if row[f'Bank {i} Default Ac Flag'].strip() == 'Y' else False,
                                    ACC_NO                  = int(row[f'Bank {i} Account No']),
                                    ACC_TYPE                = Bank_account_type_master.objects.get(id=acc_type),
                                    BANK_NAME               = Bank_master.objects.get(NAME=row[f'Bank {i} Name'].strip()),
                                    MICR_NO                 = int(row[f'Bank {i} MICR']),
                                    IFSC_CODE               = str(row[f'Bank {i} IFSC']).strip(),
                                )
                        '''     registration3 End     '''
                        '''     registration4 Start     '''

                        if row['CAN Category'].strip() == "Individual":
                            Registration_nominee_details.objects.create(
                                USER                        = add_user,
                                NOMINEE_OPTION              = "Y",
                                NOMINEE_VERIFICATION_TYPE   = "P" if row['Nominee Verf. Type'].strip() == 'Physical' else "E",
                            )
                            for i in range(1,3):
                                if i == 1:
                                    text = "First"
                                if i == 2:
                                    text = "Second"
                                if row[f'{text} Nominee Name'].strip():
                                    add_nominee = Nominee_details.objects.create(
                                        USER                        = add_user,
                                        NOMINEE_NAME                = row[f'{text} Nominee Name'].strip(),
                                        RELATIONSHIP_WITH_CLIENT    = row[f'{text} Nominee Relationship'].strip(),
                                        NOMINEE_PERCENTAGE          = int(row[f'{text} Nominee Percentage']) if row[f'{text} Nominee Percentage'] else "",
                                        NOMINEE_DOB                 = row[f'{text} Nominee DOB'].date(),
                                        NOMINEE_IS_MINOR            = False
                                    )
                                    if row[f'{text} Nominee Guardian Name'] != "Not Provided" and row[f'{text} Nominee Guardian Name']:
                                        add_nominee.NOMINEE_IS_MINOR            = True
                                        add_nominee.GUARDIAN_NAME               = row[f'{text} Nominee Guardian Name'].strip()
                                        add_nominee.GUARDIAN_RELATION           = row[f'{text} Nominee Guardian Relationship'].strip()
                                        add_nominee.GUARDIAN_DOB                = row[f'{text} Nominee Guardian DOB'].date()
                                    add_nominee.save()
                        '''     registration4 End     '''
                        
        end_time = time.time()

        total_time = "%.2f" % (end_time - start_time)
        minutes = float(total_time) // 60
        seconds = float(total_time) % 60

        formatted_time = f"{minutes} minutes and {seconds:.2f} seconds"
        logger.info(f"formatted_time = {formatted_time}")
        return JsonResponse("sucess",safe=False,status=200)
    except Exception as e:
        logger.exception(e)
        return JsonResponse({"error":"something went wrong"},status=500)
    

@api_view(["POST"])
def bulk_prn_and_bank_data(request):
    try:
        excel_file      = request.FILES.get("excel_file")
        filename = excel_file.name
        # Extract the file extension
        extension = os.path.splitext(filename)[1]

        logger.info(f"excel_file = {extension}")
        
        if extension not in [".xls", ".xlsx"]:
            return JsonResponse("Upload Only .xls format", safe=False, status=412)
        
        start_time = time.time()
        
        df = pd.read_excel(excel_file)
        df.fillna("", inplace=True)
        # df = pd.read_excel(excel_file).fillna("")

        with transaction.atomic():

            for index, row in df.iterrows():
                if row['Registration Status'].strip() == "Registration Successful" or row['Registration Status'].strip() == "Pending":
                    if row['Registration Status'].strip() == "Registration Successful":
                        mmrn_reg_status     = "PA"
                        mmrn_aggr_status    = "AK"

                    if row['Registration Status'].strip() == "Pending":
                        mmrn_reg_status     = "PE"
                        mmrn_aggr_status    = "PE"
                    logger.info(f"row['Account No'] = {row['Account No']}")
                    data = Registration_bank_details.objects.get(USER__CAN=row['CAN'].strip(),ACC_NO__icontains=row['Account No'],IS_DELETED=False)
                    data.MANDATE_BANK       = True
                    data.MMRN               = row['MMRN']
                    data.TRANSACTION_LIMIT  = row['Max Amount']
                    data.MANDATE_START_DATE = row['PRN Start Date'].date()
                    data.MANDATE_END_DATE   = row['PRN End Date'].date()
                    data.PRN                = row['PRN']
                    data.MMRN_REG_STATUS    = mmrn_reg_status
                    data.MMRN_AGGR_STATUS   = mmrn_aggr_status
                    data.save()
                    # Registration_bank_details.objects.filter(IS_DELETED=False,MANDATE_BANK=True)
                    # if i.MMRN_REG_STATUS != "PA" and i.MMRN_AGGR_STATUS != "AK" and i.MANDATE_BANK is True:
                       
        end_time = time.time()

        total_time = "%.2f" % (end_time - start_time)
        minutes = float(total_time) // 60
        seconds = float(total_time) % 60

        formatted_time = f"{minutes} minutes and {seconds:.2f} seconds"
        logger.info(f"formatted_time = {formatted_time}")
        return JsonResponse("sucess",safe=False,status=200)
    except Exception as e:
        logger.exception(e)
        return JsonResponse({"error":"something went wrong"},status=500)

@api_view(["POST"]) 
def check_user_can_status(request):
    try:
        user_id         = request.data.get('user_id')
        # logger.info(f"user_id = {user_id}")

        data = Registration_personal_details.objects.get(id=user_id)
        
        payeezz_bank_data = Registration_bank_details.objects.filter(USER__id=user_id,MMRN_AGGR_STATUS__in=["AK","PA"])
        # logger.info(f"payeezz_bank_data.count() = {payeezz_bank_data.count()} data ={data.MOBILE}")
        if payeezz_bank_data.count() == 0:
            sip_allowed = False
        else:
            sip_allowed = True

    
        status_data = {
            "status"        : data.CAN_STATUS,
            "sip_allowed"   : sip_allowed
        }
        return JsonResponse(status_data,safe=False,status=200)
    except Exception as e:
        logger.exception(e)
        return JsonResponse({"error":"something went wrong"},status=500)


def calculated_xirr(purchase_date, nav_date,total_amt,market_value):
    try:
        if isinstance(purchase_date, str):
            purchase_date = datetime.strptime(purchase_date, '%Y-%m-%d').date()  # Example format
        if isinstance(nav_date, str):
            nav_date = datetime.strptime(nav_date, '%Y-%m-%d').date()  # Example format

        delta = (nav_date - purchase_date).days
        if delta == 0:
            delta = 1
        # logger.info(f"delta = {delta}")
        days_in_year = 365

        xirr = round((((market_value/total_amt)**(1/(delta / days_in_year)))-1)*100,2)
        return xirr
    except Exception as e:
        logger.exception(f"{e}")
        return JsonResponse(f"{e}",safe=False,status=500)

@api_view(["POST"]) 
def get_user_dashboard(request):
    try:
        pan_no        = request.data.get('pan_no')

        data        = list(Cams_kfintech_transaction.objects.filter(INV_NAME__PAN_NO=pan_no).values("id","PROD_CODE__PRODCODE","PROD_CODE__SCHEME_NAME","INV_NAME__PAN_NO","INV_NAME__CUST_NAME","FOLIO_NO","PROD_CODE__COMPANY").order_by("PROD_CODE__SCHEME_NAME"))

        data = [i for i in data if Cams_kfintech_NAV.objects.filter(PRODCODE__PRODCODE=i['PROD_CODE__PRODCODE']).values("NAV_DATE","NAV_VALUE").order_by('NAV_DATE').last() is not None]

        total_units_sum = total_amount_sum = total_market_value_sum = total_value_of_sip = value_of_sip = 0       

        for idx, i in enumerate(data):
            record_id       = data[idx]["id"]
            product_code    = data[idx]["PROD_CODE__PRODCODE"]
            company_name    = data[idx]["PROD_CODE__COMPANY"]

            i["TOTAL_UNITS"]        = round(Cams_kfintech_transaction_details.objects.filter(FOLIO_NO=record_id).aggregate(Sum('UNITS'))['UNITS__sum'] or 0,2)
            i["TOTAL_AMOUNT"]       = round(Cams_kfintech_transaction_details.objects.filter(FOLIO_NO=record_id).aggregate(Sum('AMOUNT'))['AMOUNT__sum'] or 0)

            i["CURRENT_NAV"]        = Cams_kfintech_NAV.objects.filter(PRODCODE__PRODCODE =product_code).order_by('NAV_DATE').values("NAV_VALUE").last()["NAV_VALUE"]
            i["CURRENT_NAV_DATE"]   = Cams_kfintech_NAV.objects.filter(PRODCODE__PRODCODE =product_code).order_by('NAV_DATE').values("NAV_DATE").last()["NAV_DATE"]
            i["MARKET_VALUE"]       = round(float(i["CURRENT_NAV"] )* float(i["TOTAL_UNITS"]),2)

            total_units_sum         += i["TOTAL_UNITS"]
            total_amount_sum        += i["TOTAL_AMOUNT"]
            total_market_value_sum  += i["MARKET_VALUE"]

            transaction_details = Cams_kfintech_transaction_details.objects.filter(FOLIO_NO=record_id)
    
            # Loop through transaction details to check for "systematic" keyword
            for detail in transaction_details:
                if company_name == "cams":
                    if "instalment" in detail.TRXN_NATURE.lower():   
                        total_value_of_sip  += round(float(detail.AMOUNT))
                        break
                    elif "systematic-bse -" in detail.TRXN_NATURE.lower():
                        total_value_of_sip  += round(float(detail.AMOUNT))
                        break
                # For other companies
                else:
                    if "investment" in detail.TRXN_NATURE.lower():
                        total_value_of_sip  += round(float(detail.AMOUNT))
                        break

        # Avoid ZeroDivisionError by checking total_amount_sum
        if total_amount_sum != 0:
            rate_abs = round(((total_market_value_sum - total_amount_sum) / total_amount_sum) * 100, 2)
        else:
            rate_abs = 0  # Default value if total_amount_sum is 0
  
        data = {
            "invested_amount"       : total_amount_sum,
            "market_value"          : total_market_value_sum,
            "invested_amount_comma" : format_number(total_amount_sum, locale='en_IN'), 
            "market_value_comma"    : format_number(total_market_value_sum, locale='en_IN'),
            "rate_abs"              : rate_abs,
            "rate_ann"              : "20",
            "value_of_sip"          : format_number(total_value_of_sip, locale='en_IN')
        }
        return JsonResponse(data,safe=False,status=200)
    except Exception as e:
        logger.exception(e)
        return JsonResponse({"error":"something went wrong"},status=500)

@api_view(["POST"]) 
def portfolio_valuation(request):
    try:
        pan_no  = request.data.get("pan_no")

        # today_date = datetime.today()
        # user_info   = customer_transaction.objects.get(PAN_NO=client_pan)

        data        = list(Cams_kfintech_transaction.objects.filter(INV_NAME__PAN_NO=pan_no).values("id","PROD_CODE__PRODCODE","PROD_CODE__SCHEME_NAME","FOLIO_NO","PROD_CODE__COMPANY").order_by("PROD_CODE__SCHEME_NAME"))

        total_amount_sum        = 0
        total_market_value_sum  = 0
        for idx, i in enumerate(data):
            record_id       = data[idx]["id"]
            product_code    = data[idx]["PROD_CODE__PRODCODE"]

            i["TOTAL_UNITS"]        = round(Cams_kfintech_transaction_details.objects.filter(FOLIO_NO=record_id).aggregate(Sum('UNITS'))['UNITS__sum'] or 0,2)
            i["TOTAL_AMOUNT"]       = round(Cams_kfintech_transaction_details.objects.filter(FOLIO_NO=record_id).aggregate(Sum('AMOUNT'))['AMOUNT__sum'] or 0)
            i["TOTAL_AMOUNT_COMMA"] = format_number(i["TOTAL_AMOUNT"], locale='en_IN')
            
            i["CURRENT_NAV"]        = Cams_kfintech_NAV.objects.filter(PRODCODE__PRODCODE =product_code).order_by('NAV_DATE').values("NAV_VALUE").last()["NAV_VALUE"]
            i["CURRENT_NAV_DATE"]   = Cams_kfintech_NAV.objects.filter(PRODCODE__PRODCODE =product_code).order_by('NAV_DATE').values("NAV_DATE").last()["NAV_DATE"]

            i["MARKET_VALUE"]       = round(float(i["CURRENT_NAV"] )* float(i["TOTAL_UNITS"]),2)

            i["MARKET_VALUE_COMMA"] = format_number(i["MARKET_VALUE"], locale='en_IN')
            # i["GAIN_LOSS"]          = round(float(i["MARKET_VALUE"]) - float( i["TOTAL_AMOUNT"]),2)
            i["PURCHASE_DATE"]      = Cams_kfintech_transaction_details.objects.filter(FOLIO_NO=record_id).aggregate(PURCHASE_DATE=Min('TRADDATE'))['PURCHASE_DATE']
            # total_purprice_sum      += i["TOTAL_PURPRICE"]
            # total_units_sum         += i["TOTAL_UNITS"]
            total_amount_sum        += i["TOTAL_AMOUNT"]
            total_market_value_sum  += i["MARKET_VALUE"]
            # total_gain_loss_sum     += i["GAIN_LOSS"]

            i["ABS_RETURN"]         = round(((i["MARKET_VALUE"]-i["TOTAL_AMOUNT"])/float( i["TOTAL_AMOUNT"]))*100,2)
            i["XIRR"]               = calculated_xirr(i["PURCHASE_DATE"], i["CURRENT_NAV_DATE"],i["TOTAL_AMOUNT"],i["MARKET_VALUE"])
        grand_total_sum = total_market_value_sum-total_amount_sum
        data = {
            "data"                  : data,
            "summery_date"          : Cams_kfintech_NAV.objects.order_by('NAV_DATE').values("NAV_DATE").last()["NAV_DATE"],
            "invested_amount"       : total_amount_sum,
            "market_value"          : total_market_value_sum,
            "grand_total"           : grand_total_sum,
            "invested_amount_comma" : format_number(total_amount_sum, locale='en_IN'), 
            "market_value_comma"    : format_number(total_market_value_sum, locale='en_IN'),
            "grand_total_comma"     : format_number(grand_total_sum, locale='en_IN'),
            
        }

        return JsonResponse(data,safe=False,status=200)
    except Exception as e:
        logger.exception(e)
        return JsonResponse({"error":"something went wrong"},status=500)


# @api_view(["POST"])
# def bulk_candata_bank_edit(request):
#     try:
#         excel_file      = request.FILES.get("excel_file")

#         filename = excel_file.name
#         # Extract the file extension
#         extension = os.path.splitext(filename)[1]

#         logger.info(f"excel_file = {extension}")
        
#         if extension not in [".xls", ".xlsx"]:
#             return JsonResponse("Upload Only .xls format", safe=False, status=412)
        
#         start_time = time.time()
        
#         df = pd.read_excel(excel_file)
#         df.fillna("", inplace=True)
  
#         # df = pd.read_excel(excel_file).fillna("")

#         with transaction.atomic():

#             for index, row in df.iterrows():
#                 # if Cams_kfintech_schemes_master.objects.filter(PRODCODE=row["prodcode"]).exists():
#                 if row['CAN Status'].strip() == "Approved":
#                     '''     registration1 Start     '''
#                     if Registration_personal_details.objects.filter(PAN_NO=row['Primary PAN_PEKRN'].strip(),CAN=row['CAN'].strip()).exists():
#                         for i in range(1,3):
                          

#                             if row[f'Bank {i} Name'].strip():
                                
#                                 if index == 5:
#                                     return JsonResponse("sucess",safe=False,status=200)
#                                 else:
#                                     logger.info(f"Bank {i} Account No = {str(row[f'Bank {i} Account No'])}")
#                                 # logger.info(f"index ={index}")
#                                 # logger.info(f"row[f'Bank {i} Name'].strip() = {row[f'Bank {i} Name'].strip()}")
#                                 # Registration_bank_details.objects.create(
#                                 #     USER                    = add_user,
#                                 #     DEFAULT_BANK            = True if row[f'Bank {i} Default Ac Flag'].strip() == 'Y' else False,
#                                 #     ACC_NO                  = row[f'Bank {i} Account No'],
#                                 #     ACC_TYPE                = Bank_account_type_master.objects.get(id=acc_type),
#                                 #     BANK_NAME               = Bank_master.objects.get(NAME=row[f'Bank {i} Name'].strip()),
#                                 #     MICR_NO                 = int(row[f'Bank {i} MICR']),
#                                 #     IFSC_CODE               = str(row[f'Bank {i} IFSC']).strip(),
#                                 # )
#                         '''     registration1 End     '''


                        
                        
#         end_time = time.time()

#         total_time = "%.2f" % (end_time - start_time)
#         minutes = float(total_time) // 60
#         seconds = float(total_time) % 60

#         formatted_time = f"{minutes} minutes and {seconds:.2f} seconds"
#         logger.info(f"formatted_time = {formatted_time}")
#         return JsonResponse("sucess",safe=False,status=200)
#     except Exception as e:
#         logger.exception(e)
#         return JsonResponse({"error":"something went wrong"},status=500)

@api_view(["POST"])
def bulk_candata_bank_edit(request):
    try:
        excel_file = request.FILES.get("excel_file")

        filename = excel_file.name
        # Extract the file extension
        extension = os.path.splitext(filename)[1]

        logger.info(f"excel_file = {extension}")
        
        if extension not in [".xls", ".xlsx"]:
            return JsonResponse("Upload Only .xls format", safe=False, status=412)
        
        start_time = time.time()
        
        # Explicitly specify the columns that should be treated as strings
        df = pd.read_excel(excel_file, dtype={'Bank 1 Account No': str, 'Bank 2 Account No': str})
        df.fillna("", inplace=True)

        with transaction.atomic():
            for index, row in df.iterrows():
                if row['CAN Status'].strip() == "Approved":
                    # Check if the record exists based on PAN and CAN number
                    if Registration_personal_details.objects.filter(PAN_NO=row['Primary PAN_PEKRN'].strip(), CAN=row['CAN'].strip()).exists():
                        # for i in range(1, 3):
                        if row[f'Bank 1 Name'].strip():
                            # Log and check the format of the bank account number
                            default_bank = True if row[f'Bank 1 Default Ac Flag'].strip() == 'Y' else False
                            account_no = str(row[f'Bank 1 Account No']).strip()
                            logger.info(f"Bank 1 Account No = {account_no} can_no = {row['CAN'].strip()}")

                            data = Registration_bank_details.objects.get(USER__CAN=row['CAN'].strip(),DEFAULT_BANK=default_bank,IS_DELETED=False)
                            data.ACC_NO = account_no
                            data.save()
                            

                            # if index == 5:
                            #     return JsonResponse("success", safe=False, status=200)
        
        end_time = time.time()

        total_time = "%.2f" % (end_time - start_time)
        minutes = float(total_time) // 60
        seconds = float(total_time) % 60

        formatted_time = f"{minutes} minutes and {seconds:.2f} seconds"
        logger.info(f"formatted_time = {formatted_time}")
        return JsonResponse("success", safe=False, status=200)
    except Exception as e:
        logger.exception(e)
        return JsonResponse({"error": "something went wrong"}, status=500)


# def 
# rushikesh
def load_belongs_to(request):
    try:
        data =  list(Mobile_belongs_to.objects.filter(IS_DELETED = False).values("id","CODE","NAME").order_by("-id"))
        return JsonResponse({"data":data},safe=False,status=200)
    except Exception as e:
        logger.exception(f"{e}")
        return JsonResponse(f"{e}",safe=False,status=500)

def load_nominee_relation(request):
    try:
        data =  list(Nominee_Relation.objects.filter(IS_DELETED = False).values("id","NOM_REL_CODE","NOM_GURI_REL_CODE","NAME").order_by("-id"))
        return JsonResponse({"data":data},safe=False,status=200)
    except Exception as e:
        logger.exception(f"{e}")
        return JsonResponse(f"{e}",safe=False,status=500)
