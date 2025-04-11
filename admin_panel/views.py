import os
#import app.views
from app.views import mfu_payeezz_validation, mfu_can_validation
from app.models import *
from buy.models import *
from admin_panel.models import *
from django.shortcuts import render, redirect
from rest_framework.views import APIView
from rest_framework.decorators import api_view

from django.contrib import messages
from django.http import JsonResponse ,HttpResponse
# from crm.models import *

from django.contrib import messages  # import messages
import time
from datetime import datetime, timedelta, date

from dateutil.relativedelta import relativedelta
from django.contrib.auth.hashers import check_password
from django.utils import timezone

from django.db.models import F, Q, Value, CharField , Sum, Min, Avg, Count ,Max
from django.db.models.functions import Concat

from app.serializers import *
from admin_panel.serializers import *

import hashlib
import requests

# for bulk Excel
import pandas as pd
from django.db import transaction

from itertools import chain
import logging

logger = logging.getLogger()
from babel.numbers import format_number


def admin_login(request):
    return render(request, "admin_panel/login.html")


def admin_dashboard(request):
    return render(request, "admin_panel/index.html")


def customer_management(request):
    return render(request, "admin_panel/customer_management.html")


def can_error(request):
    return render(request, "admin_panel/can_error.html")

def load_can_error_data(request):
    try:
        data = list(
            can_creation_request_response.objects.filter(
                USER__CAN__isnull=False
            ).values(
                "id", "USER__NAME", "USER__MOBILE", "USER__PAN_NO","USER__EMAIL"
            ).order_by("-id")
        )
        return JsonResponse({"data": data}, safe=False, status=200)
    except Exception as e:
        logger.exception(f"{e}")
        return JsonResponse(f"{e}",safe=False,status=500)

# def get_canerror_req_res
def get_canerror_req_res(request, id):
    try:
        data = list(can_creation_request_response.objects.filter(id=id).values("id", "REQUEST", "RESPONSE"))
        return JsonResponse(data, safe=False, status=200)
    except Exception as e:
        logger.exception(f"{e}")
        return JsonResponse(f"{e}",safe=False,status=500)

def load_admin_customer(request):
    try:
        data = list(
            Registration_personal_details.objects.values(
                "id", "NAME", "MOBILE", "PAN_NO", "CAN", "EMAIL"
            ).order_by("-id")
        )
        return JsonResponse({"data": data}, safe=False, status=200)
    except Exception as e:
        logger.exception(f"{e}")
        return JsonResponse(f"{e}",safe=False,status=500)


def replace_null_with_empty(data):
    return [{k: (v if v is not None else "") for k, v in item.items()} for item in data]


def customer_detail(request, id):
    device_type = request.GET.get("device_type")
    logger.info(f"""
        device_type = {device_type}
        id = {id}
    """)
    if device_type == "mobile":
        api_use = request.GET.get("api_use")
        app_type = request.GET.get("app_type")
        logger.info(f"""
            api_use         = {api_use}
            app_type        = {app_type}
        """)
        try:
            mandate_values = []
            if api_use == "profile":
                mfu_payeezz_validation(id, app_type)
                if app_type == "prod":
                    mfu_can_validation(id, app_type)
                mandate_values = [
                    "MANDATE_BANK",
                    "PRN",
                    "MMRN_REG_STATUS",
                    "MMRN_AGGR_STATUS",
                    "TRANSACTION_LIMIT",
                    "MANDATE_START_DATE",
                    "MANDATE_END_DATE",
                ]

            mfu_values = [
                "id",
                "USER_id",
                "HOLDING_NATURE_id",
                "HOLDING_NATURE__HOLDING_TYPE",
                "INVESTOR_CATEGORY_id",
                "INVESTOR_CATEGORY__NAME",
                "TAX_STATUS_id",
                "TAX_STATUS__TAX_STATUS_DESCRIPTION",
                "TAX_STATUS__TAX_STATUS_CODE",
                "HOLDING_COUNT",
            ]
            holder_values = [
                "id",
                "USER_id",
                "HOLDER_TYPE",
                "HOLDER_NAME",
                "HOLDER_DOB",
                "PAN_EXEMPT_FLAG",
                "PAN_NO",
                "HOLDER_PAN_IMG",
                "MINOR_BIRTH_CERTIFICATE",
                "RESIDENCE_ISD",
                "RESIDENCE_STD",
                "RESIDENCE_PHONE_NO",
                "MOB_ISD_CODE",
                "PRI_MOB_NO",
                "PRI_MOB_BELONGSTO",
                "ALT_MOB_NO",
                "OFF_ISD",
                "OFF_STD",
                "OFF_PHONE_NO",
                "PRI_EMAIL",
                "PRI_EMAIL_BELONGSTO",
                "ALT_EMAIL",
                "RELATIONSHIP_WITH_MINOR",
                "PROOF_OF_RELATIONSHIP",
                "RELATIONSHIP_PROOF_DOC",
                "INCOME_TYPE",
                "GROSS_ANNUAL_INCOME_id",
                "GROSS_ANNUAL_INCOME__NAME",
                "NETWORTH_IN_RUPEES",
                "NETWORTH_AS_ON_DATE",
                "SOURCE_OF_WEALTH_id",
                "SOURCE_OF_WEALTH__NAME",
                "SOURCE_OF_WEALTH_OTHERS",
                "KRA_ADDRESS_TYPE_id",
                "OCCUPATION_id",
                "OCCUPATION__NAME",
                "OCCUPATION_OTHERS",
                "PEP_STATUS_id",
                "PEP_STATUS__NAME",
                "ANY_OTHER_INFORMATION",
                "BIRTH_CITY",
                "BIRTH_COUNTRY_id",
                "BIRTH_COUNTRY__NAME",
                "BIRTH_COUNTRY_OTH",
                "CITIZENSHIP_id",
                "CITIZENSHIP__NAME",
                "CITIZENSHIP_OTH",
                "NATIONALITY_id",
                "NATIONALITY__NAME",
                "NATIONALITY_OTH",
                "TAX_RES_FLAG",
                "TAX_COUNTRY_id",
                "TAX_COUNTRY__NAME",
                "TAX_COUNTRY_OTH",
                "TAX_REF_NO",
                "IDENTI_TYPE_id",
                "IDENTI_TYPE__NAME",
                "IDENTI_TYPE_OTH",
            ]

            bank_values = [
                "USER",
                "id",
                "DEFAULT_BANK",
                "ACC_NO",
                "ACC_TYPE_id",
                "ACC_TYPE__BANK_ACCOUNT_TYPE",
                "BANK_NAME_id",
                "BANK_NAME__NAME",
                "MICR_NO",
                "IFSC_CODE",
                "BANK_PROOF__CODE",
                "BANK_PROOF__NAME",
                "BANK_PROOF_FILE",
                "UNIQUEREFNO",
                "PRN",
            ]

            nominee_values = [
                "id",
                "USER_id",
                "NOMINEE_OPTION",
                "NOMINEE_VERIFICATION_TYPE",
            ]

            nominee_detail_values = [
                "id",
                "USER_id",
                "NOMINEE_NAME",
                "RELATIONSHIP_WITH_CLIENT",
                "NOMINEE_PERCENTAGE",
                "NOMINEE_DOB",
                "NOMINEE_IS_MINOR",
                "GUARDIAN_NAME",
                "GUARDIAN_RELATION",
                "GUARDIAN_DOB",
            ]
            context = {
                "profile": replace_null_with_empty(
                    list(Registration_personal_details.objects.filter(id=id).values())
                ),
                "mfu": replace_null_with_empty(
                    list(
                        Registration_mfu_details.objects.filter(
                            USER=id, IS_DELETED=False
                        ).values(*mfu_values)
                    )
                ),
                "holder_details": replace_null_with_empty(
                    list(
                        Registration_holder_details.objects.filter(
                            USER=id, IS_DELETED=False
                        ).values(*holder_values)
                    )
                ),
                "bank_details": replace_null_with_empty(
                    list(
                        Registration_bank_details.objects.filter(
                            USER=id, IS_DELETED=False
                        ).values(*bank_values, *mandate_values)
                    )
                ),
                "nominee": replace_null_with_empty(
                    list(
                        Registration_nominee_details.objects.filter(
                            USER=id, IS_DELETED=False
                        ).values(*nominee_values)
                    )
                ),
                "nominee_detail": replace_null_with_empty(
                    list(
                        Nominee_details.objects.filter(
                            USER=id, IS_DELETED=False
                        ).values(*nominee_detail_values)
                    )
                ),
            }
            return JsonResponse(context, safe=False, status=200)
        except Exception as e:
            logger.exception(e)
            messages.error(request, "Something went wrong")
            return JsonResponse({"error": "Something went Wrong"}, status=500)
    else:
        nominee = {}
        if Registration_mfu_details.objects.filter(USER=id, IS_DELETED=False).exists():
            mfu = Registration_mfu_details.objects.get(USER=id)
            if mfu.INVESTOR_CATEGORY.CODE != "M":
                if Registration_nominee_details.objects.filter(
                    USER=id, IS_DELETED=False
                ).exists():
                    nominee = {
                        "nominee": Registration_nominee_details.objects.get(
                            USER=id, IS_DELETED=False
                        ),
                        "nominee_detail": Nominee_details.objects.filter(
                            USER=id, IS_DELETED=False
                        ),
                    }
        else:
            mfu = ""
        context = {
            "profile": Registration_personal_details.objects.get(id=id),
            "mfu": mfu,
            "holder_details": Registration_holder_details.objects.filter(
                USER=id, IS_DELETED=False
            ),
            "bank_details": Registration_bank_details.objects.filter(
                USER=id, IS_DELETED=False
            ),
            "nominee": nominee,
        }
        return render(request, "admin_panel/customer_detail.html", context)
    # return JsonResponse("success",safe=False,status=200)


# def test_api(request):
#     id = "35"
#     r1 = Registration_personal_details.objects.filter(id=id)
#     r2 = Registration_mfu_details.objects.filter(USER__id=id)
#     r3 = Registration_bank_details.objects.filter(USER__id=id)
#     r4 = Registration_bank_details.objects.filter(USER__id=id)
#     data = {
#         "r1" :list(r1.values()),
#         "r2" : list(r2.values()),
#         "r3" : list(r3.values()),
#         "r4" : list(Registration_bank_details.objects.filter(USER__id=id).values()),
#         # "r5" : list(Registration_bank_details.objects.filter(USER__id=id).values()),
#         # "r5" : list(Registration_bank_details.objects.filter(USER__id=id).values()),
#         # "r5" : list(Registration_bank_details.objects.filter(USER__id=id).values()),
#         # "r5" : list(Registration_bank_details.objects.filter(USER__id=id).values()),

#     }
#     data['r1'][0]['ACCOUNT_TYPE'] = r1[0].ACCOUNT_TYPE.HOLDING_TYPE

#     return JsonResponse(data,safe=False,status=200)


def buy_scheme(request):
    return render(request, "admin_panel/scheme.html")


def scheme_details(request, id):
    data = Schemes.objects.get(id=id)
    return render(request, "admin_panel/scheme_details.html", context={"data": data})


# @api_view(["POST"])
# def add_scheme_excel(request):
#     try:
#         excel_file = request.FILES.get("excel_file")
#         # sheet_name = request.POST.get("sheet_name")
#         Upload_scheme.objects.create(
#             EXCEL=excel_file,
#             # SHEET_NAME = sheet_name,
#         )
#         return JsonResponse({"message": "Excel Add Successfully"}, status=200)
#     except Exception as e:
#         logger.exception(e)
#         messages.error(request, "Something went wrong")
#         return JsonResponse({"error": "Something went Wrong"}, status=500)

@api_view(["POST"])
def add_bulk_scheme(request):
    try:
        excel_file = request.FILES.get("excel_file")
        filename = excel_file.name
        # Extract the file extension
        extension = os.path.splitext(filename)[1]

        logger.info(f"excel_file schemss = {extension}")
        
        if extension == ".xls" or  extension == ".xlsx":
            start_time = time.time()
            
            df = pd.read_excel(excel_file)
            df.fillna("", inplace=True)

            with transaction.atomic():
                for index, row in df.iterrows():

                    fund_code, created = AMC.objects.get_or_create(
                        FUND_CODE=row["fund_code"]
                    )
                    # add_schemes, created = Schemes.objects.get_or_create(
                    #     SCHEME_CODE=row["scheme_code"],FUND_CODE=fund_code,SCHEME_FLAG=row["Scheme Flag"]
                    # )
                    add_schemes = Schemes.objects.create(
                        SCHEME_CODE=row["scheme_code"],
                        FUND_CODE=fund_code,
                        SCHEME_FLAG=row["Scheme Flag"]
                    )
                    add_schemes.NEW_SCHEME          = True
                    
                    add_schemes.PLAN_NAME           = row["plan_name"]
                    add_schemes.SCHEME_TYPE         = row["scheme_type"]
                    add_schemes.PLAN_TYPE           = row["plan_type"]
                    add_schemes.PLAN_OPT            = row["plan_opt"]

                    if row["div_opt"] == "Not Applicable":
                        add_schemes.DIV_OPT         = "NA"
                    else:
                        add_schemes.DIV_OPT         = row["div_opt"]
                    
                    if row["amfi_id"] == "Not Applicable":
                        add_schemes.AMFI_ID         = "NA"
                    else:
                        add_schemes.AMFI_ID         = row["amfi_id"]

                    add_schemes.PRI_ISIN            = row["pri_isin"]
                    add_schemes.SEC_ISIN            = row["sec_isin"]

                    if row["nfo_start"]:
                        add_schemes.NFO_START       = row["nfo_start"]

                    if row["nfo_end"]:
                        add_schemes.NFO_END         = row["nfo_end"]

                    if row["allot_date"]:
                        add_schemes.ALLOT_DATE      = row["allot_date"]

                    if row["reopen_date"]:
                        add_schemes.REOPEN_DATE     = row["reopen_date"]

                    if row["maturity_date"]:
                        add_schemes.MATURITY_DATE   = row["maturity_date"]

                    if (
                        row["entry_load"] == "Not Applicable"
                        or row["entry_load"] == "NA / Not Applicable"
                        or row["entry_load"] == "NA / Not Applicable"
                    ):
                        add_schemes.ENTRY_LOAD      = "NA"
                    else:
                        add_schemes.ENTRY_LOAD      = row["entry_load"]

                    if row["exit_load"] == "Not Applicable":
                        add_schemes.EXIT_LOAD       = "NA"
                    else:
                        add_schemes.EXIT_LOAD       = row["exit_load"]

                    add_schemes.PUR_ALLOWED         = row["pur_allowed"]
                    add_schemes.NFO_ALLOWED         = row["nfo_allowed"]
                    add_schemes.REDEEM_ALLOWED      = row["redeem_allowed"]
                    add_schemes.SIP_ALLOWED         = row["sip_allowed"]
                    add_schemes.SWITCH_OUT_ALLOWED  = row["switch_out_allowed"]
                    add_schemes.SWITCH_IN_ALLOWED   = row["Switch_In_Allowed"]
                    add_schemes.STP_OUT_ALLOWED     = row["stp_out_allowed"]
                    add_schemes.STP_IN_ALLOWED      = row["stp_in_allowed"]
                    add_schemes.SWP_ALLOWED         = row["swp_allowed"]
                    add_schemes.DEMAT_ALLOWED       = row["Demat_Allowed"]

                    if Scheme_sub_category.objects.filter(
                        CATEGORY__CATEGORY_ID=row["Catg ID"],
                        SUB_CATEGORY_ID=row["Sub-Catg ID"],
                    ).exists():
                        add_schemes.CATEGORY = Scheme_sub_category.objects.get(
                            CATEGORY__CATEGORY_ID=row["Catg ID"],
                            SUB_CATEGORY_ID=row["Sub-Catg ID"],
                        )

                    add_schemes.SCHEME_FLAG         = row["Scheme Flag"]
                    add_schemes.save()
                    
            end_time        = time.time()
            elapsed_time    = end_time - start_time
            formatted_time  = f"{int(elapsed_time // 60)} minutes and {elapsed_time % 60:.2f} seconds"
            logger.info(f"Execution Time: {formatted_time}")
            messages.success(request, "Scheme Add Successfully")
            return JsonResponse("Scheme Add Successfully", safe=False, status=200)
        else:
            return JsonResponse("Upload Only .xls or .xlsx format", safe=False, status=412)
    except Exception as e:
        logger.exception(e)
        # messages.error(request,"Something went wrong")
        return JsonResponse("Something went Wrong", safe=False, status=500)

def load_scheme(request):
    data = list(
        Schemes.objects.filter(PLAN_TYPE="REG",SCHEME_TYPE="OE").values(
            "id",
            "FUND_CODE__FUND_CODE",
            "FUND_CODE__COMPANY",
            "FUND_CODE__COMPANY_FUND_CODE",
            "SCHEME_CODE",
            "PLAN_NAME",
            "PLAN_TYPE",
            "PRI_ISIN",
            "SEC_ISIN",
            "PUR_ALLOWED",
            "NFO_ALLOWED",
            "REDEEM_ALLOWED",
            "SIP_ALLOWED",
            "SWITCH_OUT_ALLOWED",
            "SWITCH_IN_ALLOWED",
            "STP_OUT_ALLOWED",
            "STP_IN_ALLOWED",
            "SWP_ALLOWED",
        ).order_by("-id")
        
    )
    return JsonResponse({"data": data}, safe=False, status=200)

def buy_threshold(request):
    return render(request, "admin_panel/threshold.html")


def threshold_details(request, id):
    data = Threshold.objects.get(id=id)
    return render(request, "admin_panel/threshold_details.html", context={"data": data})

# @api_view(["POST"])
# def add_bulk_threshold(request):
#     try:
#         start_time = time.time()
#         excel_data = Upload_scheme.objects.last()

#         df = pd.read_excel(f"media/{excel_data.EXCEL}")

#         df.fillna("", inplace=True)

#         data = df.to_dict(orient="records")

#         with transaction.atomic():
#             for index, row in df.iterrows():
#                 fund_code, created = AMC.objects.get_or_create(
#                     FUND_CODE=row["fund_code"]
#                 )

#                 add = Threshold.objects.create(
#                     FUND_CODE=fund_code,
#                     SCHEME_CODE=row["scheme_code"],
#                     TXN_TYPE=row["txn_type"],
#                 )

#                 add.SYS_FREQ            = row["sys_freq"]
#                 add.SYS_FREQ_OPT        = row["sys_freq_opt"]
#                 add.SYS_DATES           = row["sys_dates"]
#                 add.MIN_AMT             = row["min_amt"]
#                 add.MAX_AMT             = row["max_amt"]
#                 add.MULTIPLE_AMT        = row["multiple_amt"]
#                 add.MIN_UNITS           = row["min_units"]
#                 add.MULTIPLE_UNITS      = row["multiple_units"]
#                 add.MIN_INST            = row["min_inst"]
#                 add.MAX_INST            = row["max_inst"]
#                 add.SYS_PERPETUAL       = row["sys_perpetual"]
#                 add.MIN_CUM_AMT         = row["min_cum_amt"]
#                 if row["start_date"]:
#                     add.START_DATE      = datetime.strptime(
#                         row["start_date"], "%d-%b-%Y"
#                     ).date()

#                 if row["end_date"]:
#                     add.END_DATE        = datetime.strptime(row["end_date"], "%d-%b-%Y").date()

#                 add.save()
#         Upload_scheme.objects.last().delete()
#         end_time = time.time()

#         total_time = "%.2f" % (end_time - start_time)
#         minutes = float(total_time) // 60
#         seconds = float(total_time) % 60

#         formatted_time = f"{minutes} minutes and {seconds:.2f} seconds"
#         logger.info(f"formatted_time = {formatted_time}")
#         messages.success(request, "Threshold Add Successfully")
#         return JsonResponse("Threshold Add Successfully", safe=False, status=200)
#     except Exception as e:
#         logger.exception(e)
#         # messages.error(request,"Something went wrong")
#         return JsonResponse("Something went Wrong", safe=False, status=500)

# Function to convert Excel serial date to datetime
def convert_excel_date(excel_date):
    if isinstance(excel_date, (int, float)):  # Handle numeric dates
        return datetime(1899, 12, 30) + timedelta(days=int(excel_date))
    elif isinstance(excel_date, str):  # Handle string dates
        try:
            return datetime.strptime(excel_date, "%d-%b-%Y").date()
        except ValueError:
            return None  # Return None for invalid dates
    return None  # Return None for other cases

@api_view(["POST"])
def add_bulk_threshold(request):
    try:
        excel_file = request.FILES.get("excel_file")
        if not excel_file:
            return JsonResponse("No file provided", safe=False, status=400)

        filename = excel_file.name
        extension = os.path.splitext(filename)[1].lower()

        logger.info(f"Uploaded file extension: {extension}")
        
        if extension not in [".xls", ".xlsx"]:
            return JsonResponse("Upload only .xls or .xlsx format", safe=False, status=412)

        start_time = time.time()
        
        # Read the Excel file
        df = pd.read_excel(excel_file)
        df.fillna("", inplace=True)

        # Process the data in chunks
        chunk_size = 10000
        for chunk in (df[i:i + chunk_size] for i in range(0, df.shape[0], chunk_size)):
            chunk_records = chunk.to_dict(orient="records")
            with transaction.atomic():
                threshold_objects = []
                for row in chunk_records:
                    try:
                        fund_code, created = AMC.objects.get_or_create(FUND_CODE=row["fund_code"])

                        threshold = Threshold(
                            FUND_CODE=fund_code,
                            SCHEME_CODE=row["scheme_code"],
                            TXN_TYPE=row["txn_type"],
                            SYS_FREQ=row["sys_freq"],
                            SYS_FREQ_OPT=row["sys_freq_opt"],
                            SYS_DATES=row["sys_dates"],
                            MIN_AMT=row["min_amt"],
                            MAX_AMT=row["max_amt"],
                            MULTIPLE_AMT=row["multiple_amt"],
                            MIN_UNITS=row["min_units"],
                            MULTIPLE_UNITS=row["multiple_units"],
                            MIN_INST=row["min_inst"],
                            MAX_INST=row["max_inst"],
                            SYS_PERPETUAL=row["sys_perpetual"],
                            MIN_CUM_AMT=row["min_cum_amt"],
                            START_DATE=convert_excel_date(row["start_date"]),
                            END_DATE=convert_excel_date(row["end_date"]),
                        )
                        threshold_objects.append(threshold)
                    except KeyError as key_err:
                        logger.error(f"Missing key in row: {key_err}")
                    except Exception as ex:
                        logger.error(f"Error processing row: {row} | Error: {ex}")

                # Use bulk_create to improve database efficiency
                Threshold.objects.bulk_create(threshold_objects, batch_size=5000)

        # Calculate execution time
        end_time = time.time()
        elapsed_time = end_time - start_time
        formatted_time = f"{int(elapsed_time // 60)} minutes and {elapsed_time % 60:.2f} seconds"
        logger.info(f"Execution Time: {formatted_time}")

        messages.success(request, "Threshold added successfully")
        return JsonResponse("Threshold added successfully", safe=False, status=200)

    except Exception as e:
        logger.exception("Unexpected error")
        return JsonResponse("Something went wrong", safe=False, status=500)


def load_threshold(request):
    data = list(Threshold.objects.values("id", "FUND_CODE", "SCHEME_CODE", "TXN_TYPE"))
    return JsonResponse({"data": data}, safe=False, status=200)

def cams_kfintech_scheme(request):
    return render(request,"admin_panel/cams_kfintech_scheme.html")

@api_view(["POST"])
def add_bulk_cams_kfintech_scheme(request):
    try:
        excel_file      = request.FILES.get("excel_file")
        company_name    = request.data.get("company_name")
        logger.info(f"company_name = {company_name}")
        filename = excel_file.name
        # Extract the file extension
        extension = os.path.splitext(filename)[1]

        logger.info(f"excel_file = {extension}")
        
        if extension == ".xls" or extension == ".xlsx":
            start_time = time.time()
            
            df = pd.read_excel(excel_file)
            df.fillna("", inplace=True)

            with transaction.atomic():
                for index, row in df.iterrows():
                    if company_name == "cams":

                        add_schemes, created = Cams_kfintech_schemes_master.objects.get_or_create(
                            PRODCODE=row["prodcode"]
                        )
                        add_schemes.COMPANY             = company_name
                        
                        # add_schemes.FUND_CODE           = row["plan_name"]
                        # add_schemes.SCHEME_CODE         = row["scheme_type"]
                        add_schemes.SCHEME_NAME         = row["name"]
                        add_schemes.ISIN_NO             = row["isin_no"]
                        add_schemes.save()
                    elif company_name == "kfintech":
                        add_schemes, created = Cams_kfintech_schemes_master.objects.get_or_create(
                            PRODCODE=row["Product Code"]
                        )
                        add_schemes.COMPANY             = company_name
                        add_schemes.FUND_CODE           = row["Fund"]
                        add_schemes.SCHEME_CODE         = row["Scheme Code"]
                        add_schemes.SCHEME_NAME         = row["Fund Description"]
                        add_schemes.ISIN_NO             = row["SchemeISIN"]                       
                        add_schemes.save()
                    else:
                        return JsonResponse("Please Check Company Name", safe=False, status=412)
                    
            end_time = time.time()
            total_time = "%.2f" % (end_time - start_time)

            minutes = float(total_time) // 60
            seconds = float(total_time) % 60

            formatted_time = f"{minutes} minutes and {seconds:.2f} seconds"
            logger.info(f"formatted_time = {formatted_time}")
            messages.success(request, "Scheme Add Successfully")
            return JsonResponse("Scheme Add Successfully", safe=False, status=200)
        else:
            return JsonResponse("Upload Only .xls or .xlsx Format", safe=False, status=412)
    except Exception as e:
        logger.exception(e)
        # messages.error(request,"Something went wrong")
        return JsonResponse("Something went Wrong", safe=False, status=500)
    

def load_cams_kfintech_schemes(request):
   data = list(Cams_kfintech_schemes_master.objects.filter(IS_DELETED=False).values("COMPANY","FUND_CODE","SCHEME_CODE","PRODCODE","SCHEME_NAME","ISIN_NO"))
   return JsonResponse({"data": data}, safe=False, status=200)

@api_view(["POST"])
def add_bulk_cams_kfintech_mailback(request):
    try:
        excel_file      = request.FILES.get("excel_file")
        company_name    = request.data.get("company_name")
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
            if company_name == "cams":
                for _, row in df.iterrows():
                    # if Cams_kfintech_schemes_master.objects.filter(PRODCODE=row["prodcode"]).exists():
                    add_schemes, _ = Cams_kfintech_schemes_master.objects.get_or_create(PRODCODE=row["prodcode"],COMPANY=company_name, defaults={"SCHEME_NAME": row['scheme'],"FUND_CODE" :row['amc_code']})
                    investor, _ = customer_transaction.objects.get_or_create(PAN_NO=row["pan"], defaults={"CUST_NAME": row["inv_name"]})
                    
                    if not Cams_kfintech_transaction_details.objects.filter(TRXNNO=row['trxnno']).exists():
                        cams_transaction, created = Cams_kfintech_transaction.objects.get_or_create(
                            PROD_CODE   = add_schemes,
                            INV_NAME    = investor,
                            FOLIO_NO    = row['folio_no'],
                        )
                        add = Cams_kfintech_transaction_details.objects.create(
                            FOLIO_NO            = cams_transaction,
                            COMPANY             = "cams",
                            TRXNTYPE            = row['trxntype'],
                            TRXNNO              = row['trxnno'],
                            TRXNMODE            = row['trxnmode'],
                            TRXNSTAT            = row['trxnstat'],
                            USERCODE            = row['usercode'],
                            USRTRXNO            = row['usrtrxno'],                            
                            PURPRICE            = row['purprice'],
                            UNITS               = row['units'],
                            AMOUNT              = row['amount'],
                            SUBBROK             = row['subbrok'],
                            TRXN_NATURE         = row['trxn_nature'],
                            SWFLAG              = row['swflag'],
                            OLD_FOLIO_NO        = row['old_folio'],
                            SEQ_NO              = row['seq_no'],
                            REINVEST_FLAG       = row['reinvest_flag'],
                            LOCATION            = row['location'],
                            SCHEME_TYPE         = row['scheme_type'],
                            TAX_STATUS          = row['tax_status'],
                            PAN_NO              = row['pan'],
                            TARG_SRC_SCHEME     = row['targ_src_scheme'],
                            TRXN_TYPE_FLAG      = row['trxn_type_flag'],
                            TRXN_SUFFIX         = row['trxn_suffix'],
                            SIPTRXNNO           = row['siptrxnno'],
                            TER_LOCATION        = row['ter_location'],
                            EUIN                = row['euin'],
                            EUIN_VALID          = row['euin_valid'],
                            EUIN_OPTED          = row['euin_opted'],
                            SUB_BRK_ARN         = row['sub_brk_arn'],
                            SRC_BRK_CODE        = row['src_brk_code'],
                        
                            ACC_NO              = row['ac_no'],
                            BANK_NAME           = row['bank_name'],
                            GST_STATE_CODE      = row['gst_state_code'],
                            STAMP_DUTY          = row['stamp_duty'],
                        )
                        if not pd.isna(row['traddate']):
                            add.TRADDATE = row['traddate'].date()  # Directly convert Timestamp to date
                        if not pd.isna(row['postdate']):
                            add.POSTDATE = row['postdate'].date()
                        if not pd.isna(row['sys_regn_date']):
                            add.SYS_REGN_DATE = row['sys_regn_date'].date()
                        add.save()
            else:              
                for _, row in df.iterrows():
                    add_schemes, _ = Cams_kfintech_schemes_master.objects.get_or_create(PRODCODE=row["Product Code"],COMPANY=company_name, defaults={"SCHEME_NAME": row['Fund Description'],"FUND_CODE" :row['Fund'],"SCHEME_CODE" :row['Scheme Code']})
                    investor, _ = customer_transaction.objects.get_or_create(PAN_NO=row["PAN1"], defaults={"CUST_NAME": row["Investor Name"]})
                    
                    if not Cams_kfintech_transaction_details.objects.filter(FOLIO_NO__INV_NAME__PAN_NO=row["PAN1"],TRADDATE=row['Transaction Date'].date(),POSTDATE=row['Process Date'].date(),USRTRXNO=row['Transaction ID'],UNITS=row['Units']).exists():
                        cams_transaction, created = Cams_kfintech_transaction.objects.get_or_create(
                            PROD_CODE   = add_schemes,
                            INV_NAME    = investor,
                            FOLIO_NO    = row['Folio Number'],
                        )
                        add = Cams_kfintech_transaction_details.objects.create(
                            FOLIO_NO            = cams_transaction,
                            COMPANY             = "kfintech",
                            TRXNTYPE            = row['Transaction Type'],
                            TRXNNO              = row['Transaction Number'],
                            TRXNMODE            = row['Transaction Mode'],
                            TRXNSTAT            = row['Transaction Status'],

                            # USERCODE            = row['usercode'],
                            USRTRXNO            = row['Transaction ID'],
                            
                            PURPRICE            = row['Price'],
                            UNITS               = row['Units'],
                            AMOUNT              = row['Amount'],
                            SUBBROK             = row['Sub-Broker Code'],
                            TRXN_NATURE         = row['Transaction Description'],
                            # SWFLAG              = row['swflag'],
                            # OLD_FOLIO_NO        = row['old_folio'],
                            # SEQ_NO              = row['seq_no'],
                            # REINVEST_FLAG       = row['reinvest_flag'],
                            # LOCATION            = row['location'],
                            # SCHEME_TYPE         = row['scheme_type'],
                            # TAX_STATUS          = row['Status'],
                            PAN_NO              = row['PAN1'],
                            TARG_SRC_SCHEME     = row['ToProductCode'],
                            # TRXN_TYPE_FLAG      = row['trxn_type_flag'],
                            # TRXN_SUFFIX         = row['trxn_suffix'],
                            # SIPTRXNNO           = row['siptrxnno'],
                            # TER_LOCATION        = row['ter_location'],
                            EUIN                = row['EUIN'],
                            EUIN_VALID          = row['EUIN Valid Indicator'],
                            EUIN_OPTED          = row['EUIN Declaration Indicator'],
                            # SUB_BRK_ARN         = row['sub_brk_arn'],
                            SRC_BRK_CODE        = row['Sub-Broker Code'],
                        
                            # ACC_NO              = row['ac_no'],
                            BANK_NAME           = row['Instrument Bank'],
                            # GST_STATE_CODE      = row['gst_state_code'],
                            STAMP_DUTY          = row['Stamp Duty Charges'],
                        )
                        # if row['traddate']:
                        #     add.TRADDATE            = datetime.strptime(row["traddate"], "%d-%b-%Y").date()
                        #     # add.TRADDATE            = row['traddate']
                        # if row['postdate']:
                        #     add.POSTDATE            = datetime.strptime(row["postdate"], "%d-%b-%Y").date()
                        # if row['sys_regn_date']:
                        #     add.SYS_REGN_DATE       = datetime.strptime(row["sys_regn_date"], "%d-%b-%Y").date()
                        if not pd.isna(row['Transaction Date']):
                            add.TRADDATE = row['Transaction Date'].date()  # Directly convert Timestamp to date
                        if not pd.isna(row['Process Date']):
                            add.POSTDATE = row['Process Date'].date()
                        if not pd.isna(row['SIP Regn Date']):
                            add.SYS_REGN_DATE = row['SIP Regn Date'].date()
                        add.save()
        end_time = time.time()
        total_time = "%.2f" % (end_time - start_time)

        minutes = float(total_time) // 60
        seconds = float(total_time) % 60

        formatted_time = f"{minutes} minutes and {seconds:.2f} seconds"
        logger.info(f"formatted_time = {formatted_time}")
        messages.success(request, "Mailback Report Add Successfully")
        return JsonResponse("Mailback Report Add Successfully", safe=False, status=200)
    except Exception as e:
        logger.exception(e)
        # messages.error(request,"Something went wrong")
        return JsonResponse("Something went Wrong", safe=False, status=500)

def mailback_transaction(request):
    # context = {
    #     "cust_data" : customer_transaction.objects.values("id","PAN_NO","CUST_NAME")
    # }
    return render(request,"admin_panel/mailback_transaction.html")

def load_mailback_transaction(request):
    try:
    # data = Cams_transaction.objects.values_list("id",flat=True)
        data = list(Cams_kfintech_transaction.objects.values("id","PROD_CODE__PRODCODE","PROD_CODE__SCHEME_NAME","INV_NAME__PAN_NO","INV_NAME__CUST_NAME","FOLIO_NO"))

        for idx, i in enumerate(data):
            record_id = data[idx]["id"]
            i["TOTAL_PURPRICE"] = round(Cams_kfintech_transaction_details.objects.filter(FOLIO_NO=record_id).aggregate(Sum('PURPRICE'))['PURPRICE__sum'] or 0,2)
            i["TOTAL_UNITS"]    = round(Cams_kfintech_transaction_details.objects.filter(FOLIO_NO=record_id).aggregate(Sum('UNITS'))['UNITS__sum'] or 0,2)
            i["TOTAL_AMOUNT"]   = round(Cams_kfintech_transaction_details.objects.filter(FOLIO_NO=record_id).aggregate(Sum('AMOUNT'))['AMOUNT__sum'] or 0,2)

        return JsonResponse({"data":data},safe=False,status=200)
    except Exception as e:
        logger.exception(e)
        # messages.error(request,"Something went wrong")
        return JsonResponse("Something went Wrong", safe=False, status=500)


def get_folio_investment(request,id):
    data = list(Cams_kfintech_transaction_details.objects.filter(FOLIO_NO=id).values("id","PURPRICE","UNITS","AMOUNT","TRADDATE","POSTDATE","SYS_REGN_DATE").order_by("TRADDATE"))
    logger.info(f"county = {len(data)}")
    return JsonResponse(data,safe=False,status=200)

def cams_kfintech_scheme_nav(request):
    return render(request, "admin_panel/cams_kfintech_scheme_nav.html")

@api_view(["POST"])
def add_bulk_cams_kfintech_nav(request):
    try:
        excel_file      = request.FILES.get("excel_file")
        company_name    = request.data.get("company_name")
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
            if company_name == "cams":
                for _, row in df.iterrows():
                    add_schemes, _ = Cams_kfintech_schemes_master.objects.get_or_create(PRODCODE=row["prodcode"],COMPANY=company_name, defaults={"SCHEME_NAME": row['name'],"NAV_VALUE": row['nav_value'],"ISIN_NO":row['isin_no']})
                    # add_schemes, _ = Cams_kfintech_schemes_master.objects.get_or_create(PRODCODE=row["prodcode"],COMPANY=company_name, defaults={"SCHEME_NAME": row['name'],"NAV_VALUE": row['nav_value'],"ISIN_NO":row['isin_no'],"FUND_CODE" :row['amc_code']})

                    if not Cams_kfintech_NAV.objects.filter(PRODCODE__id=add_schemes.id,NAV_DATE = row['nav_date'].date(),NAV_VALUE=row['nav_value']).exists():
                        add = Cams_kfintech_NAV.objects.create(
                            COMPANY         = company_name,
                            PRODCODE        = add_schemes,
                            NAV_VALUE       = round(row['nav_value'],2)
                            )
                        if not pd.isna(row['nav_date']):
                            add.NAV_DATE    = row['nav_date'].date()  # Directly convert Timestamp to date
                        add.save()
            else:              
                for _, row in df.iterrows():
                    add_schemes, _ = Cams_kfintech_schemes_master.objects.get_or_create(PRODCODE=row["Product Code"],COMPANY=company_name, defaults={"FUND_CODE":row["Fund"],"SCHEME_CODE": row["Scheme Code"],"SCHEME_NAME": row['Fund Description'],"ISIN_NO":row['SchemeISIN'],"NAV_VALUE": row['NAV']})
                                    
                    if not Cams_kfintech_NAV.objects.filter(PRODCODE__id=add_schemes.id,NAV_DATE = row['NAV Date'].date(),NAV_VALUE=row['NAV']).exists():
                        add = Cams_kfintech_NAV.objects.create(
                            COMPANY         = company_name,
                            PRODCODE        = add_schemes,
                            NAV_VALUE       = round(row['NAV'],2)
                            )
                        if not pd.isna(row['NAV Date']):
                            add.NAV_DATE    = row['NAV Date'].date()  # Directly convert Timestamp to date
                        add.save()

        total_time = "%.2f" % (time.time() - start_time)
        formatted_time = f"{float(total_time) // 60} minutes and {float(total_time) % 60:.2f} seconds"
        logger.info(f"formatted_time = {formatted_time}")
        messages.success(request, "NAV Report Add Successfully")
        return JsonResponse("NAV Report Add Successfully", safe=False, status=200)
    except Exception as e:
        logger.exception(e)
        return JsonResponse("Something went Wrong", safe=False, status=500)

def load_nav(request):
    try:
        # Get today's date
        # today = datetime.today()
        # # Subtract one day to get the previous date
        # previous_date = today - timedelta(days=1)
        latest_nav_date = Cams_kfintech_NAV.objects.aggregate(latest_date=Max('NAV_DATE'))['latest_date']
        # logger.info(f"last_date = {latest_nav_date}")

        data = list(Cams_kfintech_NAV.objects.filter(NAV_DATE=latest_nav_date).values("id","COMPANY","PRODCODE__PRODCODE","PRODCODE__SCHEME_NAME","PRODCODE__ISIN_NO","NAV_DATE","NAV_VALUE"))
        # Get the latest NAV_DATE for each product
        # subquery = Cams_kfintech_NAV.objects.values('PRODCODE').annotate(latest_nav_date=Max('NAV_DATE'))
        
        # # Fetch the NAV data for the latest date for each product
        # data = list(Cams_kfintech_NAV.objects.filter(
        #     NAV_DATE__in=[entry['latest_nav_date'] for entry in subquery]
        # ).values("id", "COMPANY", "PRODCODE__PRODCODE", "PRODCODE__SCHEME_NAME", "PRODCODE__ISIN_NO", "NAV_DATE", "NAV_VALUE"))
        return JsonResponse({"data":data},safe=False,status=200)
    except Exception as e:
        logger.exception(e)
        # messages.error(request,"Something went wrong")
        return JsonResponse("Something went Wrong", safe=False, status=500)




def buy_list(request):
    return render(request, "admin_panel/buy_list.html")


def load_buy_list(request):
    data = list(Buy.objects.values("id", "USER__CAN", "USER__PAN_NO", "USER__NAME","GROUPORDERNO").order_by("-id"))
    return JsonResponse({"data": data}, safe=False, status=200)


def buy_detail(request, id):
    data = {
        "buy": Buy.objects.get(id=id),
        "buy_schemes": Buy_schemes.objects.filter(BUY__id=id),
    }
    return render(request, "admin_panel/buy_detail.html", context={"data": data})


def sales_list(request):
    return render(request, "admin_panel/sales_list.html")


def sales_detail(request, id):
    data = {
        "redeem": Redeem.objects.get(id=id),
        "Redeem_schemes": Redeem_schemes.objects.filter(id=id),
    }
    return render(request, "admin_panel/sales_detail.html", context={"data": data})


def load_sales_list(request):
    data = list(
        Redeem.objects.values("id", "USER__CAN", "USER__PAN_NO", "USER__NAME").order_by(
            "-id"
        )
    )
    return JsonResponse({"data": data}, safe=False, status=200)


def scheme_category(request):
    return render(request, "admin_panel/scheme_category.html")


def scheme_sub_category(request):
    data = Scheme_category.objects.values("id", "CATEGORY")
    return render(
        request, "admin_panel/scheme_sub_category.html", context={"data": data}
    )


def amc(request):
    return render(request, "admin_panel/amc.html")


def remove_extra_space(request):
    for i in Schemes.objects.all():
        b = i.SCHEME_CODE
        b = b.strip()
        f = i.FUND_CODE
        f = f.strip()
        d = i.DIV_OPT
        d = d.strip()
        Schemes.objects.filter(id=i.id).update(SCHEME_CODE=b, FUND_CODE=f, DIV_OPT=d)

    return JsonResponse("success", safe=False, status=200)


def check_amc(request):
    data = AMC.objects.all()
    for i in AMC.objects.all():
        logger.info(f"iii {i.FUND_CODE} = {i.FUND_NAME}")
        Schemes.objects.filter(FUND_CODE=i.FUND_CODE).update(
            AMC=AMC.objects.get(FUND_CODE=i.FUND_CODE)
        )
    return JsonResponse("success", safe=False, status=200)


@api_view(["POST"])
def add_amc_api(request):
    try:
        fund_code = request.POST.get("fund_code")
        fund_name = request.POST.get("fund_name")

        logger.info(f"""
            fund_code        = {fund_code}
            fund_name        = {fund_name}
        """)

        if AMC.objects.filter(FUND_CODE=fund_code, FUND_NAME=fund_name).exists():
            return JsonResponse("This AMC Is Already Exist", safe=False, status=412)
        else:
            add = AMC.objects.create(FUND_CODE=fund_code, FUND_NAME=fund_name)
        return JsonResponse("AMC Add Successfully", safe=False, status=200)
    except Exception as e:
        logger.exception(e)
        return JsonResponse("something went wrong", safe=False, status=500)


def get_amc(request, id):
    data = list(AMC.objects.filter(id=id).values("id", "FUND_CODE", "FUND_NAME"))
    return JsonResponse(data, safe=False)


@api_view(["POST"])
def edit_amc(request, id):
    try:
        fund_code = request.POST.get("fund_code")
        fund_name = request.POST.get("fund_name")

        if (
            AMC.objects.filter(FUND_CODE=fund_code, FUND_NAME=fund_name)
            .exclude(id=id)
            .exists()
        ):
            return JsonResponse("This AMC Is Already Exist", safe=False, status=412)
        else:
            edit = AMC.objects.get(id=id)
            edit.FUND_CODE = fund_code
            edit.FUND_NAME = fund_name
            edit.save()
        return JsonResponse("AMC Add Successfully", safe=False, status=200)
    except Exception as e:
        logger.exception(e)
        return JsonResponse("something went wrong", safe=False, status=500)


def load_amc_table(request):
    data = list(AMC.objects.values("id", "FUND_CODE", "FUND_NAME").order_by("-id"))
    return JsonResponse({"data": data}, safe=False, status=200)


def load_amc(request):
    data = list(AMC.objects.values("id", "FUND_CODE", "FUND_NAME"))
    return JsonResponse(data, safe=False, status=200)

def calculated_xirr(purchase_date, nav_date,total_amt,market_value):
    if isinstance(purchase_date, str):
        purchase_date = datetime.strptime(purchase_date, '%Y-%m-%d').date()  # Example format
    if isinstance(nav_date, str):
        nav_date = datetime.strptime(nav_date, '%Y-%m-%d').date()  # Example format

    delta = (nav_date - purchase_date).days
    days_in_year = 365
    if delta == 0 or total_amt == 0:
        return 0  # or some other fallback value

    xirr = round((((market_value/total_amt)**(1/(delta / days_in_year)))-1)*100,2)
    return xirr

def valuation_reports(request):
    context = {
        "cust_data" : customer_transaction.objects.values("id","PAN_NO","CUST_NAME")
    }
    return render(request, "admin_panel/valuation_reports.html",context=context)

# transaction_type = []
        
        # trans_type = list(Cams_kfintech_transaction_details.objects.filter(FOLIO_NO=record_id).values("TRXN_NATURE","AMOUNT").order_by("TRADDATE"))

        # for index, j in enumerate(trans_type):
        #     purprice = j["AMOUNT"]

        #     if company_name == "cams":
        #         if "Fresh Purchase" in j['TRXN_NATURE']:
        #             if "Purchase" not in  transaction_type:
        #                 transaction_type.append("Purchase")
        #         elif "Instalment" in j['TRXN_NATURE']:
        #             if "Sip" not in  transaction_type:
        #                 transaction_type.append("Sip")
        #         elif "systematic-bse -" in j['TRXN_NATURE'].lower():
        #             if "Sip" not in  transaction_type:
        #                 transaction_type.append("Sip")
        #         elif "Switch-In" in j['TRXN_NATURE']:
        #             if "Switch-In" not in  transaction_type:
        #                 transaction_type.append("Switch-In")
        #     else:
        #         if "Purchase" in j['TRXN_NATURE']:
        #             if len(trans_type) > 1:

        #                 if index > 0:
        #                     prev_purprice = trans_type[index - 1]["AMOUNT"]
        #                     if prev_purprice == purprice:
        #                         transacrion_nature = "Sip"
        #                     else:
        #                         transacrion_nature = "Purchase"
        #                 else:
        #                     next_purprice = trans_type[index + 1]["AMOUNT"]
        #                     # logger.info(f"next_purprice {type(next_purprice)} {next_purprice}")
        #                     if next_purprice == purprice:
        #                         transacrion_nature = "Sip"
        #                     else:
        #                         transacrion_nature = "Purchase"
        #             else:
        #                 transacrion_nature = "Purchase"
        #             if f"{transacrion_nature}" not in  transaction_type:
        #                 transaction_type.append(f'{transacrion_nature}')

        #         elif "Investment" in j['TRXN_NATURE']:
        #             if "Sip" not in  transaction_type:
        #                 transaction_type.append("Sip")
        #         elif "Lateral Shift In" in j['TRXN_NATURE']:
        #             if "Switch-In" not in  transaction_type:
        #                 transaction_type.append("Switch-In")

        # i["TRANSACTION_TYPE"] = " + ".join(sorted(transaction_type))


# def specific_data(i,api_use,company_name,fund_code,scheme_code,product_code):
#     if company_name == "cams":
#         # text[:-1] 
#         i['MFU_FUND_CODE']      = fund_code
#         i['MFU_SCHEME_CODE']    = scheme_code
        
#         i['MFU_PLAN_ID'] = i['MFU_PLAN_NAME'] = ""
#         i['LUMPSUM_MIN_AMT'] = i['SWP_MIN_AMT'] = i['REDEEM_MIN_AMT'] = i['SWITCH_MIN_AMT'] = 0
#         i['LUMPSUM_ALLOWED'] = i['SWP_ALLOWED'] = i['REDEEM_ALLOWED'] = i['SWITCH_OUT_ALLOWED'] = i['STP_OUT_ALLOWED'] = False
        
#         # product_code
#         # Create the annotation with concatenated scheme_code_func_code
#         exists = Schemes.objects.annotate(
#             scheme_code_func_code=Concat('FUND_CODE__FUND_CODE',Value(''),'SCHEME_CODE', output_field=CharField())
#         ).filter(scheme_code_func_code=product_code).exists()

#         if exists:
#             # Retrieve the record since it exists
#             scheme_data = Schemes.objects.annotate(
#                 scheme_code_func_code=Concat('FUND_CODE__FUND_CODE',Value(''),'SCHEME_CODE', output_field=CharField())
#             ).get(scheme_code_func_code=product_code)
#             scheme_code = scheme_data.SCHEME_CODE
#             fund_code   = scheme_data.FUND_CODE.FUND_CODE
#             i['MFU_FUND_CODE']      = fund_code
#             i['MFU_SCHEME_CODE']    = scheme_code
#             i['MFU_PLAN_ID']        = scheme_data.id
#             i['MFU_PLAN_NAME']      = scheme_data.PLAN_NAME
#             i['DIV_OPT']            = scheme_data.DIV_OPT

#             # Ordering by MIN_AMT to get the smallest
#             i['LUMPSUM_MIN_AMT']    = Threshold.objects.filter(
#                                         SCHEME_CODE=scheme_code,
#                                         FUND_CODE__FUND_CODE=fund_code,
#                                         TXN_TYPE="A"
#                                     ).order_by('-MIN_AMT').values_list('MIN_AMT', flat=True).first() or 0
#             i['SWP_MIN_AMT']        = Threshold.objects.filter(
#                                         SCHEME_CODE=scheme_code,
#                                         FUND_CODE__FUND_CODE=fund_code,
#                                         TXN_TYPE="J"
#                                     ).order_by('-MIN_AMT').values_list('MIN_AMT', flat=True).first() or 0
#             i['REDEEM_MIN_AMT']     = Threshold.objects.filter(
#                                         SCHEME_CODE=scheme_code,
#                                         FUND_CODE__FUND_CODE=fund_code,
#                                         TXN_TYPE="R"
#                                     ).order_by('-MIN_AMT').values_list('MIN_AMT', flat=True).first() or 0
#             i['SWITCH_MIN_AMT']     = Threshold.objects.filter(
#                                         SCHEME_CODE__icontains=scheme_code,
#                                         FUND_CODE__COMPANY_FUND_CODE=fund_code,
#                                         TXN_TYPE="O"
#                                     ).order_by('-MIN_AMT').values_list('MIN_AMT', flat=True).first() or 0

#             i['LUMPSUM_ALLOWED']    = True if scheme_data.PUR_ALLOWED == "Y" else False
#             i['SWP_ALLOWED']        = True if scheme_data.SWP_ALLOWED == "Y" else False
#             i['REDEEM_ALLOWED']     = True if scheme_data.REDEEM_ALLOWED == "Y" else False
#             i['SWITCH_OUT_ALLOWED'] = True if scheme_data.SWITCH_OUT_ALLOWED == "Y" else False
#             i['STP_OUT_ALLOWED']    = True if scheme_data.STP_OUT_ALLOWED == "Y" else False
                    
#     else:

#         i['MFU_PLAN_ID'] = i['MFU_PLAN_NAME'] = ""
#         i['LUMPSUM_MIN_AMT'] = i['SWP_MIN_AMT'] = i['REDEEM_MIN_AMT'] = i['SWITCH_MIN_AMT'] = 0
#         i['LUMPSUM_ALLOWED'] = i['SWP_ALLOWED'] = i['REDEEM_ALLOWED'] = i['SWITCH_OUT_ALLOWED'] = i['STP_OUT_ALLOWED'] = False
        
#         if Schemes.objects.filter(SCHEME_CODE__icontains=scheme_code,FUND_CODE__COMPANY_FUND_CODE=fund_code,FUND_CODE__COMPANY="kfintech").exists():
#             scheme_data = Schemes.objects.get(SCHEME_CODE__icontains=scheme_code,FUND_CODE__COMPANY_FUND_CODE=fund_code,FUND_CODE__COMPANY="kfintech")
#             i['MFU_PLAN_ID']        = scheme_data.id
#             i['MFU_PLAN_NAME']      = scheme_data.PLAN_NAME
#             i['MFU_FUND_CODE']      = scheme_data.FUND_CODE.FUND_CODE
#             i['MFU_SCHEME_CODE']    = scheme_data.SCHEME_CODE
#             i['DIV_OPT']            = scheme_data.DIV_OPT

#             # Ordering by MIN_AMT to get the smallest= True
#             i['LUMPSUM_MIN_AMT']    = Threshold.objects.filter(
#                                         SCHEME_CODE__icontains=scheme_code,
#                                         FUND_CODE__COMPANY_FUND_CODE=fund_code,
#                                         TXN_TYPE="A"
#                                     ).order_by('-MIN_AMT').values_list('MIN_AMT', flat=True).first() or 0
#             i['SWP_MIN_AMT']        = Threshold.objects.filter(
#                                         SCHEME_CODE__icontains=scheme_code,
#                                         FUND_CODE__COMPANY_FUND_CODE=fund_code,
#                                         TXN_TYPE="J"
#                                     ).order_by('-MIN_AMT').values_list('MIN_AMT', flat=True).first() or 0
            
#             i['REDEEM_MIN_AMT']     = Threshold.objects.filter(
#                                         SCHEME_CODE__icontains=scheme_code,
#                                         FUND_CODE__COMPANY_FUND_CODE=fund_code,
#                                         TXN_TYPE="R"
#                                     ).order_by('-MIN_AMT').values_list('MIN_AMT', flat=True).first() or 0

#             i['SWITCH_MIN_AMT']     = Threshold.objects.filter(
#                                         SCHEME_CODE__icontains=scheme_code,
#                                         FUND_CODE__COMPANY_FUND_CODE=fund_code,
#                                         TXN_TYPE="O"
#                                     ).order_by('-MIN_AMT').values_list('MIN_AMT', flat=True).first() or 0
            
#             i['LUMPSUM_ALLOWED']    = True if scheme_data.PUR_ALLOWED == "Y" else False
#             i['SWP_ALLOWED']        = True if scheme_data.SWP_ALLOWED == "Y" else False
#             i['REDEEM_ALLOWED']     = True if scheme_data.REDEEM_ALLOWED == "Y" else False
#             i['SWITCH_OUT_ALLOWED'] = True if scheme_data.SWITCH_OUT_ALLOWED == "Y" else False
#             i['STP_OUT_ALLOWED']    = True if scheme_data.STP_OUT_ALLOWED == "Y" else False

# ----------------------------------  Start consolidated_valuation_report_page Start ---------------------------------- 
def fetch_nav_data(product_code):
    return Cams_kfintech_NAV.objects.filter(PRODCODE__PRODCODE=product_code).values("NAV_DATE", "NAV_VALUE").order_by('NAV_DATE').last()

def fetch_transaction_details(record_id, exclude_conditions):
    return Cams_kfintech_transaction_details.objects.filter(FOLIO_NO=record_id).exclude(**exclude_conditions).values("COMPANY", "TRXN_NATURE", "PURPRICE","UNITS","AMOUNT", "TRADDATE","TRXN_TYPE_FLAG").order_by("TRADDATE")


def calculate_transaction_type(trans_type, company_name):

    value_of_sip = []
    # total_value_of_sip  += sip_amt
    transaction_type = []
    for index, trans in enumerate(trans_type):
        trxn_nature = trans['TRXN_NATURE']
        purprice = trans["AMOUNT"]

        # cams company conditions
        if company_name == "cams":
            if "purchase" in trxn_nature.lower() and "Purchase" not in transaction_type:
                transaction_type.append("Purchase")
            elif any(key in trxn_nature.lower() for key in ["instalment", "systematic"]) and "Sip" not in transaction_type:
                transaction_type.append("Sip")
                if not value_of_sip:
                    value_of_sip.append(round(float(purprice)))
            elif "Switch-In" in trxn_nature and "Switch-In" not in transaction_type:
                transaction_type.append("Switch-In")

        # other companies conditions
        else:
            transaction_nature = "Purchase"
            if "Purchase" in trxn_nature:
                if len(trans_type) > 1 and (
                    (index > 0 and trans_type[index - 1]["AMOUNT"] == purprice) or
                    (index < len(trans_type) - 1 and trans_type[index + 1]["AMOUNT"] == purprice)
                ):
                    transaction_nature = "Sip"
                    if not value_of_sip:
                        value_of_sip.append(round(float(purprice)))
            elif "Investment" in trxn_nature:
                transaction_nature = "Sip"
                if not value_of_sip:
                    value_of_sip.append(round(float(purprice)))
            elif "Lateral Shift In" in trxn_nature:
                transaction_nature = "Switch-In"

            if transaction_nature not in transaction_type:
                transaction_type.append(transaction_nature)
    # logger.info(f"value_of_sip = {value_of_sip}")
    return " + ".join(sorted(transaction_type)),value_of_sip

def safe_float(value):
    try:
        return float(value)
    except (ValueError, TypeError):
        return 0.0  # Return 0.0 if conversion fails

'''Use in set_scheme_data'''
def get_value_of_sip(trans_type):
    sip_amt     = 0
    sip_count   = 0
    for detail in trans_type:
        trxn_nature = detail['TRXN_NATURE'].lower()
        sip_amt     = round(float(detail['AMOUNT']))
        sip_count   = 1
        if "systematic 1" in trxn_nature or "systematic-nse" in trxn_nature or "systematic-bse" in trxn_nature or "instalment" in trxn_nature or "investment" in trxn_nature:  
            return sip_amt ,sip_count
    return sip_amt , sip_count



'''Use in set_scheme_data'''
def get_min_amt(thresholds, scheme_code, fund_code, txn_type):
    """Helper function to retrieve the minimum amount based on conditions."""
    return thresholds.filter(
        SCHEME_CODE__icontains=scheme_code,
        FUND_CODE__COMPANY_FUND_CODE=fund_code,
        TXN_TYPE=txn_type
    ).order_by('-MIN_AMT').values_list('MIN_AMT', flat=True).first() or 0


def set_scheme_data(i, scheme_data, thresholds):
    """Helper function to set scheme-related data."""
    scheme_code = scheme_data.SCHEME_CODE
    fund_code = scheme_data.FUND_CODE.FUND_CODE
    
    i.update({
        'MFU_FUND_CODE': fund_code,
        'MFU_SCHEME_CODE': scheme_code,
        'MFU_PLAN_ID': scheme_data.id,
        'MFU_PLAN_NAME': scheme_data.PLAN_NAME,
        'DIV_OPT': scheme_data.DIV_OPT,
        'LUMPSUM_MIN_AMT': get_min_amt(thresholds, scheme_code, fund_code, "A"),
        'SWP_MIN_AMT': get_min_amt(thresholds, scheme_code, fund_code, "J"),
        'REDEEM_MIN_AMT': get_min_amt(thresholds, scheme_code, fund_code, "R"),
        'SWITCH_MIN_AMT': get_min_amt(thresholds, scheme_code, fund_code, "O"),
        'LUMPSUM_ALLOWED': scheme_data.PUR_ALLOWED == "Y",
        'SWP_ALLOWED': scheme_data.SWP_ALLOWED == "Y",
        'REDEEM_ALLOWED': scheme_data.REDEEM_ALLOWED == "Y",
        'SWITCH_OUT_ALLOWED': scheme_data.SWITCH_OUT_ALLOWED == "Y",
        'STP_OUT_ALLOWED': scheme_data.STP_OUT_ALLOWED == "Y",
    })


def specific_data(i, api_use, company_name, fund_code, scheme_code, product_code):
    thresholds = Threshold.objects.all()
    
    # Initialize with default values
    i.update({
        'MFU_PLAN_ID': '',
        'MFU_PLAN_NAME': '',
        'LUMPSUM_MIN_AMT': 0,
        'SWP_MIN_AMT': 0,
        'REDEEM_MIN_AMT': 0,
        'SWITCH_MIN_AMT': 0,
        'LUMPSUM_ALLOWED': False,
        'SWP_ALLOWED': False,
        'REDEEM_ALLOWED': False,
        'SWITCH_OUT_ALLOWED': False,
        'STP_OUT_ALLOWED': False
    })

    # Check conditions for CAMS or kfintech
    if company_name == "cams":
        exists = Schemes.objects.annotate(
            scheme_code_func_code=Concat('FUND_CODE__FUND_CODE', Value(''), 'SCHEME_CODE', output_field=CharField())
        ).filter(scheme_code_func_code=product_code).exists()
        
        if exists:
            scheme_data = Schemes.objects.annotate(
                scheme_code_func_code=Concat('FUND_CODE__FUND_CODE', Value(''), 'SCHEME_CODE', output_field=CharField())
            ).get(scheme_code_func_code=product_code)
            set_scheme_data(i, scheme_data, thresholds)
    else:
        if Schemes.objects.filter(
            SCHEME_CODE__icontains=scheme_code,
            FUND_CODE__COMPANY_FUND_CODE=fund_code,
            FUND_CODE__COMPANY="kfintech"
        ).exists():
            scheme_data = Schemes.objects.get(
                SCHEME_CODE__icontains=scheme_code,
                FUND_CODE__COMPANY_FUND_CODE=fund_code,
                FUND_CODE__COMPANY="kfintech"
            )
            set_scheme_data(i, scheme_data, thresholds)

def consolidated_valuation_report_page(request):
    try:
        from_date       = request.GET.get("from_date")
        to_date         = request.GET.get("to_date")
        
        device_type     = request.GET.get("device_type")
        api_use         = request.GET.get("api_use")
        app_type        = request.GET.get("app_type")
        kwargs = {}
        if app_type == "ep_advisor":   
            login_id            = request.GET.get("login_id")
            login_user_type     = request.GET.get("login_user_type")

           
            client_pan = Registration_personal_details.objects.filter(RM_EP=login_id,TYPE=login_user_type).values_list("PAN_NO",flat=True) 
            # client_pan      = request.GET.getlist("client_pan")
            kwargs['INV_NAME__PAN_NO__in'] = client_pan
        else:
            client_pan      = request.GET.get("client_pan")
            kwargs['INV_NAME__PAN_NO'] = client_pan
            user_info = {}
            # if api_use
            if customer_transaction.objects.filter(PAN_NO=client_pan).exists():
                user_info = customer_transaction.objects.get(PAN_NO=client_pan)
        data = list(
            Cams_kfintech_transaction.objects.filter(**kwargs)
            .values("id", "PROD_CODE__PRODCODE", "PROD_CODE__SCHEME_NAME", "INV_NAME__PAN_NO", "INV_NAME__CUST_NAME", "FOLIO_NO", "PROD_CODE__COMPANY","PROD_CODE__FUND_CODE","PROD_CODE__SCHEME_CODE")
            .order_by("PROD_CODE__SCHEME_NAME")
        )

        total_purprice_sum = total_units_sum = total_amount_sum = total_market_value_sum = total_gain_loss_sum = total_dividend_paid_sum =  0

        data = [i for i in data if fetch_nav_data(i['PROD_CODE__PRODCODE']) is not None]
        total_value_of_sip =[]
    
        for i in data:
            
            product_code    = i["PROD_CODE__PRODCODE"]
            company_name    = i["PROD_CODE__COMPANY"]
            fund_code       = i["PROD_CODE__FUND_CODE"]
            scheme_code     = i["PROD_CODE__SCHEME_CODE"]
            
            current_nav_data = fetch_nav_data(product_code)
            i["CURRENT_NAV"], i["CURRENT_NAV_DATE"] = current_nav_data["NAV_VALUE"], current_nav_data["NAV_DATE"]

            exclude_conditions = {} if company_name == "cams" else {'TRXN_NATURE__icontains': "rejection"}
            trans_type = fetch_transaction_details(i["id"], exclude_conditions)
            if device_type == "mobile" and api_use != "dashboard":
                specific_data(i,api_use,company_name,fund_code,scheme_code,product_code)
                
            # Filter transactions based on rules
            trans_type = [t for t in trans_type if not (t['COMPANY'] == "cams" and "insufficient balance" in t['TRXN_NATURE'].lower()) and not (t['COMPANY'] != "cams" and "rejection" in t['TRXN_NATURE'].lower())]

            i["TRANSACTION_TYPE"] ,value_of_sip = calculate_transaction_type(trans_type, company_name)
            '''Check value_of_sip is empty or not if not empty then extend total_value_of_sip list'''
            if value_of_sip:
                total_value_of_sip.extend(value_of_sip)

            agg_data            = {'purprice_sum': 0, 'units_sum': 0, 'amount_sum': 0,'dividend_paid': 0}

            for trans in trans_type:
                if "switchout" in trans['TRXN_NATURE'].lower():  # Reset the calculations upon Switch-Out
                    # skip_calculation = True
                    agg_data = {'purprice_sum': 0, 'units_sum': 0, 'amount_sum': 0,'dividend_paid': 0}
                    continue  # Skip any calculations after a Switch-Out

                else:
                    # In the loop
                    # logger.info(f"PURPRICE = {trans.get('PURPRICE', 0)}")
                    # if i['TRXN_NATURE'] == "Dividend Paid" and i['COMPANY'] == "cams":
                    if trans['TRXN_NATURE'] == "Dividend Paid" and trans['COMPANY'] == "cams":
                        agg_data['purprice_sum']    += 0
                        agg_data['units_sum']       += 0
                        agg_data['amount_sum']      += 0
                        agg_data['dividend_paid']   += safe_float(trans.get('AMOUNT', 0))
                    else:
                        agg_data['purprice_sum']    += safe_float(trans.get('PURPRICE', 0))
                        agg_data['units_sum']       += safe_float(trans.get('UNITS', 0))
                        agg_data['amount_sum']      += safe_float(trans.get('AMOUNT', 0))
                        agg_data['dividend_paid']   += 0
        # Aggregate data
            i.update({
                "TOTAL_PURPRICE"        : round(agg_data.get('purprice_sum', 0) or 0, 2),
                "TOTAL_UNITS"           : round(agg_data.get('units_sum', 0) or 0, 2),
                "TOTAL_AMOUNT"          : round(agg_data.get('amount_sum', 0) or 0, 2),
                "TOTAL_DIVIDEND_PAID"   : round(agg_data.get('dividend_paid', 0) or 0, 2)
            })

            # Calculate MARKET_VALUE based on CURRENT_NAV and TOTAL_UNITS
            i["MARKET_VALUE"] = round(float(i.get("CURRENT_NAV", 0)) * float(i.get("TOTAL_UNITS", 0)), 2)

            # Calculate GAIN_LOSS based on MARKET_VALUE and TOTAL_AMOUNT
            i["GAIN_LOSS"] = round(float(i.get("MARKET_VALUE", 0)) - float(i.get("TOTAL_AMOUNT", 0)) +  float(i.get("TOTAL_DIVIDEND_PAID", 0)), 2)

            # Retrieve the PURCHASE_DATE
            i["PURCHASE_DATE"] = Cams_kfintech_transaction_details.objects.filter(FOLIO_NO=i["id"]).aggregate(
                PURCHASE_DATE=Min('TRADDATE')
            )['PURCHASE_DATE']


            # Calculate ABS_RETURN, handling potential zero division for TOTAL_AMOUNT
            i["ABS_RETURN"] = round((i["GAIN_LOSS"] / float(i["TOTAL_AMOUNT"])) * 100, 2) if i["TOTAL_AMOUNT"] else 0

            # Calculate XIRR using PURCHASE_DATE and CURRENT_NAV_DATE
            i["XIRR"] = calculated_xirr(i["PURCHASE_DATE"], i.get("CURRENT_NAV_DATE"), i["TOTAL_AMOUNT"], i["MARKET_VALUE"])

            i["TOTAL_AMOUNT_COMMA"] = format_number(round(float(i.get("TOTAL_AMOUNT", 0)), 2), locale='en_IN')
            i["MARKET_VALUE_COMMA"] = format_number(round(float(i.get("MARKET_VALUE", 0)), 2), locale='en_IN')

            total_purprice_sum      += i["TOTAL_PURPRICE"]
            total_units_sum         += i["TOTAL_UNITS"]
            total_amount_sum        += i["TOTAL_AMOUNT"]
            total_market_value_sum  += i["MARKET_VALUE"]
            total_gain_loss_sum     += i["GAIN_LOSS"]
            total_dividend_paid_sum += i["TOTAL_DIVIDEND_PAID"]
            # if api_use == "dashboard":
            #     sip_amt ,sip_count            = get_value_of_sip(trans_type)
            #     total_value_of_sip  += sip_amt
            #     total_number_of_sip += sip_count
                
        if device_type == "mobile":
            try:
                if api_use == "dashboard":
                    if total_amount_sum != 0:
                        rate_abs = round(((total_market_value_sum - total_amount_sum) / total_amount_sum) * 100, 2)
                    else:
                        rate_abs = 0  # Default value if total_amount_sum is 0
                    # gain_or_loss_amt = round(total_amount_sum, 2) - round(total_market_value_sum, 2) + round(total_dividend_paid_sum, 2)
                    gain_or_loss_amt = round(total_market_value_sum, 2) + round(total_dividend_paid_sum, 2) - round(total_amount_sum, 2)
                    # logger.info(f"total_value_of_sip ={total_value_of_sip}")
                    context = {
                        "invested_amount"           : round(total_amount_sum, 2),
                        "market_value"              : round(total_market_value_sum, 2),
                        "total_dividend_paid"       : round(total_dividend_paid_sum, 2),
                        "gain_or_loss_amt"          : gain_or_loss_amt,
                        "invested_amount_comma"     : format_number(round(total_amount_sum, 2), locale='en_IN'), 
                        "market_value_comma"        : format_number(round(total_market_value_sum, 2), locale='en_IN'),
                        "total_dividend_paid_comma" : format_number(round(total_dividend_paid_sum, 2), locale='en_IN'),
                        "gain_or_loss_amt_comma"    : format_number(round(gain_or_loss_amt, 2), locale='en_IN'),
                        "rate_abs"                  : rate_abs,
                        "rate_ann"                  : "0",
                        "value_of_sip"              : format_number(sum(total_value_of_sip), locale='en_IN'),
                        "number_of_sip"             : len(total_value_of_sip)
                    }
                else:
                    context = {
                        "data"                      : data,
                        "summery_date"              : Cams_kfintech_NAV.objects.order_by('NAV_DATE').values("NAV_DATE").last()["NAV_DATE"],
                        "invested_amount"           : round(total_amount_sum, 2),
                        "market_value"              : round(total_market_value_sum, 2),
                        "grand_total"               : round(total_gain_loss_sum, 2),
                        "total_dividend_paid"       : round(total_dividend_paid_sum, 2),
                        "invested_amount_comma"     : format_number(round(total_amount_sum, 2), locale='en_IN'), 
                        "market_value_comma"        : format_number(round(total_market_value_sum, 2), locale='en_IN'),
                        "grand_total_comma"         : format_number(round(total_gain_loss_sum, 2), locale='en_IN'),
                        "total_dividend_paid_comma" : format_number(round(total_dividend_paid_sum, 2), locale='en_IN'),
                        
                    }
                return JsonResponse(context,safe=False,status=200)
            except Exception as e:
                logger.exception(e)
                return JsonResponse({"error":"something went wrong"},status=500)
        else:
            if total_amount_sum != 0:
                rate_abs = round((total_gain_loss_sum / float(total_amount_sum)) * 100, 2)
            else:
                rate_abs = 0  # Default value if total_amount_sum is 0
            context = {
                "data"                  : data,
                "user_info"             : user_info,
                "from_date"             : datetime.strptime(from_date, '%Y-%m-%d').date(),
                "to_date"               : datetime.strptime(to_date, '%Y-%m-%d').date(),
                "total_purprice_sum"    : round(total_purprice_sum, 2),
                "total_units_sum"       : round(total_units_sum, 2),
                "total_amount_sum"      : round(total_amount_sum, 2),
                "total_market_value_sum": round(total_market_value_sum, 2),
                "total_gain_loss_sum"   : round(total_gain_loss_sum, 2),
                "total_dividend_paid"   : round(total_dividend_paid_sum, 2),
                "total_abs_return"      : rate_abs,
            }
            return render(request, "admin_panel/consolidated_valuation_report_page.html", context=context)
    except Exception as e:
        logger.exception(e)
        return JsonResponse({"error":"something went wrong"},status=500)

# ----------------------------------  Start consolidated_valuation_report_page End ---------------------------------- 


# def consolidated_valuation_report_page(request):
#     from_date   = request.GET.get("from_date")
#     to_date     = request.GET.get("to_date")
#     client_pan  = request.GET.get("client_pan")

#     user_info   = customer_transaction.objects.get(PAN_NO=client_pan)
#     data        = list(Cams_kfintech_transaction.objects.filter(INV_NAME__PAN_NO=client_pan).values("id","PROD_CODE__PRODCODE","PROD_CODE__SCHEME_NAME","INV_NAME__PAN_NO","INV_NAME__CUST_NAME","FOLIO_NO","PROD_CODE__COMPANY").order_by("PROD_CODE__SCHEME_NAME"))

#     total_purprice_sum = total_units_sum = total_amount_sum = total_market_value_sum = total_gain_loss_sum = 0


#     data = [i for i in data if Cams_kfintech_NAV.objects.filter(PRODCODE__PRODCODE=i['PROD_CODE__PRODCODE']).values("NAV_DATE","NAV_VALUE").order_by('NAV_DATE').last() is not None]


#     for idx_i, i in enumerate(data):
#         record_id       = data[idx_i]["id"]
#         product_code    = data[idx_i]["PROD_CODE__PRODCODE"]
#         company_name    = data[idx_i]["PROD_CODE__COMPANY"]
#         current_nav_data        = Cams_kfintech_NAV.objects.filter(PRODCODE__PRODCODE=product_code).values("NAV_DATE","NAV_VALUE").order_by('NAV_DATE').last()
        
#         # if current_nav_data:
#         current_nav, current_nav_date = current_nav_data["NAV_VALUE"], current_nav_data["NAV_DATE"]
#          = {} = {}
#         if company_name == "cams":
#             kwargs = {}
#             # a
#         else: 
#             kwargs['TRXN_NATURE__icontains'] = "rejection"

#         trans_type = list(Cams_kfintech_transaction_details.objects.filter(FOLIO_NO=record_id).exclude(**kwargs).values("COMPANY","TRXN_NATURE", "AMOUNT","TRADDATE").order_by("TRADDATE"))
#         trans_type = [k for k in trans_type if not (k['COMPANY'] == "cams" and "insufficient balance" in k['TRXN_NATURE'].lower()) and not (
#             k['COMPANY'] != "cams" and "rejection" in k['TRXN_NATURE'].lower())]

#         transaction_type = []  # Initialize an empty list for transaction types

#         for index_j, j in enumerate(trans_type):
#             purprice = j["AMOUNT"]
#             # if i['PROD_CODE__SCHEME_NAME'] == 'NIPPON INDIA CONSUMPTION FUND - GROWTH PLAN - GROWTH OPTION':
#             #     logger.info(f"""                    
#             #         index = {index_j} purprice = {purprice} TRADDATE = {j['TRADDATE']} TRXN_NATURE = {j['TRXN_NATURE']}
#             #     """)

#             # For company "cams"
#             if company_name == "cams":
#                 if "Fresh Purchase" in j['TRXN_NATURE'] and "Purchase" not in transaction_type:
#                     transaction_type.append("Purchase")
#                 elif "NFO Purchase" in j['TRXN_NATURE'] and "Purchase" not in transaction_type:
#                     transaction_type.append("Purchase")
#                 elif "Instalment" in j['TRXN_NATURE'] and "Sip" not in transaction_type:
#                     transaction_type.append("Sip")
#                 elif "systematic 1" in j['TRXN_NATURE'].lower() and "Sip" not in transaction_type:
#                     transaction_type.append("Sip")
#                 elif "systematic-nse -" in j['TRXN_NATURE'].lower() and "Sip" not in transaction_type:
#                     transaction_type.append("Sip")
#                 elif "systematic-bse -" in j['TRXN_NATURE'].lower() and "Sip" not in transaction_type:
#                     transaction_type.append("Sip")
#                 elif "Switch-In" in j['TRXN_NATURE'] and "Switch-In" not in transaction_type:
#                     transaction_type.append("Switch-In")

#             # For other companies
#             else:
                # if "Purchase" in j['TRXN_NATURE']:
                #     # if i['PROD_CODE__SCHEME_NAME'] == 'NIPPON INDIA CONSUMPTION FUND - GROWTH PLAN - GROWTH OPTION':
                #     #     logger.info(f"""                    
                #     #         index = {index_j} purprice = {purprice} TRADDATE = {j['TRADDATE']} TRXN_NATURE = {j['TRXN_NATURE']}
                #     #     """)
                #     transacrion_nature = "Purchase"  # Default to "Purchase"
                #     if len(trans_type) > 1:
                #         if index_j > 0:  # Check previous transaction if exists
                #             prev_purprice = trans_type[index_j - 1]["AMOUNT"]
                            
                #             if prev_purprice == purprice:
                #                 transacrion_nature = "Sip"
                #         else:  # Check the next transaction if no previous one
                #             next_purprice = trans_type[index_j + 1]["AMOUNT"]
                #             if next_purprice == purprice:
                #                 transacrion_nature = "Sip"

                #     if transacrion_nature not in transaction_type:
                #         transaction_type.append(transacrion_nature)

                # elif "Investment" in j['TRXN_NATURE'] and "Sip" not in transaction_type:
                #     transaction_type.append("Sip")
                # elif "Lateral Shift In" in j['TRXN_NATURE'] and "Switch-In" not in transaction_type:
                #     transaction_type.append("Switch-In")

#         # Join and sort the transaction types
#         i["TRANSACTION_TYPE"] = " + ".join(sorted(transaction_type))

        
        
#         i["CURRENT_NAV"]        = current_nav
#         i["CURRENT_NAV_DATE"]   = current_nav_date
#         i["TOTAL_PURPRICE"]     = round(Cams_kfintech_transaction_details.objects.filter(FOLIO_NO=record_id).exclude(**kwargs).aggregate(Sum('PURPRICE'))['PURPRICE__sum'] or 0,2)
#         i["TOTAL_UNITS"]        = round(Cams_kfintech_transaction_details.objects.filter(FOLIO_NO=record_id).exclude(**kwargs).aggregate(Sum('UNITS'))['UNITS__sum'] or 0,2)
#         i["TOTAL_AMOUNT"]       = round(Cams_kfintech_transaction_details.objects.filter(FOLIO_NO=record_id).exclude(**kwargs).aggregate(Sum('AMOUNT'))['AMOUNT__sum'] or 0)

        
#         i["MARKET_VALUE"]       = round(float(current_nav)* float(i["TOTAL_UNITS"]),2)
#         i["GAIN_LOSS"]          = round(float(i["MARKET_VALUE"]) - float( i["TOTAL_AMOUNT"]),2)
#         i["PURCHASE_DATE"]      = Cams_kfintech_transaction_details.objects.filter(FOLIO_NO=record_id).aggregate(PURCHASE_DATE=Min('TRADDATE'))['PURCHASE_DATE']
#         total_purprice_sum      += i["TOTAL_PURPRICE"]
#         total_units_sum         += i["TOTAL_UNITS"]
#         total_amount_sum        += i["TOTAL_AMOUNT"]
#         total_market_value_sum  += i["MARKET_VALUE"]
#         total_gain_loss_sum     += i["GAIN_LOSS"]

#         i["ABS_RETURN"]         = round((i["GAIN_LOSS"]/float( i["TOTAL_AMOUNT"]))*100,2)

#         i["XIRR"]               = calculated_xirr(i["PURCHASE_DATE"], current_nav_date, i["TOTAL_AMOUNT"],i["MARKET_VALUE"])
#         # else:
#         #     continue
#             # data.pop(idx_i)
#     context = {
#         "data"                  : data,
#         "user_info"             : user_info,
#         "from_date"             : datetime.strptime(from_date, '%Y-%m-%d').date(),
#         "to_date"               : datetime.strptime(to_date, '%Y-%m-%d').date(),
#         "total_purprice_sum"    : round(total_purprice_sum, 2),  # Include total sum of TOTAL_PURPRICE
#         "total_units_sum"       : round(total_units_sum, 2),  # Include total sum of TOTAL_UNITS
#         "total_amount_sum"      : round(total_amount_sum, 2),  # Include total sum of TOTAL_AMOUNT
#         "total_market_value_sum": round(total_market_value_sum, 2),  # Include total sum of MARKET_VALUE
#         "total_gain_loss_sum"   : round(total_gain_loss_sum, 2),  # Include total sum of GAIN_LOSS
#         "total_abs_return"      : round((total_gain_loss_sum/float(total_amount_sum))*100,2),
#     }
#     return render(request, "admin_panel/consolidated_valuation_report_page.html",context=context)


def calculated_date_diff(nav_date,purchase_date):
    if isinstance(purchase_date, str):
        purchase_date = datetime.strptime(purchase_date, '%Y-%m-%d').date()  # Example format
    if isinstance(nav_date, str):
        nav_date = datetime.strptime(nav_date, '%Y-%m-%d').date()  # Example format

    differance_days = (nav_date - purchase_date).days
    return differance_days

# def detailized_folio_view(request):
#     folio_no        = request.GET.get("folio_no")
#     client_pan      = request.GET.get("client_pan")

#     folio_data              = Cams_kfintech_transaction.objects.get(id=folio_no)
#     current_nav_data        = Cams_kfintech_NAV.objects.filter(PRODCODE__PRODCODE = folio_data.PROD_CODE.PRODCODE).values("NAV_DATE","NAV_VALUE").order_by('NAV_DATE').last()
#     current_nav, current_nav_date = current_nav_data["NAV_VALUE"], current_nav_data["NAV_DATE"]

#     data                    = list(Cams_kfintech_transaction_details.objects.filter(FOLIO_NO__id=folio_no,FOLIO_NO__INV_NAME__PAN_NO=client_pan).values().order_by("TRADDATE"))
#     total_investing_amt_sum = total_market_value_sum = total_units_sum = 0

#     for index, i in enumerate(data):
#         company_name    = i['COMPANY']

#         if company_name == "cams":
            
#             if "insufficient balance" in i['TRXN_NATURE'].lower():
#                 data.pop(index)
#                 if i['TRADDATE'] == data[index - 1]["TRADDATE"]:
#                     data.pop(index-1)
#                 else:
#                     data.pop(index+1)
#         else:       
#             if "rejection" in i['TRXN_NATURE'].lower():
#                 data.pop(index)

#     for index, i in enumerate(data):
#         company_name    = i['COMPANY']
#         purprice        = i["AMOUNT"]
#         amount                  = float(i["AMOUNT"])
#         units                   = float(i["UNITS"])
#         i["MARKET_VALUE"]       = round(float(current_nav)* units,2)
        
#         i["ABS_RETURN"]         = round(((i["MARKET_VALUE"]- amount)/amount)*100,2)
#         i["XIRR"]               = calculated_xirr(i["TRADDATE"], current_nav_date, amount,i["MARKET_VALUE"])
#         i["TRANS_DAYS"]         = calculated_date_diff(current_nav_date,i["TRADDATE"])
#         total_investing_amt_sum += amount
#         total_units_sum         += units
#         total_market_value_sum  += i["MARKET_VALUE"]
        
#         if company_name == "cams":
#             if "Fresh Purchase" in i['TRXN_NATURE']:
#                     i['NEW_TRXN_NATURE']    = "Purchase"
#             elif "Purchase" in i['TRXN_NATURE'] or "Additional Purchase" in i['TRXN_NATURE']:
#                 if len(data) > 1:
#                     if index > 0:
#                         prev_purprice = data[index - 1]["AMOUNT"]
#                         if prev_purprice == purprice:
#                             transacrion_nature = "SIP"
#                         else:
#                             transacrion_nature = i['TRXN_NATURE']
#                     else:                
#                         next_purprice = data[index + 1]["AMOUNT"]
#                         if next_purprice == purprice:
#                             transacrion_nature = "SIP"
#                         else:
#                             transacrion_nature = i['TRXN_NATURE']
#                 else:
#                     transacrion_nature = "Purchase"
#                 i['NEW_TRXN_NATURE']    = transacrion_nature
#             elif "Instalment" in i['TRXN_NATURE']:
#                 i['NEW_TRXN_NATURE']    = "SIP"
#             elif "systematic-bse -" in i['TRXN_NATURE'].lower():
#                 i['NEW_TRXN_NATURE']    = "SIP"
  
#             elif "Switch-In" in i['TRXN_NATURE']:
#                 i['NEW_TRXN_NATURE']    = "Switch-In"
#         else:
#             if "purchase" in i['TRXN_NATURE'].lower() or "additional purchase" in i['TRXN_NATURE'].lower():
#                 if len(data) > 1:
#                     if index > 0:
#                         prev_purprice = data[index - 1]["AMOUNT"]
#                         if prev_purprice == purprice:
#                             transacrion_nature = "SIP"
#                         else:
#                             transacrion_nature = i['TRXN_NATURE']
#                     else:
#                         next_purprice = data[index + 1]["AMOUNT"]
#                         # logger.info(f"next_purprice {type(next_purprice)} {next_purprice} purprice = {type(purprice)} {purprice}")
#                         if next_purprice == purprice:
#                             transacrion_nature = "SIP"
#                         else:
#                             transacrion_nature = i['TRXN_NATURE']
#                 else:
#                     transacrion_nature = "Purchase"
#                 # if f"{transacrion_nature}" not in  transaction_type:
#                 i['NEW_TRXN_NATURE']    = transacrion_nature

#             elif "Investment" in i['TRXN_NATURE']:
#                 # if "Sip" not in  transaction_type:
#                     i['NEW_TRXN_NATURE']    = "SIP"
#             elif "Lateral Shift In" in i['TRXN_NATURE']:
#                 # if "Switch-In" not in  transaction_type:
#                     i['NEW_TRXN_NATURE']    = "Switch-In"
    
#     context = {
#         "data"                      : data ,
#         "folio_data"                : folio_data,
#         "current_nav"               : current_nav,
#         "current_nav_date"          : current_nav_date,
#         "total_investing_amt_sum"   : round(total_investing_amt_sum,2),
#         "total_units_sum"           : round(total_units_sum,2),
#         "total_market_value_sum"    : round(total_market_value_sum,2),
#         "avg_abs_return"            : round(((total_market_value_sum - total_investing_amt_sum)/total_investing_amt_sum)*100,2)
#                             #  .values("id","PROD_CODE__PRODCODE","PROD_CODE__SCHEME_NAME","INV_NAME__PAN_NO","INV_NAME__CUST_NAME","FOLIO_NO","PROD_CODE__COMPANY").order_by("PROD_CODE__SCHEME_NAME"))
#     }
    
#     return render(request, "admin_panel/detailized_folio_view.html",context=context)
def detailized_folio_view(request):
    folio_no    = request.GET.get("folio_no")
    client_pan  = request.GET.get("client_pan")
    device_type  = request.GET.get("device_type")
    logger.info(f"""
        folio_no = {folio_no}
        client_pan ={client_pan}
        device_type = {device_type}
    """)
    # folio_data = Cams_kfintech_transaction.objects.get(id=folio_no)
    folio_data = Cams_kfintech_transactionSerializer(Cams_kfintech_transaction.objects.get(id=folio_no),many=False).data
    logger.info(f'prodcode = {folio_data["PROD_CODE"]["PRODCODE"]}')
    current_nav_data = Cams_kfintech_NAV.objects.filter(PRODCODE__PRODCODE=folio_data["PROD_CODE"]["PRODCODE"]).values("NAV_DATE", "NAV_VALUE").order_by('NAV_DATE').last()
    current_nav, current_nav_date = current_nav_data["NAV_VALUE"], current_nav_data["NAV_DATE"]

    data = list(Cams_kfintech_transaction_details.objects.filter(FOLIO_NO__id=folio_no, FOLIO_NO__INV_NAME__PAN_NO=client_pan).values().order_by("TRADDATE"))
    
    total_investing_amt_sum = total_market_value_sum = total_units_sum = total_dividend_paid_sum = 0

    data = [i for i in data if not (i['COMPANY'] == "cams" and "insufficient balance" in i['TRXN_NATURE'].lower()) and not (i['COMPANY'] != "cams" and "rejection" in i['TRXN_NATURE'].lower())]
    # Store valid transactions
    valid_transactions = []

    for index, i in enumerate(data):
        if "Switchout" in i['TRXN_NATURE']:
            valid_transactions.clear()
            total_investing_amt_sum = total_market_value_sum = total_units_sum = total_dividend_paid_sum = 0
        else:
            amount, units = float(i["AMOUNT"]), float(i["UNITS"])
            i["MARKET_VALUE"]   = round(float(current_nav) * units, 2)
            i["ABS_RETURN"]     =  0 if i['TRXN_NATURE'] == "Dividend Paid" and i['COMPANY'] == "cams" else round(((i["MARKET_VALUE"] - amount) / amount) * 100, 2)
            i["XIRR"]           = 0 if i['TRXN_NATURE'] == "Dividend Paid" and i['COMPANY'] == "cams" else calculated_xirr(i["TRADDATE"], current_nav_date, amount, i["MARKET_VALUE"])
            i["TRANS_DAYS"]     = calculated_date_diff(current_nav_date, i["TRADDATE"])

            total_units_sum         += units
            total_market_value_sum  += i["MARKET_VALUE"]
            if i['TRXN_NATURE'] == "Dividend Paid" and i['COMPANY'] == "cams":
                total_investing_amt_sum += 0
                total_dividend_paid_sum += amount
                i["TOTAL"]              = amount
            else:
                total_investing_amt_sum += amount
                total_dividend_paid_sum += 0
                i["TOTAL"]              = i["MARKET_VALUE"]

            total_sum  = total_market_value_sum + total_dividend_paid_sum
            if "purchase" in i['TRXN_NATURE'].lower() or "additional purchase" in i['TRXN_NATURE'].lower():
                transacrion_nature = "SIP" if len(data) > 1 and (
                    (index > 0 and data[index - 1]["AMOUNT"] == i["AMOUNT"]) or 
                    (index < len(data) - 1 and data[index + 1]["AMOUNT"] == i["AMOUNT"])) else "Purchase"
                i['NEW_TRXN_NATURE'] = transacrion_nature
            elif "systematic 1" in i['TRXN_NATURE'].lower() or "systematic-nse" in i['TRXN_NATURE'].lower() or "systematic-bse" in i['TRXN_NATURE'].lower() or "Instalment" in i['TRXN_NATURE'] or "Investment" in i['TRXN_NATURE']:
                i['NEW_TRXN_NATURE'] = "SIP"
            elif "Switch-In" in i['TRXN_NATURE'] or "Lateral Shift In" in i['TRXN_NATURE']:
                i['NEW_TRXN_NATURE'] = "Switch-In"
            valid_transactions.append(i)

    context = {
        "data"                      : valid_transactions,
        "folio_data"                : folio_data,
        "current_nav"               : current_nav,
        "current_nav_date"          : current_nav_date,
        "total_investing_amt_sum"   : round(total_investing_amt_sum, 2),
        "total_units_sum"           : round(total_units_sum, 2),
        "total_dividend_paid_sum"   : round(total_dividend_paid_sum, 2),
        "total_market_value_sum"    : round(total_market_value_sum, 2),
        "total_sum"                 : round(total_sum, 2),
        "avg_abs_return"            : round(((total_market_value_sum - total_investing_amt_sum) / total_investing_amt_sum) * 100, 2)
        if total_investing_amt_sum != 0 else 0
    }
    if device_type == "mobile":
        return JsonResponse(context,safe=False,status=200)
    else:
        return render(request, "admin_panel/detailized_folio_view.html", context=context)


# def test_rushikesh(request):
#     try:
#         data = [
#             {
#                 'id': 5,
#                 'PROD_CODE__PRODCODE': 'D167',
#                 'PROD_CODE__SCHEME_NAME': 'DSP Flexi Cap Fund - Regular Plan - Growth',
#                 'INV_NAME__PAN_NO': 'ASZPP6345G',
#                 'INV_NAME__CUST_NAME': 'Baban Gautam Patil  ',
#                 'FOLIO_NO': '6575773/56',
#                 'PROD_CODE__COMPANY': 'cams'
#             },
#             {
#                 'id': 456,
#                 'PROD_CODE__PRODCODE': 'OFEG',
#                 'PROD_CODE__SCHEME_NAME': 'HSBC Focused Fund - Regular Growth (Formerly known as HSBC Focused Equity Fund Growth)',
#                 'INV_NAME__PAN_NO': 'ASZPP6345G',
#                 'INV_NAME__CUST_NAME': 'Baban Gautam Patil  ',
#                 'FOLIO_NO': '5710147/50',
#                 'PROD_CODE__COMPANY': 'cams'
#             },
#             {
#                 'id': 433,
#                 'PROD_CODE__PRODCODE': 'OLFOCG',
#                 'PROD_CODE__SCHEME_NAME': 'L&T Focused Equity Fund - Growth',
#                 'INV_NAME__PAN_NO': 'ASZPP6345G',
#                 'INV_NAME__CUST_NAME': 'Baban Gautam Patil  ',
#                 'FOLIO_NO': '5710147/50',
#                 'PROD_CODE__COMPANY': 'cams'
#             },
#             {
#                 'id': 266,
#                 'PROD_CODE__PRODCODE': 'MMMRBRG',
#                 'PROD_CODE__SCHEME_NAME': 'Mahindra Manulife Consumption Fund - Regular - Growth',
#                 'INV_NAME__PAN_NO': 'ASZPP6345G',
#                 'INV_NAME__CUST_NAME': 'Baban Gautam Patil  ',
#                 'FOLIO_NO': '1001138837',
#                 'PROD_CODE__COMPANY': 'cams'
#             }
#             ]
        
#         for idx, i in enumerate(data):

#             record_id       = data[idx]["id"]
#             product_code    = data[idx]["PROD_CODE__PRODCODE"]
#             i["CURRENT_NAV"]        = Cams_kfintech_NAV.objects.filter(PRODCODE__PRODCODE =product_code).order_by('NAV_DATE').values("NAV_VALUE").last()["NAV_VALUE"]
#             i["CURRENT_NAV_DATE"]   = Cams_kfintech_NAV.objects.filter(PRODCODE__PRODCODE =product_code).order_by('NAV_DATE').values("NAV_DATE").last()["NAV_DATE"]

#             logger.info(f"""
#                 product_code    = {product_code}
#                 i["CURRENT_NAV"] = {i["CURRENT_NAV"]}
#                 i["CURRENT_NAV_DATE"] = {i["CURRENT_NAV_DATE"]}
#             """)

#         return JsonResponse(data,safe=False,status=200)
#     except Exception as e:
#         logger.exception(e)
#         return JsonResponse("something went wrong", safe=False, status=500)
    
def test_query(request):
    try:
        product_code = "OLFOCG"
        # data = Cams_kfintech_NAV.objects.filter(PRODCODE__PRODCODE =product_code).order_by('NAV_DATE').values("NAV_VALUE").last()["NAV_VALUE"]
        data = list(Cams_kfintech_NAV.objects.filter(PRODCODE__PRODCODE =product_code).values("NAV_VALUE"))
        
        return JsonResponse(data,safe=False,status=200)
    except Exception as e:
        logger.exception(e)
        return JsonResponse("something went wrong", safe=False, status=500)
    

@api_view(["POST"])
def get_user_mobile_no(request,id):
    try:

        data = Registration_personal_details.objects.get(id=id)

        data = {
            "user_name"   : data.NAME,
            "mobile_no"   : data.MOBILE
            }
        # EMPLOYEE_CODE
        return JsonResponse(data,safe=False,status=200)
    except Exception as e:
        logger.exception(f"{e}")
        return JsonResponse(f"{e}",safe=False,status=500)

@api_view(["POST"])
def edit_user_mobile_no(request,id):
    try:
        # ep_name = request.POST.get("ep_name")
        mobile_no = request.POST.get("mobile_no")
        if Registration_personal_details.objects.filter(MOBILE = mobile_no).exclude(id=id).exists():
            return JsonResponse("This Mobile Number Already Exist",safe=False,status=412)
        else:
            data = Registration_personal_details.objects.get(id=id)
            data.MOBILE = mobile_no
            data.save()

            return JsonResponse("Mobile Number Change Successfully",safe=False,status=200)
    except Exception as e:
        logger.exception(f"{e}")
        return JsonResponse(f"{e}",safe=False,status=500)
    

@api_view(["GET"])
def make_payment(request):
    try:
        api_key = "JTAXgH"                          # Replace with your key
        salt = "7bwqA1gOpfRw6B332nOjkWURoVfwYafn"   # Replace with your salt
        # Transaction details
        txn_id = "1234"             # Ensure this is unique for every payment
        amount = "1.00"           # Amount to charge
        product_info = "Test Product"
        first_name = "John"
        email = "john@example.com"
        phone = "9999999999"
        surl = "https://investology.dvadminpanel.in/payment_response" # Success URL
        furl = "https://investology.dvadminpanel.in/payment_response" # Failure URL
        udf1    = "testingId"

        hash_string = f"{api_key}|{txn_id}|{amount}|{product_info}|{first_name}|{email}|{udf1}||||||||||{salt}"
        hash = hashlib.sha512(hash_string.encode('utf-8')).hexdigest()

        logger.info(f"hash = {hash}")
        # PayU payment form
        payu_url = "https://test.payu.in/_payment"
        payload = {
            "key": api_key,
            "txnid": txn_id,
            "amount": amount,
            "productinfo": product_info,
            "firstname": first_name,
            "email": email,
            "phone": phone,
            "surl": surl,
            "furl": furl,
            "udf1": udf1,
            "hash": hash
        }
        # Create auto-submitting form for redirection
        html = f"""
        <html>
        <body onload="document.forms['payu_form'].submit();">
            <form name="payu_form" method="POST" action="{payu_url}">
                {''.join([f'<input type="hidden" name="{k}" value="{v}"/>' for k, v in payload.items()])}
            </form>
        </body>
        </html>
        """
        return HttpResponse(html)
    except Exception as e:
        logger.exception(f"{e}")
        return JsonResponse(f"{e}",safe=False,status=500)

# @api_view(["POST"])
# def payment_response(request):
#     try:
#         # Extract PayU response data
#         response_data = request.POST.dict()

#         # Verify hash to ensure data integrity
#         salt = "7bwqA1gOpfRw6B332nOjkWURoVfwYafn"
#         hash_sequence = f"{salt}|{response_data.get('status')}|{'|'.join([response_data.get(k, '') for k in reversed(['udf5', 'udf4', 'udf3', 'udf2', 'udf1', 'email', 'firstname', 'productinfo', 'amount', 'txnid', 'key'])])}"
#         generated_hash = hashlib.sha512(hash_sequence.encode("utf-8")).hexdigest()
        
#         logger.info(f"response_data = {response_data}")
#         logger.info(f"generated_hash = {generated_hash}")
#         if generated_hash != response_data.get("hash"):
#             return JsonResponse({"error": "Invalid hash"}, safe=False, status=400)

#         if response_data.get("status") == "success":
#             # Handle successful payment
#             return JsonResponse({"message": "Payment successful", "data": response_data}, safe=False, status=200)
#         else:
#             # Handle failed payment
#             return JsonResponse({"message": "Payment failed", "data": response_data}, safe=False, status=400)

#     except Exception as e:
#         return JsonResponse({"error": str(e)}, safe=False, status=500)

@api_view(["POST"])
def payment_response(request):
    try:
        # Extract PayU response data
        response_data = request.POST.dict()

        # PayU Merchant Salt
        salt = "7bwqA1gOpfRw6B332nOjkWURoVfwYafn"

        # Generate hash sequence
        # hash_sequence = f"{response_data['key']}|{response_data['txnid']}|{response_data['amount']}|{response_data['productinfo']}|{response_data['firstname']}|{response_data['email']}|{response_data.get('udf1', '')}|{response_data.get('udf2', '')}|{response_data.get('udf3', '')}|{response_data.get('udf4', '')}|{response_data.get('udf5', '')}|{response_data.get('udf6', '')}|{response_data.get('udf7', '')}|{response_data.get('udf8', '')}|{response_data.get('udf9', '')}|{response_data.get('udf10', '')}|{salt}|{response_data['status']}"
        hash_sequence = f"{salt}|{response_data['status']}|{response_data.get('udf10', '')}|{response_data.get('udf9', '')}|{response_data.get('udf8', '')}|{response_data.get('udf7', '')}|{response_data.get('udf6', '')}|{response_data.get('udf5', '')}|{response_data.get('udf4', '')}|{response_data.get('udf3', '')}|{response_data.get('udf2', '')}|{response_data.get('udf1', '')}|{response_data['email']}|{response_data['firstname']}|{response_data['productinfo']}|{response_data['amount']}|{response_data['txnid']}|{response_data['key']}"
        generated_hash = hashlib.sha512(hash_sequence.encode("utf-8")).hexdigest()

        # Log for debugging
        logger.info(f"Response Data: {response_data}")
        logger.info(f"Generated Hash: {generated_hash}")
        logger.info(f"PayU Hash: {response_data.get('hash')}")

        # Validate hash
        if generated_hash != response_data.get("hash"):
            return JsonResponse({"error": "Invalid hash"}, safe=False, status=400)

        # Process payment status
        if response_data.get("status") == "success":
            return JsonResponse({"message": "Payment successful", "data": response_data}, safe=False, status=200)
        else:
            return JsonResponse({"message": "Payment failed", "data": response_data}, safe=False, status=400)

    except Exception as e:
        logger.exception(f"Error processing payment response: {e}")
        return JsonResponse({"error": str(e)}, safe=False, status=500)


def test_payu(request):
    return render(request,"admin_panel/test_payu.html")

# import hashlib

# def generate_hash(key, txnid, amount, productinfo, firstname, email, salt):
#     input_str = f"{key}|{txnid}|{amount}|{productinfo}|{firstname}|{email}|||||||||||{salt}"
#     return hashlib.sha512(input_str.encode('utf-8')).hexdigest()

#     # Example usage
#     key = 'yourKey'
#     txnid = 'yourTxnId'
#     amount = 'yourAmount'
#     productinfo = 'yourProductInfo'
#     firstname = 'yourFirstName'
#     email = 'yourEmail'
#     salt = 'yourSalt'

#     hash_value = generate_hash(key, txnid, amount, productinfo, firstname, email, salt)
#     print("Generated Hash:", hash_value)