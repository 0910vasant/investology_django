from django.shortcuts import render , redirect
from rest_framework.views import APIView
from rest_framework.decorators import api_view
import logging
logger = logging.getLogger()
from django.contrib import messages
from django.http import JsonResponse
from crm.models import *
from app.models import *
from .serializers import *
from django.contrib import messages #import messages
from datetime import datetime,timedelta,date
from dateutil.relativedelta import relativedelta
from django.contrib.auth.hashers import check_password
from django.utils import timezone
from django.db.models import Q
from django.db.models import Avg, Count, Min, Sum

import json

import pandas as pd
from itertools import chain
from babel.numbers import format_number

# from datetime import datetime, timedelta
# Create your views here.

def get_under_mapped(request):
    login_id = request.session['LOGIN_ID']
    user_type = request.session['USER_TYPE']
    user_type_id = request.session['USER_TYPE_ID']
    if user_type =="bm":
        mapped_bm_id_list = list(User.objects.filter(USER_TYPE="bm",BM__id=user_type_id).values_list("id",flat=True))
        mapped_rm_id_list = list(User.objects.filter(USER_TYPE="rm",RM__BRANCH__id=user_type_id).values_list("id",flat=True))
        mapped_ep_id_list = list(User.objects.filter(USER_TYPE="ep",EP__RM__id=user_type_id).values_list("id",flat=True))
        final_list = list(set(mapped_rm_id_list + mapped_ep_id_list+mapped_bm_id_list))
    elif user_type == "rm":
        mapped_ep_id_list = list(User.objects.filter(USER_TYPE="ep",EP__RM__id=user_type_id).values_list("id",flat=True))
        final_list = mapped_ep_id_list
    final_list.append(login_id)
    return final_list

def demo_login(request):
    return render(request,"auth_login.html")



def home(request):
    if request.session.get("is_authenticated"):
        if request.session['USER_TYPE'] == "bo":
            return redirect("/attendance")
        else:
            return redirect("/dashboard")
    else:
        return redirect("/login")

class Login(APIView):
    def get(self,request):
        return render(request,"demo_login.html")
    def post(self,request):
        try:
            username        = request.data.get("username")
            password        = request.data.get("password")
            device_type     = request.data.get("device_type")
            # login_time = timezone.now()+timedelta(hours = 5, minutes = 30)
            login_time = timezone.now()

            if User.objects.filter(USERNAME=username).exists():
                user = User.objects.get(USERNAME=username)
                if(check_password(password,user.PASSWORD)):
                    if device_type == "mobile":
                        ''' this condition check the use type
                            this function is only for Easy Partner
                        '''
                        if user.USER_TYPE == "ep":
                            data = list(User.objects.filter(id=user.id).values("id","USER_ID","USER_TYPE","OWNER","EMPLOYEE_CODE","NAME","USERNAME"))
                            # Branch_Manager (bm)
                            if user.USER_TYPE == "bm":
                                user_data = Branch_Manager.objects.get(id=user.USER_ID)
                            # Relationship_Manager (rm)
                            if user.USER_TYPE == "rm":
                                user_data = Relationship_Manager.objects.get(id=user.USER_ID)
                            # Easy_Partner (ep)
                            if user.USER_TYPE == "ep":
                                user_data = Easy_Partner.objects.get(id=user.USER_ID)
                            data[0]["MOB_NO"]   = user_data.MOB_NO
                            data[0]["EMAIL"]    = user_data.EMAIL
                            return JsonResponse({"message":"Login successfully","data":data},status=200)
                        else:
                            return JsonResponse({"error":"This User not allowed to use this app Please contact admin"},status=412)
                    else:
                        x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
                        if x_forwarded_for:
                            ip = x_forwarded_for.split(',')[0]
                        else:
                            ip = request.META.get('REMOTE_ADDR')
                        if request.session.session_key is None:
                            request.session.create()
                        request.session['is_authenticated'] = True
                        request.session['SESSION_ID'] = request.session.session_key
                        request.session['LOGIN_ID'] = user.id
                        # request.session['USER_CONTACT'] = user.MOB_NO
                        # messages.success(request,'Login Successfully')
                        
                        request.session['USER_USERNAME'] = user.USERNAME
                        request.session['USER_TYPE'] = user.USER_TYPE
                        request.session['USER_TYPE_ID'] = user.USER_ID
                        request.session['NAME'] = user.NAME
                        logger.info(f"user type = {user.USER_TYPE}")
                        role = User_Role_Permission.objects.get(USER_TYPE = user.USER_TYPE)
                        request.session['ALLOWED_MODULES'] = role.ALLOWED_MODULES
                        # request.session['ALLOWED_URL'] = role.ALLOWED_MODULES

                        LoginLogs.objects.create(
                            USER_ID = user.id,
                            USER_TYPE = request.session['USER_TYPE'],
                            LOGIN_DATETIME = login_time,
                            LOGIN_SESSION = request.session['SESSION_ID'],
                            IP_ADDRESS = ip,
                        )
                        messages.success(request,"Login successfully")
                        return JsonResponse({"message":"Login successfully"},status=200)
                else:
                #   messages.error(request,"Invalid credentials")
                    return JsonResponse({"error":"Invalid credentials"},status=412)
            else:
                # messages.error(request,"User Does Not Exist")
                # return redirect("/login")
                return JsonResponse({"error":"User Does Not Exist. Please Contact To Administrator"},status=412)
        except Exception as e:
            logger.exception(e)
            return JsonResponse("Something went wrong",safe=False,status=500)


def Logout(request):
    try:
        if LoginLogs.objects.filter(LOGIN_SESSION=request.session['SESSION_ID']).exists():
            login = LoginLogs.objects.filter(LOGIN_SESSION=request.session['SESSION_ID']).last()
            LoginLogs.objects.update(LOGIN_STATUS=False)
            login.LOGOUT_DATETIME = timezone.now()
            login.LOGIN_STATUS=False
            login.save()
            request.session.flush()
        else:
            request.session.flush()
        return redirect("/login")
    except Exception as e:
        request.session.flush()
        logger.exception(e)
        print(e)
        return redirect("/login")



def employee_code_generation(user_type):
    # user = User.objects.get(id=id)
    e_number = 1
    if user_type == "ep":
        e_code = "EP"
        if User.objects.filter(USER_TYPE="ep").exclude(Q(EMPLOYEE_CODE="") | Q(EMPLOYEE_CODE=None)).exists():
            e_number = User.objects.filter(USER_TYPE="ep").exclude(Q(EMPLOYEE_CODE="") | Q(EMPLOYEE_CODE=None)).last().EMPLOYEE_NUMBER
            e_number = str(int(e_number) + 1).zfill(4)
        # else:
        #     e_number = "1"
        # e_code = e_code + str(e_number).zfill(4)
    # if user_type == "bm":
    #     e_code = "EE"
    #     if User.objects.filter(USER_TYPE="bm").exclude(Q(EMPLOYEE_CODE="") | Q(EMPLOYEE_CODE=None)):
    #         e_number = User.objects.filter(USER_TYPE="bm").exclude(Q(EMPLOYEE_CODE="") | Q(EMPLOYEE_CODE=None)).last().EMPLOYEE_NUMBER
    #         logger.info(f"e_number = {e_number}")
    #         e_number = str(int(e_number) + 1).zfill(4)
    #     else:
    #         e_number = "11"
    if user_type == "bm" or user_type == "rm" or user_type == "bo":
        e_code = "EE"
        if User.objects.filter(USER_TYPE__in=["bm","rm","bo"]).exclude(Q(EMPLOYEE_CODE="") | Q(EMPLOYEE_CODE=None)).exists():
            e_number = User.objects.filter(USER_TYPE__in=["bm","rm","bo"]).exclude(Q(EMPLOYEE_CODE="") | Q(EMPLOYEE_CODE=None)).last().EMPLOYEE_NUMBER
            logger.info(f"e_number = {e_number}")
            e_number = str(int(e_number) + 1).zfill(4)
        # else:
        #     e_number = "1"
    e_code = e_code + str(e_number).zfill(4)
    # if user_type == "rm" or user_type == "bo":
    #     e_code = "EE"
    #     if User.objects.filter(USER_TYPE__in=["rm","bo"]).exclude(Q(EMPLOYEE_CODE="") | Q(EMPLOYEE_CODE=None)).exists():
    #         e_number = User.objects.filter(USER_TYPE__in=["rm","bo"]).exclude(Q(EMPLOYEE_CODE="") | Q(EMPLOYEE_CODE=None)).last().EMPLOYEE_NUMBER
    #         logger.info(f"e_number = {e_number}")
    #         e_number = str(int(e_number) + 1).zfill(4)
    #     else:
    #         e_number = "11"
    # e_code = e_code + str(e_number).zfill(4)
    return e_code,e_number

class Create_user_login(APIView):
    def post(self,request):
        try:
            login_id   = request.session['LOGIN_ID']
            user_id   = request.POST.get("user_id")
            user_type = request.POST.get("user_type")
            # name     = request.POST.get("name")
            username = request.POST.get("username")
            password = request.POST.get("password")
            
            e_code,e_number = employee_code_generation(user_type)
            logger.info(f"""
                user_id = {user_id}
                user_type = {user_type}
                username = {username}
                password = {password}
                e_code = {e_code}
                e_number = {e_number}
                """)
            # name = {name}
            if User.objects.filter(USERNAME = username).exists():
                return JsonResponse({"error":"Username Already Exist Please create new user"},status=412)
            else:
                user_obj = User.objects.get(id=login_id)
                add = User.objects.create(
                    USER_ID = user_id,
                    USERNAME = username,
                    PASSWORD = password ,
                    CREATED_BY = user_obj,
                    EMPLOYEE_CODE =  e_code,
                    EMPLOYEE_NUMBER = e_number,
                )
                if user_type == "bm":
                    bm_obj = Branch_Manager.objects.get(id = user_id)
                    bm_obj.LOGIN = add
                    bm_obj.CREATE_LOGIN = True
                    bm_obj.MODIFIED_BY = user_obj
                    bm_obj.save()

                    if bm_obj.OWNER is True:
                        add.OWNER = True
                    add.USER_TYPE = user_type
                    add.NAME = bm_obj.NAME
                    add.BM = bm_obj

                if user_type == "rm":
                    rm_obj = Relationship_Manager.objects.get(id = user_id)
                    rm_obj.LOGIN = add
                    rm_obj.CREATE_LOGIN = True
                    rm_obj.MODIFIED_BY = user_obj
                    rm_obj.save()

                    add.RM = rm_obj
                    add.USER_TYPE = user_type
                    add.NAME = rm_obj.NAME

                if user_type == "ep":
                    ep_obj = Easy_Partner.objects.get(id = user_id)
                    ep_obj.LOGIN = add
                    ep_obj.CREATE_LOGIN = True
                    ep_obj.MODIFIED_BY = user_obj
                    ep_obj.save()
                    
                    add.EP = ep_obj
                    add.USER_TYPE = user_type
                    add.NAME = ep_obj.NAME
                    
                    
                if user_type == "bo":
                    bo_obj = Back_Office.objects.get(id = user_id)
                    bo_obj.LOGIN = add
                    bo_obj.CREATE_LOGIN = True
                    bo_obj.MODIFIED_BY = user_obj
                    bo_obj.save()

                    add.BO = bo_obj
                    add.USER_TYPE = user_type
                    add.NAME = bo_obj.NAME
                    
                add.save()
                messages.success(request,"Login Create successfully")
                return JsonResponse({"message":"Login Create successfully"},status=200)
            # return JsonResponse({"message":"Login Create successfully"},status=200)
        except Exception as e:
            messages.error(request,"Something went wrong")
            logger.exception(f"{e}")
            return JsonResponse({"error":f"{e}"},safe=False,status=500)
        
# def login_page(request):
#     return render(request,"auth_login.html")
class Change_password(APIView):
    def post(self,request):
        try:
            login_id   = request.session['LOGIN_ID']
            # id = request.session['LOGIN_ID']
            # logger.info(f"user id = {id}")
            old_password = request.POST.get("old_pass")
            new_password = request.POST.get("new_pass")

            user = User.objects.get(id=login_id)
            if(check_password(old_password,user.PASSWORD)):
                user.MODIFIED_BY = user
                user.PASSWORD = new_password
                user.MODIFIED_BY = User.objects.get(id=request.session['LOGIN_ID'])
                user.save()
                messages.success(request,"Password Change successfully")
                return JsonResponse({"message":"Password Change successfully"},status=200)
            else:
                return JsonResponse({"error":"Old Password cannot be matched"},status=412)
        except Exception as e:
            messages.error(request,"Something went wrong")
            logger.exception(f"{e}")
            return JsonResponse({"error":f"{e}"},safe=False,status=500)
        
class Forgot_password(APIView):
    def post(self,request):
        try:
            
            login_id   = request.session['LOGIN_ID']
            user_id = request.POST.get("user_id")
            user_type = request.POST.get("user_type")
            conf_pass = request.POST.get("conf_pass")

            # logger.info(f"""
            #     login_id = {login_id}
            #     user_id = {user_id}
            #     user_type = {user_type}
            # """)
            if user_type == "admin":
                user = User.objects.get(id=user_id)
            else:
                user = User.objects.get(USER_ID=user_id,USER_TYPE=user_type)
            user.PASSWORD = conf_pass
            user.MODIFIED_BY = User.objects.get(id=login_id)
            user.save()
            # messages.success(request,"Password Change successfully")
            return JsonResponse({"message":"Password Change successfully"},status=200)
        except Exception as e:
            messages.error(request,"Something went wrong")
            logger.exception(f"{e}")
            return JsonResponse({"error":f"{e}"},safe=False,status=500)

def profile(request):
    id           = request.session['LOGIN_ID']
    user_type    = request.session['USER_TYPE']
    user_type_id = request.session['USER_TYPE_ID']
    logger.info(f"""
        id = {id}
        user_type = {user_type}
        user_type_id = {user_type_id}
    """)
    # data = User.objects.get(id=id)
    if user_type == "bm":
        data = Branch_Manager.objects.get(id=user_type_id)
    if user_type == "rm":
        data = Relationship_Manager.objects.get(id=user_type_id)
    if user_type == "ep":
        data = Easy_Partner.objects.get(id=user_type_id)
    if user_type == "bo":
        data = Back_Office.objects.get(id=user_type_id)
    if user_type == "admin" or user_type == "superadmin":
        data = User.objects.get(id=id)
    
        #  = USER_ID data
        # USER_TYPE =
    return render(request,"profile.html",context={"data":data})

def load_customer_count(request):
    user_type = request.session['USER_TYPE']
    if user_type == "bm" or user_type == "rm":
        final_list = get_under_mapped(request)
        # logger.info(f"final list = {final_list}")
        data = list(Customer.objects.filter(RM_EP__in=final_list).exclude(IS_DELETED=True).values("id").order_by("-id"))
    else:
    # if user_type == "admin" or user_type == "superadmin":
        data = list(Customer.objects.values("id").exclude(IS_DELETED=True).order_by("-id"))
    return len(data)

class Index(APIView):
    def get(self,request):
        today = date.today()
        date_after_30_days = today + relativedelta(days = 30)
        logger.info(f"{today.month,today.day,date_after_30_days}")
        
        cust_count = load_customer_count(request)
        data = {
            "cust_count":cust_count
        }

        data["greetings"] = {
            "bday" : Customer.objects.filter(CUST_DOB__month = today.month, CUST_DOB__day = today.day).exclude(IS_DELETED=True),
            "anniversary" : []
        }
        # data["renewal"] = Insurance.objects.filter(RENEWAL_DATE__gte = today, RENEWAL_DATE__lte = date_after_30_days)
        # logger.info(f"data = {data}")
        return render(request,"index.html",context={"data":data})


class Scheme_Master(APIView):
    def get(self,request):
        return render(request,"scheme_master.html")

class Client_Family(APIView):
    def get(self,request):
        return render(request,"client_family.html")

class Add_Client_Family(APIView):
    def get(self,request):
        return render(request,"add_client_family.html")


class Super_Partner(APIView):
    def get(self,request):
        return render(request,"super_partner.html")

class Add_Super_Partner(APIView):
    def get(self,request):
        return render(request,"add_super_partner.html")

class SP_Brokerage(APIView):
    def get(self,request):
        return render(request,"sp_brokerage.html")

class Add_SP_Brokerage(APIView):
    def get(self,request):
        return render(request,"add_sp_brokerage.html")

class BSE_SM_User(APIView):
    def get(self,request):
        return render(request,"bse_sm_user.html")

class Add_BSE_SM_User(APIView):
    def get(self,request):
        return render(request,"add_bse_sm_user.html")

class MF_Manually(APIView):
    def get(self,request):
        return render(request,"mf_manually.html")

class Add_MF_Manually(APIView):
    def get(self,request):
        return render(request,"add_mf_manually.html")

class NAV_View(APIView):
    def get(self,request):
        return render(request,"nav_view.html")

class Add_NAV_View(APIView):
    def get(self,request):
        return render(request,"add_nav_view.html")

class Edit_NAV_View(APIView):
    def get(self,request):
        return render(request,"edit_nav_view.html")

class Transaction_View(APIView):
    def get(self,request):
        return render(request,"transaction_view.html")

class Add_Transaction_View(APIView):
    def get(self,request):
        return render(request,"add_transaction_view.html")

class Edit_Transaction_View(APIView):
    def get(self,request):
        return render(request,"edit_transaction_view.html")

class MF_Valuation_Report(APIView):
    def get(self,request):
        return render(request,"mf_valuation_report.html")

class ACC_Statement_Report(APIView):
    def get(self,request):
        return render(request,"account_statement_report.html")

class Portfolio_Composition(APIView):
    def get(self,request):
        return render(request,"portfolio_composition.html")

class Capital_Gain_Report(APIView):
    def get(self,request):
        return render(request,"capital_gain_report.html")
    
class Capital_Gain_Report_Page(APIView):
    def get(self,request):
        return render(request,"capital_gain_report_page.html")

class Dividend_Income_Statement(APIView):
    def get(self,request):
        return render(request,"dividend_income_statement.html")

class Transaction_Report(APIView):
    def get(self,request):
        return render(request,"transaction_report.html")

class SIP_Report(APIView):
    def get(self,request):
        return render(request,"sip_report.html")

class Top_N_Client(APIView):
    def get(self,request):
        return render(request,"top_n_client.html")

class Scheme_Comparison(APIView):
    def get(self,request):
        return render(request,"scheme_comparison.html")

class Scheme_Comparison_Page(APIView):
    def get(self,request):
        return render(request,"scheme_comparison_page.html")

class Scheme_Factsheet(APIView):
    def get(self,request):
        return render(request,"scheme_factsheet.html")

class Scheme_Factsheet_Page(APIView):
    def get(self,request):
        return render(request,"scheme_factsheet_page.html")

class ARN_Brokerage_Report(APIView):
    def get(self,request):
        return render(request,"arn_brokerage_report.html")

class ARN_Brokerage_Report_Page(APIView):
    def get(self,request):
        return render(request,"arn_brokerage_report_page.html")

class ARN_Clientwise_Brokerage_Report(APIView):
    def get(self,request):
        return render(request,"arn_clientwise_brokerage_report.html")

class ARN_Clientwise_Brokerage_Report_Page(APIView):
    def get(self,request):
        return render(request,"arn_clientwise_brokerage_report_page.html")

class ARN_AUM_Report(APIView):
    def get(self,request):
        return render(request,"arn_aum_report.html")

class ARN_AUM_Typewise_Report_Page(APIView):
    def get(self,request):
        return render(request,"arn_aum_typewise_report_page.html")

class ARN_AUM_Schemewise_Report_Page(APIView):
    def get(self,request):
        return render(request,"arn_aum_schmewise_report_page.html")

class ARN_AUM_Clientwise_Report_Page(APIView):
    def get(self,request):
        return render(request,"arm_aum_clientwise_report_page.html")

@api_view(["GET"])
def add_mf_customer(request):
    return render(request,"add_mf_customer.html")

def branch_location_master_page(request):
    return render(request,"branch_location_master.html")

class add_branch_location(APIView):
    def post(self,request):
        try:
            login_id   = request.session['LOGIN_ID']
            location_name = request.POST.get("location_name")
            logger.info(f"""
                location_name = {location_name}
            """)
            if Branch_location_master.objects.filter(NAME=location_name).exists():
                return JsonResponse({"error":"This Location Already Exist"},status=412)
            else:
                add = Branch_location_master.objects.create(
                    NAME = location_name,
                    CREATED_BY = User.objects.get(id=login_id)
                )
            # messages.success(request,"Sub Broker Brokerage Add successfully")
            # return redirect("/easy_partner_brokerage")
                return JsonResponse({"message":"Branch Location Add successfully"},status=200)
        except Exception as e:
            # messages.error(request,"Something went wrong")
            logger.exception(f"{e}")
            # return redirect("/add_easy_partner_brokerage")
            return JsonResponse({"error":"something went wong"},status=200)

class edit_branch_location(APIView):
    def get(self,request,id):
        data = list(Branch_location_master.objects.filter(id=id).values("NAME"))
        return JsonResponse(data,safe=False)
    def post(self,request,id):
        try:
            login_id   = request.session['LOGIN_ID']
            location_name = request.POST.get("location_name")
            logger.info(f"""
                location_name = {location_name}
            """)
            if Branch_location_master.objects.filter(NAME=location_name).exclude(id=id).exists():
                return JsonResponse({"error":"This Location Already Exist"},status=412)
            else:
                edit = Branch_location_master.objects.get(id=id)
                edit.NAME = location_name
                edit.MODIFIED_BY = User.objects.get(id=login_id)
                edit.save()
            # messages.success(request,"Sub Broker Brokerage Add successfully")
            # return redirect("/easy_partner_brokerage")
                return JsonResponse({"message":"Branch Location Edited successfully"},status=200)
        except Exception as e:
            # messages.error(request,"Something went wrong")
            logger.exception(f"{e}")
            # return redirect("/add_easy_partner_brokerage")
            return JsonResponse({"error":"something went wong"},status=200)

def load_branch_location(request):
    data = list(Branch_location_master.objects.values("id","NAME").order_by('-id'))
    return JsonResponse({"data":data},safe=False)

class Branch_Manager_Page(APIView):
    def get(self,request):
        return render(request,"branch_manager.html")

def load_bm_data(request):
    data = list(Branch_Manager.objects.values("LOGIN__EMPLOYEE_CODE","LOGIN__USERNAME","id","PAN_NO","CODE","NAME","DOB","PHONE","MOB_NO","EMAIL","CREATE_LOGIN").order_by("-id"))
    return JsonResponse({"data":data},safe=False)

class Add_Branch_Manager(APIView):
    def get(self,request):
        bml = Branch_location_master.objects.values('id',"NAME")
        return render(request,"add_branch_manager.html",context={"bml":bml})
    def post(self,request):
        try:
            login_id   = request.session['LOGIN_ID']
            # bm_code = request.POST.get("bm_code")
            bm_name = request.POST.get("bm_name")
            bm_address_1 = request.POST.get("bm_address_1")
            bm_address_2 = request.POST.get("bm_address_2")
            bm_dob = request.POST.get("bm_dob")
            bm_phone_no = request.POST.get("bm_phone_no")
            bm_mob_no = request.POST.get("bm_mob_no")
            bm_email = request.POST.get("bm_email")
            branch_loc = request.POST.get("branch_loc")
            bank_name = request.POST.get("bank_name")
            acc_no = request.POST.get("acc_no")
            ifsc_code = request.POST.get("ifsc_code")
            pan_no = request.POST.get("pan_no")
            aadhaar_no = request.POST.get("aadhaar_no")
            logger.info(f"""
                bm_name = {bm_name}
                bm_address_1 = {bm_address_1}
                bm_address_2 = {bm_address_2}
                bm_dob = {bm_dob}
                bm_phone_no = {bm_phone_no}
                bm_mob_no = {bm_mob_no}
                bm_email = {bm_email}
                branch_loc = {branch_loc}
                bank_name = {bank_name}
                acc_no = {acc_no}
                ifsc_code = {ifsc_code}
                pan_no = {pan_no}
                aadhaar_no = {aadhaar_no}
            """)
            if Branch_Manager.objects.filter(PAN_NO=pan_no).exists():
                return JsonResponse({"error":"This Pan Card details is already exists"},status=412)
            else:
                add_bm = Branch_Manager.objects.create(
                    # CODE = bm_code ,
                    NAME = bm_name ,
                    ADD1 = bm_address_1 ,
                    ADD2 = bm_address_2 ,
                    DOB = bm_dob ,
                    PHONE = bm_phone_no ,
                    MOB_NO = bm_mob_no ,
                    EMAIL = bm_email ,
                    BANK_NAME = bank_name,
                    ACC_NO = acc_no,
                    IFSC_CODE = ifsc_code,
                    PAN_NO = pan_no,
                    AADHAAR_NO = aadhaar_no,
                    BRANCH_LOC = Branch_location_master.objects.get(id = branch_loc),
                    CREATED_BY = User.objects.get(id=login_id)
                )
                messages.success(request,"Branch Manager Add successfully")
                # return redirect("/branch_manager_master")
                return JsonResponse({"message":"Branch Manager Add successfully"},status=200)
        except Exception as e:
            messages.error(request,"Something went wrong")
            logger.exception(f"{e}")
            return JsonResponse(f"{e}",safe=False,status=500)

class Edit_Branch_Manager(APIView):
    def get(self,request,id):
        bml = Branch_location_master.objects.values('id',"NAME")
        bm = Branch_Manager.objects.get(id=id)  
        return render(request,"edit_branch_manager.html",context={"bm":bm,"bml":bml})
    def post(self,request,id):
        try:
            login_id   = request.session['LOGIN_ID']
            # previous_url = (request.POST.get("previous_url")).replace('http://43.204.0.1:9003/','')
            # usl = previous_url.split("/")
            # logger.info(f"previous_url = {previous_url}")
            # logger.info(f"usl = {usl}")
            

            # bm_code = request.POST.get("bm_code")
            bm_name = request.POST.get("bm_name")
            bm_address_1 = request.POST.get("bm_address_1")
            bm_address_2 = request.POST.get("bm_address_2")
            bm_dob = request.POST.get("bm_dob")
            bm_phone_no = request.POST.get("bm_phone_no")
            bm_mob_no = request.POST.get("bm_mob_no")
            bm_email = request.POST.get("bm_email")
            branch_loc = request.POST.get("branch_loc")
            bank_name = request.POST.get("bank_name")
            acc_no = request.POST.get("acc_no")
            ifsc_code = request.POST.get("ifsc_code")
            pan_no = request.POST.get("pan_no")
            aadhaar_no = request.POST.get("aadhaar_no")

            logger.info(f"""
                login_id = {login_id}
                bm_name = {bm_name}
                bm_address_1 = {bm_address_1}
                bm_address_2 = {bm_address_2}
                bm_dob = {bm_dob}
                bm_phone_no = {bm_phone_no}
                bm_mob_no = {bm_mob_no}
                bm_email = {bm_email}
                bm_email = {branch_loc}
                bank_name = {bank_name}
                acc_no = {acc_no}
                ifsc_code = {ifsc_code}
                pan_no = {pan_no}
                aadhaar_no = {aadhaar_no}
            """)
            
            if Branch_Manager.objects.filter(PAN_NO=pan_no).exclude(id=id).exists():
                return JsonResponse({"error":"This Pan Card details is already exists"},status=412)
            else:
                edit_bm = Branch_Manager.objects.get(id= id)
                edit_bm.NAME = bm_name
                edit_bm.ADD1 = bm_address_1
                edit_bm.ADD2 = bm_address_2
                edit_bm.DOB = bm_dob
                edit_bm.PHONE = bm_phone_no
                edit_bm.MOB_NO = bm_mob_no
                edit_bm.EMAIL = bm_email
                edit_bm.BANK_NAME = bank_name
                edit_bm.ACC_NO = acc_no
                edit_bm.IFSC_CODE = ifsc_code
                edit_bm.PAN_NO = pan_no
                edit_bm.AADHAAR_NO = aadhaar_no
                edit_bm.BRANCH_LOC = Branch_location_master.objects.get(id = branch_loc)
                edit_bm.MODIFIED_BY = User.objects.get(id=login_id)
                edit_bm.save()
                a = User.objects.filter(BM=id).update(NAME = bm_name)
                
                messages.success(request,"Branch Manager Edited successfully")
                # return redirect(f"/{previous_url}")
                return JsonResponse({"message":"Branch Manager Edited successfully"},status=200)
        except Exception as e:
            messages.error(request,"Something went wrong")
            logger.exception(f"{e}")
            return JsonResponse(f"{e}",safe=False,status=500)

def load_rm_data(request):
    data=list(Relationship_Manager.objects.values("LOGIN__EMPLOYEE_CODE","LOGIN__USERNAME","id","PAN_NO","BRANCH__NAME","CODE","NAME","DOB","PHONE","MOB_NO","EMAIL","CREATE_LOGIN").order_by("-id"))
    return JsonResponse({"data":data},safe=False)

class Relationship_Manager_Page(APIView):
    def get(self,request):
        # bm_data = Branch_Manager.objects.values("CODE","NAME")
        return render(request,"relationship_manager.html")
    
class Add_Relationship_Manager(APIView):
    def get(self,request):
        branch = Branch_Manager.objects.values("id","NAME")
        return render(request,"add_relationship_manager.html",context={"branch":branch})
    def post(self,request):
        try:
            # rm_code = request.POST.get("rm_code")
            rm_name = request.POST.get("rm_name")
            rm_address_1 = request.POST.get("rm_address_1")
            rm_address_2 = request.POST.get("rm_address_2")
            rm_dob = request.POST.get("rm_dob")
            rm_phone_no = request.POST.get("rm_phone_no")
            rm_mob_no = request.POST.get("rm_mob_no")
            rm_email = request.POST.get("rm_email")
            rm_branch_manager = request.POST.get("rm_branch_manager")
            # bank_name = request.POST.get("bank_name")
            rm_bank_name = request.POST.get("rm_bank_name")
            acc_no = request.POST.get("acc_no")
            ifsc_code = request.POST.get("ifsc_code")
            pan_no = request.POST.get("pan_no")
            aadhaar_no = request.POST.get("aadhaar_no")
            pan_card_img = request.data.get("pan_card_img")
            aadhar_card_img  = request.data.get("aadhar_card_img")
            relieving_letter_img = request.data.get("relieving_letter_img")
            cheque_img = request.data.get("cheque_img")
            education_cerificate_img = request.data.get("education_cerificate_img")

            logger.info(f"""
                rm_name = {rm_name}
                rm_address_1 = {rm_address_1}
                rm_address_2 = {rm_address_2}
                rm_dob = {rm_dob}
                rm_phone_no = {rm_phone_no}
                rm_mob_no = {rm_mob_no}
                rm_email = {rm_email}
                rm_branch_manager = {rm_branch_manager}
                bank_name = {rm_bank_name}
                ifsc_code = {ifsc_code}
                pan_no = {pan_no}
                aadhaar_no = {aadhaar_no}
                pan_card_img ={pan_card_img}
                aadhar_card_img ={aadhar_card_img}
                relieving_letter_img = {relieving_letter_img}
                cheque_img = {cheque_img}
                education_cerificate_img = {education_cerificate_img}
            """)
            if Relationship_Manager.objects.filter(PAN_NO=pan_no).exists():
                return JsonResponse({"error":"This Pan Card details is already exists"},status=412)
            else:
                add_rm = Relationship_Manager.objects.create(
                    NAME = rm_name ,
                    ADD1 = rm_address_1 ,
                    ADD2 = rm_address_2 ,
                    DOB = rm_dob ,
                    PHONE = rm_phone_no ,
                    MOB_NO = rm_mob_no ,
                    EMAIL = rm_email ,
                    BRANCH = Branch_Manager.objects.get(id=rm_branch_manager) ,
                    # BANK = Bank_master.objects.get(id= bank_name) ,
                    BANK_NAME = rm_bank_name ,
                    ACC_NO = acc_no ,
                    IFSC_CODE = ifsc_code,
                    PAN_NO = pan_no ,
                    AADHAAR_NO = aadhaar_no ,
                    CREATED_BY = User.objects.get(id=request.session['LOGIN_ID'])
                )
                if pan_card_img is not None:
                    add_rm.PAN_IMG      = pan_card_img
                
                if aadhar_card_img is not None:
                        add_rm.AADHAAR_IMG  = aadhar_card_img

                if relieving_letter_img is not None:
                        add_rm.RELIEVING_LETTER_IMG  = relieving_letter_img

                if cheque_img is not None:
                        add_rm.CHEQUE_IMG  = cheque_img

                if education_cerificate_img is not None:
                        add_rm.EDUCATION_CERIFICATE_IMG  = education_cerificate_img
                messages.success(request,"Relationship Manager Add successfully")
                # return redirect("/relationship_manager_master")
                return JsonResponse({"message":"Relationship Manager Add successfully"},status=200)
        except Exception as e:
            messages.error(request,"Something went wrong")
            logger.exception(f"{e}")
            return JsonResponse({"error":"Something went wrong"},safe=False,status=500)
        
class Edit_Relationship_Manager(APIView):
    def get(self,request,id):
        branch = Branch_Manager.objects.values("id","NAME")
        rm = Relationship_Manager.objects.get(id=id)
        rm2 = Relationship_Manager.objects.get(id=id).LOGIN_id
       
        print(rm2)
        ecode = User.objects.get(id=rm2).EMPLOYEE_CODE
        print(ecode)
        return render(request,"edit_relationship_manager.html",context={"rm":rm,"branch":branch, "ecode":ecode})
    def post(self,request,id):
        try:
            # previous_url = (request.POST.get("previous_url")).replace('http://43.204.0.1:9003/','')
            # logger.info(f"previous_url = {previous_url}")
            
            rm_ecode = request.POST.get("rm_code")
            rm_name = request.POST.get("rm_name")
            rm_address_1 = request.POST.get("rm_address_1")
            rm_address_2 = request.POST.get("rm_address_2")
            rm_dob = request.POST.get("rm_dob")
            rm_phone_no = request.POST.get("rm_phone_no")
            rm_mob_no = request.POST.get("rm_mob_no")
            rm_email = request.POST.get("rm_email")
            rm_branch_manager = request.POST.get("rm_branch_manager")
            # bank_name = request.POST.get("bank_name")
            acc_no = request.POST.get("acc_no")
            ifsc_code = request.POST.get("ifsc_code")
            rm_bank_name = request.POST.get("rm_bank_name")
            pan_no = request.POST.get("pan_no")
            aadhaar_no = request.POST.get("aadhaar_no")
            pan_card_img = request.data.get("pan_card_img")
            aadhar_card_img  = request.data.get("aadhar_card_img")
            relieving_letter_img = request.data.get("relieving_letter_img")
            cheque_img = request.data.get("cheque_img")
            education_cerificate_img = request.data.get("education_cerificate_img")

            logger.info(f"""
                rm_name = {rm_name}
                rm_address_1 = {rm_address_1}
                rm_address_2 = {rm_address_2}
                rm_dob = {rm_dob}
                rm_phone_no = {rm_phone_no}
                rm_mob_no = {rm_mob_no}
                rm_email = {rm_email}
                rm_branch_manager = {rm_branch_manager}
                bank_name = {rm_bank_name}
                ifsc_code = {ifsc_code}
                acc_no = {acc_no}
                pan_no = {pan_no}
                aadhaar_no = {aadhaar_no}
                pan_card_img ={pan_card_img}
                aadhar_card_img ={aadhar_card_img}
                relieving_letter_img = {relieving_letter_img}
                cheque_img = {cheque_img}
                education_cerificate_img = {education_cerificate_img}
            """)
            if User.objects.filter(EMPLOYEE_CODE=rm_ecode).exists():
                if not User.objects.filter(EMPLOYEE_CODE=rm_ecode, USER_ID=id).exists():
                    return JsonResponse({"error":"Employee code is already exists"},status=412)

            if Relationship_Manager.objects.filter(PAN_NO=pan_no).exclude(id=id).exists():
                return JsonResponse({"error":"This Pan Card details is already exists"},status=412)
            else:
                
                edit_rm = Relationship_Manager.objects.get(id=id)
                edit_rm.NAME = rm_name
                edit_rm.ADD1 = rm_address_1
                edit_rm.ADD2 = rm_address_2
                edit_rm.DOB = rm_dob
                edit_rm.PHONE = rm_phone_no
                edit_rm.MOB_NO = rm_mob_no
                edit_rm.EMAIL = rm_email
                edit_rm.BRANCH = Branch_Manager.objects.get(id=rm_branch_manager)
                # edit_rm.BANK = Bank_master.objects.get(id= bank_name)
                edit_rm.BANK_NAME = rm_bank_name
                edit_rm.IFSC_CODE = ifsc_code
                edit_rm.ACC_NO = acc_no
                edit_rm.PAN_NO = pan_no
                edit_rm.AADHAAR_NO = aadhaar_no
                edit_rm.MODIFIED_BY = User.objects.get(id=request.session['LOGIN_ID'])
                if pan_card_img is not None:
                    edit_rm.PAN_IMG      = pan_card_img
                
                if aadhar_card_img is not None:
                    edit_rm.AADHAAR_IMG  = aadhar_card_img

                if relieving_letter_img is not None:
                    edit_rm.RELIEVING_LETTER_IMG  = relieving_letter_img

                if cheque_img is not None:
                    edit_rm.CHEQUE_IMG  = cheque_img

                if education_cerificate_img is not None:
                    edit_rm.EDUCATION_CERIFICATE_IMG  = education_cerificate_img
                edit_rm.save()

                User.objects.filter(RM=id).update(NAME = rm_name)
                User.objects.filter(RM=id).update(EMPLOYEE_CODE=rm_ecode, EMPLOYEE_NUMBER=rm_ecode[2:])


                messages.success(request,"Relationship Manager Edited successfully")
                # return redirect(f"/{previous_url}")
                return JsonResponse({"message":"Relationship Manager Edited successfully"},status=200)
        except Exception as e:
            messages.error(request,"Something went wrong")
            logger.exception(f"{e}")
            print(e)
            return JsonResponse({"error":"Something went wrong"},safe=False,status=500)


def bo_page(request):
    return render(request,"bo.html")

def add_bo_page(request):
    return render(request,"add_bo.html")

def edit_bo_page(request,id):
    data = Back_Office.objects.get(id=id)
    return render(request,"edit_bo.html",context={"data":data})

@api_view(["POST"])
def add_bo_api(request):
    try:
        logger.info(f"request = {request.data}")
        login_id   = request.session['LOGIN_ID']
        # bo_code = request.data.get("bo_code")
        bo_name = request.POST.get("bo_name")
        bo_address_1 = request.data.get("bo_address_1")
        bo_address_2 = request.data.get("bo_address_2")
        bo_dob = request.data.get("bo_dob")
        bo_phone_no = request.data.get("bo_phone_no")
        bo_mob_no = request.data.get("bo_mob_no")
        bo_email = request.data.get("bo_email")
        bank_name = request.data.get("bank_name")
        acc_no = request.data.get("acc_no")
        ifsc_code = request.data.get("ifsc_code")
        pan_no = request.data.get("pan_no")
        aadhaar_no = request.data.get("aadhaar_no")
        pan_card_img = request.data.get("pan_card_img")
        aadhar_card_img  = request.data.get("aadhar_card_img")
        relieving_letter_img = request.data.get("relieving_letter_img")
        cheque_img = request.data.get("cheque_img")
        education_cerificate_img = request.data.get("education_cerificate_img")
        
        logger.info(f"""
            bo_name = {bo_name}
            bo_address_1 = {bo_address_1}
            bo_address_2 = {bo_address_2}
            bo_dob = {bo_dob}
            bo_phone_no = {bo_phone_no}
            bo_mob_no = {bo_mob_no}
            bo_email = {bo_email}
            bank_name = {bank_name}
            acc_no = {acc_no}
            ifsc_code = {ifsc_code}
            pan_no = {pan_no}
            aadhaar_no = {aadhaar_no}
            pan_card_img ={pan_card_img}
            aadhar_card_img ={aadhar_card_img}
            relieving_letter_img = {relieving_letter_img}
            cheque_img = {cheque_img}
            education_cerificate_img = {education_cerificate_img}
        """)

        if Back_Office.objects.filter(PAN_NO=pan_no).exists():
            return JsonResponse({"error":"This Pan Card details is already exists"},status=412)
        else:
            add_bm = Back_Office.objects.create(
                # CODE = bo_code ,
                NAME = bo_name ,
                ADD1 = bo_address_1 ,
                ADD2 = bo_address_2 ,
                DOB = bo_dob ,
                PHONE = bo_phone_no ,
                MOB_NO = bo_mob_no ,
                EMAIL = bo_email ,
                BANK_NAME = bank_name,
                ACC_NO = acc_no,
                IFSC_CODE = ifsc_code,
                PAN_NO = pan_no,
                AADHAAR_NO = aadhaar_no,
                CREATED_BY = User.objects.get(id=login_id)
            )
            if pan_card_img is not None:
                    add_bm.PAN_IMG      = pan_card_img
                
            if aadhar_card_img is not None:
                    add_bm.AADHAAR_IMG  = aadhar_card_img

            if relieving_letter_img is not None:
                    add_bm.RELIEVING_LETTER_IMG  = relieving_letter_img

            if cheque_img is not None:
                    add_bm.CHEQUE_IMG  = cheque_img

            if education_cerificate_img is not None:
                    add_bm.EDUCATION_CERIFICATE_IMG  = education_cerificate_img


            add_bm.save()
            messages.success(request,"Back Office Employee Added Successfully")
            # return redirect("/branch_manager_master")
        return JsonResponse({"message":"Back Office Employee Added Successfully"},status=200)
    except Exception as e:
        messages.error(request,"Something went wrong")
        logger.exception(f"{e}")
        return JsonResponse(f"{e}",safe=False,status=500)

@api_view(["POST"])
def edit_bo_api(request,id):
    try:
        login_id   = request.session['LOGIN_ID']
        # previous_url = (request.POST.get("previous_url")).replace('http://43.204.0.1:9003/','')
        # usl = previous_url.split("/")
        # logger.info(f"previous_url = {previous_url}")
        # logger.info(f"usl = {usl}")
        

        # bo_code = request.POST.get("bo_code")
        bo_name = request.POST.get("bo_name")
        bo_address_1 = request.POST.get("bo_address_1")
        bo_address_2 = request.POST.get("bo_address_2")
        bo_dob = request.POST.get("bo_dob")
        bo_phone_no = request.POST.get("bo_phone_no")
        bo_mob_no = request.POST.get("bo_mob_no")
        bo_email = request.POST.get("bo_email")
        branch_loc = request.POST.get("branch_loc")
        bank_name = request.POST.get("bank_name")
        acc_no = request.POST.get("acc_no")
        ifsc_code = request.POST.get("ifsc_code")
        pan_no = request.POST.get("pan_no")
        aadhaar_no = request.POST.get("aadhaar_no")
        pan_card_img = request.data.get("pan_card_img")
        aadhar_card_img = request.data.get("aadhar_card_img")
        relieving_letter_img = request.data.get("relieving_letter_img")
        cheque_img = request.data.get("cheque_img")
        education_cerificate_img = request.data.get("education_cerificate_img")

        logger.info(f"""
            login_id = {login_id}
            bo_name = {bo_name}
            bo_address_1 = {bo_address_1}
            bo_address_2 = {bo_address_2}
            bo_dob = {bo_dob}
            bo_phone_no = {bo_phone_no}
            bo_mob_no = {bo_mob_no}
            bo_email = {bo_email}
            bo_email = {branch_loc}
            bank_name = {bank_name}
            acc_no = {acc_no}
            ifsc_code = {ifsc_code}
            pan_no = {pan_no}
            aadhaar_no = {aadhaar_no}
            pan_card_img ={pan_card_img}
            aadhar_card_img ={aadhar_card_img}
            relieving_letter_img = {relieving_letter_img}
            cheque_img = {cheque_img}
            education_cerificate_img = {education_cerificate_img}
        """)
        
        if Back_Office.objects.filter(PAN_NO=pan_no).exclude(id=id).exists():
            return JsonResponse({"error":"This Pan Card details is already exists"},status=412)
        else:
            edit_bo = Back_Office.objects.get(id= id)
            edit_bo.NAME = bo_name
            edit_bo.ADD1 = bo_address_1
            edit_bo.ADD2 = bo_address_2
            edit_bo.DOB = bo_dob
            edit_bo.PHONE = bo_phone_no
            edit_bo.MOB_NO = bo_mob_no
            edit_bo.EMAIL = bo_email
            edit_bo.BANK_NAME = bank_name
            edit_bo.ACC_NO = acc_no
            edit_bo.IFSC_CODE = ifsc_code
            edit_bo.PAN_NO = pan_no
            edit_bo.AADHAAR_NO = aadhaar_no
            edit_bo.MODIFIED_BY = User.objects.get(id=login_id)

            if pan_card_img is not None:
                    edit_bo.PAN_IMG      = pan_card_img
                
            if aadhar_card_img is not None:
                    edit_bo.AADHAAR_IMG  = aadhar_card_img

            if relieving_letter_img is not None:
                    edit_bo.RELIEVING_LETTER_IMG  = relieving_letter_img

            if cheque_img is not None:
                    edit_bo.CHEQUE_IMG  = cheque_img

            if education_cerificate_img is not None:
                    edit_bo.EDUCATION_CERIFICATE_IMG  = education_cerificate_img

            edit_bo.save()
            
            User.objects.filter(BO=id).update(NAME = bo_name)
            
            messages.success(request,"Back Office Employee Updated successfully")
            # return redirect(f"/{previous_url}")
            return JsonResponse({"message":"Back Office Employee Updated successfully"},status=200)
    except Exception as e:
        messages.error(request,"Something went wrong")
        logger.exception(f"{e}")
        return JsonResponse(f"{e}",safe=False,status=500)

def delete_bo_api(request,id):
    try:
        Back_Office.objects.filter(id=id).delete()
        return JsonResponse({"message":"Back Office Employee Deleted successfully"},status=200)
    except Exception as e:
        messages.error(request,"Something went wrong")
        logger.exception(f"{e}")
        return JsonResponse(f"{e}",safe=False,status=500)

def load_bo_data_api(request):
    data = list(Back_Office.objects.values("id","PAN_NO","LOGIN__EMPLOYEE_CODE","LOGIN__USERNAME","NAME","DOB","PHONE","MOB_NO","EMAIL","CREATE_LOGIN").order_by("-id"))
    return JsonResponse({"data":data},safe=False,status=200)


class EP_Page(APIView):
    def get(self,request):
        return render(request,"easy_partner.html")

class Add_Easy_Partner(APIView):
    def get(self,request):
        rm_data = Relationship_Manager.objects.values("id","NAME")
        return render(request,"add_easy_partner.html",context={"rm_data":rm_data})
    def post(self,request):
        try:
            rm_id = request.POST.get("rm_id")
            sb_name = request.POST.get("sb_name")
            sb_address_1 = request.POST.get("sb_address_1")
            sb_address_2 = request.POST.get("sb_address_2")
            sb_dob = request.POST.get("sb_dob")
            sb_phone_no = request.POST.get("sb_phone_no")
            sb_mob_no = request.POST.get("sb_mob_no")
            sb_email = request.POST.get("sb_email")
            # sb_bank_name = request.POST.get("bank_name")
            
            sb_bank_name = request.POST.get("sb_bank_name")
            acc_no = request.POST.get("acc_no")
            ifsc_code = request.POST.get("ifsc_code")
            sb_pan_no = request.POST.get("sb_pan_no")
            aadhaar_no = request.POST.get("aadhaar_no")
            commission_percentage = request.POST.get("commission_percentage")

            cheque_no       = request.POST.get("cheque_no")
            nominee_name    = request.POST.get("nominee_name")

            pan_card_img    = request.FILES.get("pan_card_img")
            aadhar_card_img = request.FILES.get("aadhar_card_img")
            cheque_img      = request.FILES.get("cheque_img")
            nominee_img     = request.FILES.get("nominee_img")

            logger.info(f"""
                rm_id                   = {rm_id}
                sb_name                 = {sb_name}
                sb_address_1            = {sb_address_1}
                sb_address_2            = {sb_address_2}
                sb_dob                  = {sb_dob}
                sb_phone_no             = {sb_phone_no}
                sb_mob_no               = {sb_mob_no}
                sb_email                = {sb_email}
                sb_bank_name            = {sb_bank_name}
                acc_no                  = {acc_no}
                ifsc_code               = {ifsc_code}
                sb_pan_no               = {sb_pan_no}
                aadhaar_no              = {aadhaar_no}
                commission_percentage   = {commission_percentage}

                cheque_no               = {cheque_no}
                nominee_name            = {nominee_name}
                pan_card_img            = {pan_card_img}
                aadhar_card_img         = {aadhar_card_img}
                cheque_img              = {cheque_img}
                nominee_img             = {nominee_img}
            """)
            if Easy_Partner.objects.filter(PAN_NO=sb_pan_no).exists():
                return JsonResponse({"error":"This Pan Card details is already exists"},status=412)
            else:
                add_sb = Easy_Partner.objects.create(
                    RM = Relationship_Manager.objects.get(id=rm_id),
                    NAME = sb_name ,
                    ADD1 = sb_address_1 ,
                    ADD2 = sb_address_2 ,
                    DOB = sb_dob ,
                    PHONE = sb_phone_no ,
                    MOB_NO = sb_mob_no ,
                    EMAIL = sb_email ,

                    BANK_NAME = sb_bank_name ,
                    ACC_NO = acc_no,
                    IFSC_CODE = ifsc_code,
                    # BANK = Bank_master.objects.get(id=sb_bank_name) ,
                    PAN_NO = sb_pan_no ,
                    AADHAAR_NO = aadhaar_no,
                    MF_C_P = commission_percentage,
                    NOMINEE_NAME = nominee_name,
                    CHEQUE_NO = cheque_no,
                    CREATED_BY = User.objects.get(id=request.session['LOGIN_ID'])
                )
                if pan_card_img is not None:
                    add_sb.PAN_IMG = pan_card_img
                if aadhar_card_img is not None:
                    add_sb.AADHAAR_IMG = aadhar_card_img
                if cheque_img is not None:
                    add_sb.CHEQUE_IMG = cheque_img
                if nominee_img is not None:
                    add_sb.NOMINEE_IMG = nominee_img
                add_sb.save()
                messages.success(request,"Easy Partner Add successfully")
                # return redirect("/easy_partner_master")
                return JsonResponse({"message":"Easy Partner Add successfully"},status=200)
        except Exception as e:
            messages.error(request,"Something went wrong")
            logger.exception(f"{e}")
            return JsonResponse({"error":"Something went wrong"},safe=False,status=500)

def get_easy_partner(request,id):
    data =  Easy_PartnerSerializer(Easy_Partner.objects.get(id=id),many=False).data
    return JsonResponse(data,safe=False,status=200)

class Edit_Easy_Partner(APIView):
    def get(self,request,id):
        sb = Easy_Partner.objects.get(id=id)
        rm_data = Relationship_Manager.objects.values("id","NAME")
        return render(request,"edit_easy_partner.html",context={"sb":sb,"rm_data":rm_data})
    def post(self,request,id):
        try:
            # previous_url = (request.POST.get("previous_url")).replace('http://43.204.0.1:9003/','')
            rm_id = request.POST.get("rm_id")
            sb_name = request.POST.get("sb_name")
            sb_address_1 = request.POST.get("sb_address_1")
            sb_address_2 = request.POST.get("sb_address_2")
            sb_dob = request.POST.get("sb_dob")
            sb_phone_no = request.POST.get("sb_phone_no")
            sb_mob_no = request.POST.get("sb_mob_no")
            sb_email = request.POST.get("sb_email")
            # sb_bank_name = request.POST.get("bank_name")
            sb_bank_name = request.POST.get("sb_bank_name")
            acc_no = request.POST.get("acc_no")
            ifsc_code = request.POST.get("ifsc_code")
            sb_pan_no = request.POST.get("sb_pan_no")
            aadhaar_no = request.POST.get("aadhaar_no")
            commission_percentage = request.POST.get("commission_percentage")

            cheque_no       = request.POST.get("cheque_no")
            nominee_name    = request.POST.get("nominee_name")

            pan_card_img    = request.FILES.get("pan_card_img")
            aadhar_card_img = request.FILES.get("aadhar_card_img")
            cheque_img      = request.FILES.get("cheque_img")
            nominee_img     = request.FILES.get("nominee_img")

            logger.info(f"""rm_id = {rm_id}
                sb_name = {sb_name}
                sb_address_1 = {sb_address_1}
                sb_address_2 = {sb_address_2}
                sb_dob = {sb_dob}
                sb_phone_no = {sb_phone_no}
                sb_mob_no = {sb_mob_no}
                sb_email = {sb_email}
                sb_bank_name = {sb_bank_name}
                ifsc_code = {ifsc_code}
                acc_no ={acc_no}
                sb_pan_no = {sb_pan_no}
                aadhaar_no = {aadhaar_no}
                commission_percentage = {commission_percentage}

                cheque_no               = {cheque_no}
                nominee_name            = {nominee_name}
                pan_card_img            = {pan_card_img}
                aadhar_card_img         = {aadhar_card_img}
                cheque_img              = {cheque_img}
                nominee_img             = {nominee_img}
            """)
            if Easy_Partner.objects.filter(PAN_NO=sb_pan_no).exclude(id=id).exists():
                return JsonResponse({"error":"This Pan Card details is already exists"},status=412)
            else:
                edit_sb = Easy_Partner.objects.get(id=id)
                edit_sb.RM = Relationship_Manager.objects.get(id=rm_id)
                edit_sb.NAME = sb_name
                edit_sb.ADD1 = sb_address_1
                edit_sb.ADD2 = sb_address_2
                edit_sb.DOB = sb_dob
                edit_sb.PHONE = sb_phone_no
                edit_sb.MOB_NO = sb_mob_no
                edit_sb.EMAIL = sb_email
                edit_sb.BANK_NAME = sb_bank_name
                edit_sb.ACC_NO = acc_no
                edit_sb.IFSC_CODE = ifsc_code
                # edit_sb.BANK = Bank_master.objects.get(id=sb_bank_name)
                edit_sb.PAN_NO = sb_pan_no
                edit_sb.AADHAAR_NO = aadhaar_no
                edit_sb.MF_C_P = commission_percentage
                edit_sb.MODIFIED_BY = User.objects.get(id=request.session['LOGIN_ID'])

                edit_sb.NOMINEE_NAME = nominee_name
                edit_sb.CHEQUE_NO = cheque_no

                if pan_card_img is not None:
                    edit_sb.PAN_IMG = pan_card_img
                if aadhar_card_img is not None:
                    edit_sb.AADHAAR_IMG = aadhar_card_img
                if cheque_img is not None:
                    edit_sb.CHEQUE_IMG = cheque_img
                if nominee_img is not None:
                    edit_sb.NOMINEE_IMG = nominee_img
                edit_sb.save()

                
                User.objects.filter(EP=id).update(NAME = sb_name)
                messages.success(request,"Easy Partner Edit successfully")
                return JsonResponse({"message":"Easy Partner Edit successfully"},status=200)
            # return redirect(f"/{previous_url}")
        except Exception as e:
            messages.error(request,"Something went wrong")
            logger.exception(f"{e}")
            return JsonResponse({"error":"Something went wrong"},safe=False,status=500)


def load_ep_data(request):
    # data = Easy_PartnerSerializer(Easy_Partner.objects.all().order_by("-id"),many=True).data
    data = list(Easy_Partner.objects.values("LOGIN__id","LOGIN__EMPLOYEE_CODE","LOGIN__USERNAME","RM__NAME","id","NAME","PAN_NO","DOB","PHONE","MOB_NO","EMAIL","BANK_NAME","NAME","CREATE_LOGIN").order_by("-id"))
    return JsonResponse({"data":data},safe=False)

@api_view(["POST"])
def get_user_ep_code(request,id):
    try:
        # user_id = request.data.get("user_id")
        data = User.objects.get(id=id)

        data = {
            "name"      : data.EP.NAME,
            "ep_code"   : data.EMPLOYEE_NUMBER
            }
        # EMPLOYEE_CODE
        return JsonResponse(data,safe=False,status=200)
    except Exception as e:
        logger.exception(f"{e}")
        return JsonResponse(f"{e}",safe=False,status=500)
    

@api_view(["POST"])
def edit_user_ep_code(request,id):
    try:
        # ep_name = request.POST.get("ep_name")
        ep_code = request.POST.get("ep_code")
        data                    = User.objects.get(id=id)
        data.EMPLOYEE_NUMBER    = ep_code
        data.EMPLOYEE_CODE      = f"EP{ep_code}"
        data.save()

        return JsonResponse("Ep Code Change Successfully",safe=False,status=200)
    except Exception as e:
        logger.exception(f"{e}")
        return JsonResponse(f"{e}",safe=False,status=500)

class BM_Brokerage_Page(APIView):
    def get(self,request):
        return render(request,"bm_brokerage.html")

class Add_BM_Brokerage(APIView):
    def get(self,request):
        data = Branch_Manager.objects.values("id","NAME")
        return render(request,"add_bm_brokerage.html",context={"data":data})
    def post(self,request):
        try:
            dob = request.POST.get("dob")
            bm_name = request.POST.get("bm_name")
            amc_name = request.POST.get("amc_name")
            trail = request.POST.get("trail")
        
            logger.info(f"""
                dob = {dob}
                bm_name = {bm_name}
                amc_name = {amc_name}
                trail = {trail}
            """)

            add_bm_bro = BM_Brokerage.objects.create(
                DOB = dob ,
                BM_NAME = Branch_Manager.objects.get(id=bm_name),
                AMC_NAME = amc_name ,
                TRAIL = trail ,
                CREATED_BY = User.objects.get(id=request.session['LOGIN_ID'])
            )
            messages.success(request,"BM Brokerage Add successfully")
            return redirect("/bm_brokerage")
            # return JsonResponse({"message":"Adviser Sub_broker Add successfully"},status=200)
        except Exception as e:
            messages.error(request,"Something went wrong")
            logger.exception(f"{e}")
            return JsonResponse({"error":"Something went wrong"},safe=False,status=500)
        
class Edit_BM_Brokerage(APIView):
    def get(self,request,id):
        bmbro_data = BM_Brokerage.objects.get(id=id)
        data = Branch_Manager.objects.values("id","NAME")
        return render(request,"edit_bm_brokerage.html",context={"data":data,"bmbro_data":bmbro_data})
    def post(self,request,id):
        try:
            dob = request.POST.get("dob")
            bm_name = request.POST.get("bm_name")
            amc_name = request.POST.get("amc_name")
            trail = request.POST.get("trail")
        
            logger.info(f"""
                dob = {dob}
                bm_name = {bm_name}
                amc_name = {amc_name}
                trail = {trail}
            """)

            edit_bm_bro = BM_Brokerage.objects.get(id=id)
            edit_bm_bro.DOB = dob
            edit_bm_bro.BM_NAME = Branch_Manager.objects.get(id=bm_name)
            edit_bm_bro.AMC_NAME = amc_name
            edit_bm_bro.TRAIL = trail
            edit_bm_bro.MODIFIED_BY = User.objects.get(id=request.session['LOGIN_ID'])
            edit_bm_bro.save()

            messages.success(request,"BM Brokerage Edited successfully")
            return redirect("/bm_brokerage")
            # return JsonResponse({"message":"Adviser Sub_broker Add successfully"},status=200)
        except Exception as e:
            messages.error(request,"Something went wrong")
            logger.exception(f"{e}")
            return redirect(f"/edit_bm_brokerage/{id}")
            # return JsonResponse({"error":"Something went wrong"},safe=False,status=500)

def load_bm_brokerage_data(request):
    data = BM_BrokerageSerializer(BM_Brokerage.objects.all().order_by("-id"),many=True).data
    return JsonResponse({"data":data},safe=False)

class RM_Brokerage_Page(APIView):
    def get(self,request):
        return render(request,"rm_brokerage.html")

class Add_RM_Brokerage(APIView):
    def get(self,request):
        data = Relationship_Manager.objects.values("id","NAME")
        return render(request,"add_rm_brokerage.html",context={"data":data})
    def post(self,request):
        try:
            dob = request.POST.get("dob")
            rm_name = request.POST.get("rm_name")
            amc_name = request.POST.get("amc_name")
            trail = request.POST.get("trail")
        
            logger.info(f"""
                dob = {dob}
                rm_name = {rm_name}
                amc_name = {amc_name}
                trail = {trail}
            """)

            add_rm_bro = RM_Brokerage.objects.create(
                DOB = dob ,
                RM_NAME = Relationship_Manager.objects.get(id=rm_name),
                AMC_NAME = amc_name ,
                TRAIL = trail ,
                CREATED_BY = User.objects.get(id=request.session['LOGIN_ID'])
            )
            messages.success(request,"RM Brokerage Add successfully")
            return redirect("/rm_brokerage")
            # return JsonResponse({"message":"Adviser Sub_broker Add successfully"},status=200)
        except Exception as e:
            messages.error(request,"Something went wrong")
            logger.exception(f"{e}")
            return redirect("/add_rm_brokerage")
            # return JsonResponse({"error":"Something went wrong"},safe=False,status=500)

class Edit_RM_Brokerage(APIView):
    def get(self,request,id):
        rmbro_data = RM_Brokerage.objects.get(id=id)
        data = Relationship_Manager.objects.values("id","NAME")
        return render(request,"edit_rm_brokerage.html",context={"data":data,"rmbro_data":rmbro_data})
    def post(self,request,id):
        try:
            dob = request.POST.get("dob")
            rm_name = request.POST.get("rm_name")
            amc_name = request.POST.get("amc_name")
            trail = request.POST.get("trail")
        
            logger.info(f"""
                dob = {dob}
                rm_name = {rm_name}
                amc_name = {amc_name}
                trail = {trail}
            """)

            edit_rm_bro = RM_Brokerage.objects.get(id=id)
            edit_rm_bro.DOB = dob
            edit_rm_bro.RM_NAME = Relationship_Manager.objects.get(id=rm_name)
            edit_rm_bro.AMC_NAME = amc_name
            edit_rm_bro.TRAIL = trail
            edit_rm_bro.MODIFIED_BY = User.objects.get(id=request.session['LOGIN_ID'])
            edit_rm_bro.save()

            messages.success(request,"RM Brokerage Edited successfully")
            return redirect("/rm_brokerage")
            # return JsonResponse({"message":"Adviser Sub_broker Add successfully"},status=200)
        except Exception as e:
            messages.error(request,"Something went wrong")
            logger.exception(f"{e}")
            return redirect(f"/edit_rm_brokerage/{id}")
            # return JsonResponse({"error":"Something went wrong"},safe=False,status=500)
        
def load_rm_brokerage_data(request):
    data = RM_BrokerageSerializer(RM_Brokerage.objects.all().order_by("-id"),many=True).data
    return JsonResponse({"data":data},safe=False)

class sub_broker_brokerage_page(APIView):
    def get(self,request):
        return render(request,"easy_partner_brokerage.html")

class Add_SUB_broker_Brokerage(APIView):
    def get(self,request):
        data = Easy_Partner.objects.values("id","NAME")
        return render(request,"add_easy_partner_brokerage.html",context={"data":data})
    def post(self,request):
        try:
            eff_date = request.POST.get("eff_date")
            partner_name = request.POST.get("partner_name")
            amc_name = request.POST.get("amc_name")
            trail = request.POST.get("trail")
            add_incentive = request.POST.get("add_incentive")
            for_type = request.POST.get("for_type")
            note = request.POST.get("note")
            logger.info(f"""
                eff_date = {eff_date}
                partner_name = {partner_name}
                amc_name = {amc_name}
                trail = {trail}
                add_incentive = {add_incentive}
                for_type = {for_type}
                note = {note}
            """)

            add_sb_bro = Easy_Partner_Brokerage.objects.create(
                EFFECTIVE_DATE = eff_date,
                PARTNER_NAME = Easy_Partner.objects.get(id=partner_name),
                AMC_NAME = amc_name,
                TRAIL = trail,
                ADD_INCENTIVE = add_incentive,
                TYPE = for_type,
                NOTE = note,
                CREATED_BY = User.objects.get(id=request.session['LOGIN_ID'])
            )
            messages.success(request,"Easy Partner Brokerage Add successfully")
            return redirect("/easy_partner_brokerage")
            # return JsonResponse({"message":"Adviser Sub_broker Add successfully"},status=200)
        except Exception as e:
            messages.error(request,"Something went wrong")
            logger.exception(f"{e}")
            return redirect("/add_easy_partner_brokerage")
        
def load_sub_brokerage_data(request):
    data = Sub_Broker_BrokerageSerializer(Easy_Partner_Brokerage.objects.all().order_by("-id"),many=True).data
    return JsonResponse({"data":data},safe=False)

class Edit_SUB_broker_Brokerage(APIView):
    def get(self,request,id):
        data = Easy_Partner.objects.values("id","NAME")
        sub_brokerage = Easy_Partner_Brokerage.objects.get(id=id)
        return render(request,"edit_easy_partner_brokerage.html",context={"data":data,"sub_brokerage":sub_brokerage})
    def post(self,request,id):
        try:
            eff_date = request.POST.get("eff_date")
            partner_name = request.POST.get("partner_name")
            amc_name = request.POST.get("amc_name")
            trail = request.POST.get("trail")
            add_incentive = request.POST.get("add_incentive")
            for_type = request.POST.get("for_type")
            note = request.POST.get("note")
            logger.info(f"""
                eff_date = {eff_date}
                partner_name = {partner_name}
                amc_name = {amc_name}
                trail = {trail}
                add_incentive = {add_incentive}
                for_type = {for_type}
                note = {note}
            """)

            add_sb_bro = Easy_Partner_Brokerage.objects.get(id=id)
            add_sb_bro.EFFECTIVE_DATE = eff_date
            add_sb_bro.PARTNER_NAME = Easy_Partner.objects.get(id=partner_name)
            add_sb_bro.AMC_NAME = amc_name
            add_sb_bro.TRAIL = trail
            add_sb_bro.ADD_INCENTIVE = add_incentive
            add_sb_bro.TYPE = for_type
            add_sb_bro.NOTE = note
            add_sb_bro.MODIFIED_BY = User.objects.get(id=request.session['LOGIN_ID'])
            add_sb_bro.save()

            messages.success(request,"Easy Partner Brokerage Edited successfully")
            return redirect("/easy_partner_brokerage")
            # return JsonResponse({"message":"Adviser Sub_broker Add successfully"},status=200)
        except Exception as e:
            messages.error(request,"Something went wrong")
            logger.exception(f"{e}")
            return redirect(f"/edit_easy_partner_brokerage/{id}")

def insurance_master_page(request):
    return render(request,"insurance_master.html")

class AddBulkInsuranceExcel(APIView):
  def post(self,request):
    try:
      excel_file = request.FILES.get("excel_file")
      # sheet_name = request.POST.get("sheet_name")
      UploadInsuranceMaster.objects.create(
        EXCEL = excel_file,
        # SHEET_NAME = sheet_name,
      )
      return JsonResponse({"message":"Excel Add Successfully"},status=200)
    except Exception as e:
      logger.exception(e)
      messages.error(request,"Something went wrong")
      return JsonResponse({"error":"Something went Wrong"},status=500)

def add_im_bulk(request):
  try:
    # xls = pd.ExcelFile('static/optical_crm_all_data.xlsx')
    # , sheet_name=f"{excel_data.SHEET_NAME}"
    excel_data = UploadInsuranceMaster.objects.last()
    df1 = pd.read_excel(f"media/{excel_data.EXCEL}",usecols=["INSURER" , "PRODUCT" , "PLAN_TYPE" ,"PPT","PT" ,"PB_GRID_OFFLINE", "PB_GRID_OFFLINE_PERCENT", "PB_GRID_RENEWAL" ,"PB_GRID_RENEWAL_PERCENT", "PB_GRID_ONLINE" ,"PB_GRID_ONLINE_PERCENT"])
    # d = UploadPurchaseExcel.objects.last().EXCEL.path
    # logger.info(f"dasdasd = {d}")
    # for index, row in df1.head(3).iterrows():
    for index, row in df1.iterrows():
        im = Insurance_master.objects.create(
        INSURER              = row['INSURER'],
        PRODUCT              = row['PRODUCT'],
        PLAN_TYPE            = row['PLAN_TYPE'],
        PPT                  = row['PPT'],
        PT                   = row['PT'] ,
        PB_G_OFF             = row['PB_GRID_OFFLINE'] ,
        PB_G_OFF_PERCENT     = row['PB_GRID_OFFLINE_PERCENT'],
        PB_RENEW_OFF         = row['PB_GRID_RENEWAL'],
        PB_RENEW_OFF_PERCENT = row['PB_GRID_RENEWAL_PERCENT'],
        PB_GRID_ON           = row['PB_GRID_ONLINE'],
        PB_GRID_ON_PERCENT   = row['PB_GRID_ONLINE_PERCENT'],
        CREATED_BY = User.objects.get(id=request.session['LOGIN_ID'])
        )
    UploadInsuranceMaster.objects.last().delete()
    messages.success(request,'Insurance Master Add Successfully')
    return JsonResponse({"message":"Insurance Master Add Successfully"},status=200)
  except Exception as e:
    logger.exception(e)
    messages.error(request,"Something went wrong")
    return JsonResponse({"error":"Something went Wrong"},status=500)

@api_view(["GET"])
def load_edit_im(request,id):
    data = list(Insurance_master.objects.filter(id=id).values())
    return JsonResponse(data,safe=False)

@api_view(["POST"])
def edit_im(request,id):
    try:
        insurer_name = request.POST.get("insurer_name")
        product = request.POST.get("product")
        plan_type = request.POST.get("plan_type")
        ppt = request.POST.get("ppt")
        pt = request.POST.get("pt")
        pb_off = request.POST.get("pb_off")
        pb_off_percent = request.POST.get("pb_off_percent")
        pb_renew = request.POST.get("pb_renew")
        pb_renew_percent = request.POST.get("pb_renew_percent")
        pb_on = request.POST.get("pb_on")
        pb_on_percent = request.POST.get("pb_on_percent")
        logger.info(f"""
            insurer_name = {insurer_name}
            product = {product}
            plan_type = {plan_type}
            ppt = {ppt}
            pt = {pt}
            pb_off = {pb_off}
            pb_off_percent = {pb_off_percent}
            pb_renew = {pb_renew}
            pb_renew_percent = {pb_renew_percent}
            pb_on = {pb_on}
            pb_on_percent = {pb_on_percent}
            user = {request.session['LOGIN_ID']}
            """)
        e = Insurance_master.objects.get(id=id)
        e.INSURER = insurer_name
        e.PRODUCT = product
        e.PLAN_TYPE = plan_type
        e.PPT = ppt
        e.PT = pt
        e.PB_G_OFF = pb_off
        e.PB_G_OFF_PERCENT = pb_off_percent
        e.PB_RENEW_OFF = pb_renew
        e.PB_RENEW_OFF_PERCENT = pb_renew_percent
        e.PB_GRID_ON = pb_on
        e.PB_GRID_ON_PERCENT = pb_on_percent
        e.MODIFIED_BY = User.objects.get(id=request.session['LOGIN_ID'])
        e.save()
        return JsonResponse("Insurance Master updated successfully",safe=False,status=200)
    except Exception as e:
        logger.exception(e)
        return JsonResponse("something went wrong",safe=False,status=500)

@api_view(['POST'])
def button_add_im_data(request):
    print("helo")
    try:
        insurer_name = request.POST.get("add_insurer_name")
        product = request.POST.get("add_product")
        plan_type = request.POST.get("add_plan_type")
        ppt = request.POST.get("add_ppt")
        pt = request.POST.get("add_pt")
        ei_grid_offline = request.POST.get("add_EI_off")
        ei_grid_offline_percent = request.POST.get("add_pb_off_percent")
        ei_grid_offline_renewal = request.POST.get("add_pb_renew")
        ei_grid_online = request.POST.get("add_pb_renew_percent")
        ei_grid_online_percent = request.POST.get("add_pb_on")
        ei_grid_online_renewal = request.POST.get("add_pb_on_percent")
        print(insurer_name, product, plan_type, ppt, pt, ei_grid_offline, ei_grid_offline_percent, ei_grid_offline_renewal, ei_grid_online, ei_grid_online_percent, ei_grid_online_renewal)
        # logger.info(f"""
        #     insurer_name = {insurer_name}
        #     product = {product}
        #     plan_type = {plan_type}
        #     ppt = {ppt}
        #     pt = {pt}
        #     pb_off = {pb_off}
        #     pb_off_percent = {pb_off_percent}
        #     pb_renew = {pb_renew}
        #     pb_renew_percent = {pb_renew_percent}
        #     pb_on = {pb_on}
        #     pb_on_percent = {pb_on_percent}
        #     user = {request.session['LOGIN_ID']}
        #     """)
        e = Insurance_master.objects.create(
        INSURER              = insurer_name,
        PRODUCT              = product,
        PLAN_TYPE            = plan_type,
        PPT                  = ppt,
        PT                   = pt,
        PB_G_OFF             = ei_grid_offline,
        PB_G_OFF_PERCENT     = ei_grid_offline_percent,
        PB_RENEW_OFF         = ei_grid_offline_renewal,
        PB_RENEW_OFF_PERCENT = ei_grid_online,
        PB_GRID_ON           = ei_grid_online_percent,
        PB_GRID_ON_PERCENT   = ei_grid_online_renewal,
        CREATED_BY = User.objects.get(id=request.session['LOGIN_ID']))
        print(User.objects.get(id=request.session['LOGIN_ID']))
        e.save()
        return JsonResponse("Insurance Master updated successfully",safe=False,status=200)
    except Exception as e:
        logger.exception(e)
        print(e)
        return JsonResponse("something went wrong",safe=False,status=500)
    

def load_im_data(request):
    data = list(Insurance_master.objects.values().order_by("-id"))
    
    return JsonResponse({"data":data},safe=False)
#------------------------------
def mf_master_page(request):
    return render(request,"mf_master.html")

class AddBulk_mfm_Excel(APIView):
  def post(self,request):
    try:
      excel_file = request.FILES.get("excel_file")
      # sheet_name = request.POST.get("sheet_name")
      UploadMFMaster.objects.create(
        EXCEL = excel_file,
        # SHEET_NAME = sheet_name,
      )
      return JsonResponse({"message":"Excel Add Successfully"},status=200)
    except Exception as e:
      logger.exception(e)
      messages.error(request,"Something went wrong")
      return JsonResponse({"error":"Something went Wrong"},status=500)

def Add_mfm_Bulk(request):
  try:
    # xls = pd.ExcelFile('static/optical_crm_all_data.xlsx')
    # , sheet_name=f"{excel_data.SHEET_NAME}"
    excel_data = UploadMFMaster.objects.last()
    df1 = pd.read_excel(f"media/{excel_data.EXCEL}",usecols=["SCHEME" , "E_C_PAYOUT" , "NET_A_GST" ,"EP_PAYOUT"])
    # d = UploadPurchaseExcel.objects.last().EXCEL.path
    # logger.info(f"dasdasd = {d}")
    # for index, row in df1.head(3).iterrows():
    for index, row in df1.iterrows():
        if MF_master.objects.filter(SCHEME =row['SCHEME']).exists():
            e = MF_master.objects.get(SCHEME =row['SCHEME'])
            e.E_C_P       = round(row['E_C_PAYOUT'],2)
            e.NET_A_GST   = round(row['NET_A_GST'],2)
            e.EP_PAYOUT   = round(row['EP_PAYOUT'],2)
            e.MODIFIED_BY = User.objects.get(id=request.session['LOGIN_ID'])
            e.save()
        else:
            mfm = MF_master.objects.create(
            SCHEME     = row['SCHEME'],
            E_C_P      = round(row['E_C_PAYOUT'],2),
            NET_A_GST  = round(row['NET_A_GST'],2),
            EP_PAYOUT  = round(row['EP_PAYOUT'],2),
            CREATED_BY = User.objects.get(id=request.session['LOGIN_ID'])
            )
    UploadMFMaster.objects.last().delete()
    messages.success(request,'Mutual Fund Add Successfully')
    return JsonResponse({"message":"Mutual Fund Add Successfully"},status=200)
  except Exception as e:
    logger.exception(e)
    messages.error(request,"Something went wrong")
    return JsonResponse({"error":f"{e}"},status=500)

@api_view(["GET"])
def load_edit_mfm(request,id):
    data = list(MF_master.objects.filter(id=id).values())
    return JsonResponse(data,safe=False)

@api_view(["POST"])
def edit_mfm(request,id):
    try:
        scheme_name = request.POST.get("scheme_name")
        e_c_payout = request.POST.get("e_c_payout")
        net_a_gst = request.POST.get("net_a_gst")
        ep_payout = request.POST.get("ep_payout")

        logger.info(f"""
            scheme_name = {scheme_name}
            e_c_payout = {e_c_payout}
            net_a_gst = {net_a_gst}
            ep_payout = {ep_payout}
            user = {request.session['LOGIN_ID']}
            """)
        e = MF_master.objects.get(id=id)
        e.SCHEME = scheme_name
        e.E_C_P = e_c_payout
        e.NET_A_GST = net_a_gst
        e.EP_PAYOUT = ep_payout
        e.MODIFIED_BY = User.objects.get(id=request.session['LOGIN_ID'])
        e.save()
        return JsonResponse("MF Master updated successfully",safe=False,status=200)
    except Exception as e:
        logger.exception(e)
        return JsonResponse("something went wrong",safe=False,status=500)


def load_mfm_data(request):
    data = list(MF_master.objects.values().order_by("-id"))
    return JsonResponse({"data":data},safe=False)

#--------------------------------------

def insurance_type_master_page(request):
    return render(request,"insurance_type_master.html")

class add_insurance_name(APIView):
    def post(self,request):
        try:
            login_id = request.session['LOGIN_ID']
            insurance_name = request.POST.get("insurance_name")
            # logger.info(f"""
            #     insurance_name = {insurance_name}
            # """)
            if Insurance_type_master.objects.filter(NAME=insurance_name).exists():
                return JsonResponse({"error":"This Insurance Name Already Exist"},status=412)
            else:
                add = Insurance_type_master.objects.create(
                    NAME = insurance_name,
                    CREATED_BY = User.objects.get(id=login_id)
                )
            # messages.success(request,"Sub Broker Brokerage Add successfully")
            # return redirect("/easy_partner_brokerage")
                return JsonResponse({"message":"Insurance Name Add successfully"},status=200)
        except Exception as e:
            # messages.error(request,"Something went wrong")
            logger.exception(f"{e}")
            # return redirect("/add_easy_partner_brokerage")
            return JsonResponse({"error":"something went wong"},status=200)

class edit_insurance_name(APIView):
    def get(self,request,id):
        data = list(Insurance_type_master.objects.filter(id=id).values("NAME"))
        return JsonResponse(data,safe=False)
    def post(self,request,id):
        try:
            login_id = request.session['LOGIN_ID']
            insurance_name = request.POST.get("insurance_name")
            logger.info(f"""
                insurance_name = {insurance_name}
            """)
            if Insurance_type_master.objects.filter(NAME=insurance_name).exclude(id=id).exists():
                return JsonResponse({"error":"This Insurance Name Already Exist"},status=412)
            else:
                edit = Insurance_type_master.objects.get(id=id)
                edit.NAME = insurance_name
                edit.MODIFIED_BY =  User.objects.get(id=login_id)
                edit.save()
            # messages.success(request,"Sub Broker Brokerage Add successfully")
            # return redirect("/easy_partner_brokerage")
                return JsonResponse({"message":"Insurance Name Edited successfully"},status=200)
        except Exception as e:
            # messages.error(request,"Something went wrong")
            logger.exception(f"{e}")
            # return redirect("/add_easy_partner_brokerage")
            return JsonResponse({"error":"something went wong"},status=200)

def load_insurance_name(request):
    data = list(Insurance_type_master.objects.values("id","NAME").order_by('-id'))
    return JsonResponse({"data":data},safe=False)

# def insurance_customer_api(request):
#     data = list(Insurance_Customer_Master.objects.all().values())
#     return JsonResponse(data,safe=False,status=200)
#     pass

def load_select_customer(request):
    user_type = request.session['USER_TYPE']
    v= ["id","C_NAME","MOB_NO"]
    if user_type == "bm" or user_type == "rm":
        final_list = get_under_mapped(request)
        # logger.info(f"final_list = {final_list}")
        data = list(Customer.objects.filter(RM_EP__in=final_list).values(*v).exclude(IS_DELETED=True).order_by("-id"))
    elif user_type == "admin" or user_type == "superadmin"  or user_type == "bo":
        data = list(Customer.objects.values(*v).exclude(IS_DELETED=True).order_by("-id"))
    # logger.info(f"count = {len(data)}")
    return JsonResponse(data,safe=False)


def customer_page(request):
    return render(request,"customer.html")

def load_customer(request):
    login_id = request.session['LOGIN_ID']
    user_type = request.session['USER_TYPE']
    user_type_id = request.session['USER_TYPE_ID']
    # if
    v = ["id","PAN_NO","C_NAME","QUALIFICATION","MOB_NO","COMP_NAME","INDUSTRY_TYPE","EMAIL","RM_EP__NAME","RM_EP__USERNAME"]
    if user_type == "bm" or user_type == "rm":
        # if user_type == "bm":
        #     mapped_rm_id_list = list(User.objects.filter(USER_TYPE="rm",RM__BRANCH=user_type_id).values_list("id",flat=True))
        #     mapped_ep_id_list = list(User.objects.filter(USER_TYPE="ep",EP__RM=user_type_id).values_list("id",flat=True))
        #     mapped_rm_ep_id_list = list(set(mapped_rm_id_list + mapped_ep_id_list))
        #     data = list(Customer.objects.filter(RM_EP__in=mapped_rm_ep_id_list).values().order_by("-id"))
        # if user_type == "rm":
        #     mapped_ep_id_list = list(User.objects.filter(USER_TYPE="ep",EP__RM=user_type_id).values_list("id",flat=True))
        #     mapped_ep_id_list.append(login_id)
            # final_id = list(set(id + mapped_ep_id_list))
        final_list = get_under_mapped(request)
        logger.info(f"final list = {final_list}")
        data = list(Customer.objects.filter(RM_EP__in=final_list).exclude(IS_DELETED=True).values(*v).order_by("-id"))
    else:
    # if user_type == "admin" or user_type == "superadmin":
        data = list(Customer.objects.values(*v).exclude(IS_DELETED=True).order_by("-id"))
    return JsonResponse({"data":data},safe=False)
# def add_insurance_customer_master(request):
#     return render(request,"add_insurance_customer_master.html")
class Add_customer(APIView):
    def get(self,request):
        context = {'customer_types':Customer_types.objects.all()}
        
        return render(request,"add_customer.html",context)
    def post(self,request):
        try:
            # user_id = request.session['USER_TYPE_ID']
            # user_type = request.session['USER_TYPE']
            pan_no                  = request.POST.get("pan_no")
            aadhaar_no              = request.POST.get("aadhaar_no")
            cust_name               = request.POST.get("cust_name")
            m_name                  = request.POST.get("m_name")
            f_name                  = request.POST.get("f_name")
            cust_dob                = request.POST.get("cust_dob")
            qualification           = request.POST.get("qualification")
            mob_no                  = request.POST.get("mob_no")
            comp_name               = request.POST.get("comp_name")
            industry_type           = request.POST.get("industry_type")
            annual_ctc              = request.POST.get("annual_ctc")
            height                  = request.POST.get("height")
            weight                  = request.POST.get("weight")
            email                   = request.POST.get("email")
            tobacco_user            = request.POST.get("tobacco_user")
            tobacco_qty             = request.POST.get("tobacco_qty")
            tobacco_consume         = request.POST.get("tobacco_consume")
            alcohol_user            = request.POST.get("alcohol_user")
            alcohol_qty             = request.POST.get("alcohol_qty")
            alcohol_consume         = request.POST.get("alcohol_consume")
            medical_history         = request.POST.get("medical_history")
            medical_dtl             = request.POST.get("medical_dtl")
            old_comp_name           = request.POST.get("old_comp_name")
            sum_assured             = request.POST.get("sum_assured")
            nominee_name            = request.POST.get("nominee_name")
            nominee_dob             = request.POST.get("nominee_dob")
            relationship            = request.POST.get("relationship")
            marital_status          = request.POST.get("marital_status")
            vaccination_img         = request.FILES.get("vaccination_img")
            pan_img                 = request.FILES.get("pan_img")
            aadhar_img              = request.FILES.get("aadhar_img")
            cc_img                  = request.FILES.get("cc_img")
            profile_img             = request.FILES.get("profile_img")
            last_edu                = request.FILES.get("last_edu")
            salaryslip_img          = request.FILES.get("salaryslip_img")
            combine_document        = request.FILES.get("combine_document")
            customer_types          = request.POST.getlist("customer_types")

            user_type               = request.POST.get("u_type")
            user                    = request.POST.get("user")
            ut                      = User.objects.get(id=user)
            user_id                 = ut.USER_ID

            # USER_ID
            logger.info(f"""
            user_type = {user_type}
            user = {user}
            ut = {ut}
            pan_no = {pan_no}
            aadhaar_no = {aadhaar_no}
            cust_name = {cust_name}
            m_name = {m_name}
            f_name = {f_name}
            cust_dob = {cust_dob}
            qualification = {qualification}
            mob_no = {mob_no}
            comp_name = {comp_name}
            industry_type = {industry_type}
            annual_ctc = {annual_ctc}
            height = {height}
            weight = {weight}
            email = {email}
            tobacco_user = {tobacco_user}
            tobacco_qty = {tobacco_qty}
            tobacco_consume = {tobacco_consume}
            alcohol_user = {alcohol_user}
            alcohol_qty = {alcohol_qty}
            alcohol_consume = {alcohol_consume}
            medical_history = {medical_history}
            medical_dtl = {medical_dtl}
            old_comp_name = {old_comp_name}
            sum_assured = {sum_assured}
            nominee_name = {nominee_name}
            nominee_dob = {nominee_dob}
            relationship = {relationship}
            marital_status = {marital_status}
            vaccination_img = {vaccination_img}
            pan_img = {pan_img}
            aadhar_img = {aadhar_img}
            cc_img = {cc_img}
            profile_img = {profile_img}
            last_edu = {last_edu}
            salaryslip_img = {salaryslip_img}
            combine_document = {combine_document}
            customer_types = {customer_types}
            """)
            if Customer.objects.filter(PAN_NO = pan_no).exclude(IS_DELETED=True).exists():
                return JsonResponse({"error":"This Pan Card details is already exists"},status=412)
            else:
                add = Customer.objects.create(
                    RM_EP           = ut,
                    PAN_NO          = pan_no,
                    AADHAAR_NO      = aadhaar_no,
                    C_NAME          = cust_name ,
                    M_NAME          = m_name ,
                    F_NAME          = f_name ,
                    TYPE            = user_type,
                    QUALIFICATION   = qualification ,
                    MOB_NO          = mob_no ,
                    COMP_NAME       = comp_name ,
                    INDUSTRY_TYPE   = industry_type ,
                    ANNUAL_CTC      = annual_ctc ,
                    HEIGHT          = height ,
                    WEIGHT          = weight ,
                    EMAIL           = email ,
                    OLD_COMP_NAME   = old_comp_name ,
                    SUM_ASSURED     = sum_assured ,
                    NOMINEE_NAME    = nominee_name ,
                    
                    RELATIONSHIP    = relationship ,
                    MARITAL_STATUS  = marital_status ,                
                    CUSTOMER_TYPES  = ",".join(customer_types),
                    CREATED_BY = User.objects.get(id=request.session['LOGIN_ID'])
                )
                if cust_dob != "":
                    add.CUST_DOB = cust_dob

                if nominee_dob != "":
                    add.NOMINEE_DOB = nominee_dob

                if vaccination_img is not None:
                    add.VACCINATION_IMG = vaccination_img

                if pan_img is not None:
                    add.PAN_IMG = pan_img

                if aadhar_img is not None:
                    add.AADHAR_IMG = aadhar_img
                
                if cc_img is not None:
                    add.CC_IMG = cc_img
                
                if profile_img is not None:
                    add.PROFILE_IMG = profile_img

                if last_edu is not None:
                    add.LAST_EDU = last_edu

                if salaryslip_img is not None:
                    add.SALARYSLIP_IMG = salaryslip_img

                if combine_document is not None:
                    add.COMBINE_DOC = combine_document

                if user_type == "bm":
                    add.BM = Branch_Manager.objects.get(id=user_id)
                if user_type == "rm":
                    add.RM = Relationship_Manager.objects.get(id=user_id)
                if user_type == "ep":
                    add.EP = Easy_Partner.objects.get(id=user_id)

                if tobacco_user == "yes":
                    add.TOBACCO_USER = True
                    add.TOBACCO_QTY = tobacco_qty
                    add.TOBACCO_CONSUME = tobacco_consume
                else:
                    add.TOBACCO_QTY = ""
                    add.TOBACCO_CONSUME = ""

                if alcohol_user == "yes":
                    add.ALCOHOL_USER = True
                    add.ALCOHOL_QTY = alcohol_qty
                    add.ALCOHOL_CONSUME = alcohol_consume
                else:
                    add.ALCOHOL_QTY = ""
                    add.ALCOHOL_CONSUME = ""

                if medical_history == "yes":
                    add.MEDICAL_HISTORY = True
                    add.MEDICAL_DTL = medical_dtl
                else:
                    add.MEDICAL_DTL = ""

                add.save()
                messages.success(request,"Customer Add successfully")
                return JsonResponse({"message":"Customer Add successfully"},status=200)
            # return redirect("/insurance_customer")
        except Exception as e:
            messages.error(request,"Something went wrong")
            logger.exception(f"{e}")
            return JsonResponse({"error":f"{e}"},status=500)
            # return redirect("/add_insurance_customer_master")
            # return JsonResponse({"error":"something went wong"},status=200)

@api_view(['POST'])
def update_insurance(request):
    try:
        id                      = request.POST.get("inputid")
        print(id)
        get_details = New_Insurance.objects.filter(id=21)
        get_details.update(VEHICLE_REGISTRATION_NUMBER = '1234')
        #print(get_details.update())
        pan_no                  = request.POST.get("pan")
        # aadhaar_no              = request.POST.get("aadhaar_no")
        cust_name               = request.POST.get("client_name")
        # m_name                  = request.POST.get("m_name")
        # f_name                  = request.POST.get("f_name")
        cust_dob                = request.POST.get("date_of_birth")
        # qualification           = request.POST.get("qualification")
        mob_no                  = request.POST.get("mobile")
        # comp_name               = request.POST.get("comp_name")
        # industry_type           = request.POST.get("industry_type")
        # annual_ctc              = request.POST.get("annual_ctc")
        height                  = request.POST.get("height")
        weight                  = request.POST.get("weight")
        email                   = request.POST.get("email")
        

        user_type               = request.POST.get("u_type")
        #user                    = request.POST.get("user")
        #ut                      = User.objects.get(id=user)
        # user_id                 = ut.USER_ID

        type_insurance          = request.POST.get("type_insurance")
        number_of_insured       = request.POST.get("number_of_insured")
        insurance_name          = request.POST.get("insurance_name")
        plan_name               = request.POST.get("plan_name")
        pb                      = request.POST.get("pb")
        insurance_product       = request.POST.get("insurance_product")
        mode                    = request.POST.get("mode")
        sub_mode                = request.POST.get("sub_mode")
        pt                      = request.POST.get("pt")
        ppt                     = request.POST.get("ppt")
        start_date              = request.POST.get("start_date")
        maturity_date           = request.POST.get("maturity_date")
        renewal_date            = request.POST.get("renewal_date")
        sum_assured             = request.POST.get("sum_assured")
        policy_number           = request.POST.get("policy_number")
        policy_pdf              = request.FILES.get("policy_pdf")
        rc_copy_pdf                = request.FILES.get("rc_copy_pdf")
        old_insurance_policy_pdf   = request.FILES.get("old_insurance_policy_pdf")
        net_premium             = request.POST.get("net_premium")
        commission              = request.POST.get("commission")
        commission_amt          = request.POST.get("commission_amt")
        
        number_of_insured_list = []
        number_of_insured_dob_list = []
        vehical_input_list = []
        number_of_years = []
        
        
        if number_of_insured is not None:
            number_of_insured       = int(request.POST.get("number_of_insured"))

        
        if number_of_insured is not None:
            for i in range(1, number_of_insured+1):
                life_to_be_insured = request.POST.get("life_to_be_insured"+str(i))
                life_to_be_insured_DOB = request.POST.get("insured_date_input"+str(i))
                number_of_insured_list.append(life_to_be_insured)
                number_of_insured_dob_list.append(life_to_be_insured_DOB)
        print(number_of_insured_list)
        print(number_of_insured_dob_list)
        if type_insurance == "13":
            for i in range(0, 5):
                vehical_input = request.POST.get("vehical_input"+str(i))
                vehical_input_list.append(vehical_input)
        print(vehical_input_list)

        if type_insurance == "15":
            travel_date = request.POST.get("travel_date")
            travel_location = request.POST.get("travel_location")
            travel_product = request.POST.get('travel_product_input')

        # if type_insurance == "12":
        policy_first_inception_date = request.POST.get("policy_first_inception_date")
        print(pb)
        # if ppt is None:
        #     for i in range(2, int(pt)+1):
        #         print(i)
        #         future_commission = request.POST.get("future_commission"+str(i))
        #         number_of_years.append(future_commission)
        # if ppt is not None:
        #     for i in range(2, int(ppt)+1):
        #         print(i)
        #         future_commission = request.POST.get("future_commission"+str(i))
        #         number_of_years.append(future_commission)
        print(number_of_years)
        print(len(number_of_insured_list))
        print(len(number_of_insured_dob_list))
        print(maturity_date, renewal_date)
        
        if type_insurance == '11' or type_insurance == '12':
            update_add = New_Insurance.objects.filter(id=id).update(
            TYPE_INSURANCE = type_insurance,
            INSURANCE_COMPANY_NAME=insurance_name,
            INSURANCE_NAME=plan_name,
            NUMBER_OF_INSURED = number_of_insured,
            POLICY_BROKER = pb,
            LIFE_TO_INSURED_ONE=number_of_insured_list[0] if len(number_of_insured_list) >= 1 else None,
            LIFE_TO_INSURED_DOB_ONE = datetime.strptime(number_of_insured_dob_list[0], "%Y-%m-%d").date() if len(number_of_insured_dob_list) >=1 else None,
            LIFE_TO_INSURED_TWO = number_of_insured_list[1] if len(number_of_insured_list) >= 2 else None,
            LIFE_TO_INSURED_DOB_TWO =datetime.strptime(number_of_insured_dob_list[1], "%Y-%m-%d").date() if len(number_of_insured_dob_list) >=2 else None,
            LIFE_TO_INSURED_THREE = number_of_insured_list[2] if len(number_of_insured_list) >= 3 else None,
            LIFE_TO_INSURED_DOB_THREE = datetime.strptime(number_of_insured_dob_list[2], "%Y-%m-%d").date() if len(number_of_insured_dob_list) >=3 else None,
            LIFE_TO_INSURED_FOUR = number_of_insured_list[3] if len(number_of_insured_list) == 4 else None,
            LIFE_TO_INSURED_DOB_FOUR = datetime.strptime(number_of_insured_dob_list[3], "%Y-%m-%d").date() if len(number_of_insured_dob_list) ==4 else None,
            PRODUCT=insurance_product,
            MODE=mode,
            SUB_MODE = sub_mode,
            PT = pt,
            PPT = ppt,
            PRODUCT_ISSUANCE_DATE = datetime.strptime(start_date, "%Y-%m-%d").date(),
            START_DATE = datetime.strptime(policy_first_inception_date, "%Y-%m-%d").date() if type_insurance == '12' else None,
            # sSTART_DATE = datetime.strptime(policy_first_inception_date, "%Y-%m-%d").date() if type_insurance == "12" else datetime.strptime(None, "%Y-%m-%d").date(),
            MATURITY_DATE = datetime.strptime(maturity_date, "%Y-%m-%d").date() if maturity_date is not None else None,  #datetime.strptime(03-04-2025, "%Y-%m-%d").date(),
            RENEWAL_DATE = datetime.strptime(renewal_date, "%Y-%m-%d").date(),  #datetime.strptime("03-04-2025", "%Y-%m-%d").date(),
            
            SUM_ASSURED =  sum_assured,
            POLICY_NUMBER = policy_number,
            NET_AMT = net_premium,
            GROSS_AMT = commission,
            # CUSTOMER_id = add_customer.id
            

            )
            # get_id = New_Insurance.objects.get(id=id)
        #     # add_customer.save
            
            #print(type(add.id))
            # print(type(request.POST.get("label_ppt"+)))
            # print(type(request.POST.get("future_commission"+i)))
            for i in range(2, int(ppt)+1):
                year = "Year "+str(i)
                
                amount = request.POST.get("future_commission"+str(i))
                add_ppt_year = INSURANCE_PPT_YEAR.objects.create(INSURANCE_ID = id, YEAR=year, PPT_AMOUNT=amount)
        

        if type_insurance == '13':
           
            add_vehicle = New_Insurance.objects.filter(id=id).update(
            
            TYPE_INSURANCE = type_insurance,
            INSURANCE_COMPANY_NAME=insurance_name,
            INSURANCE_NAME=plan_name,
            NUMBER_OF_INSURED = number_of_insured,
            POLICY_BROKER = pb,
            PRODUCT=insurance_product,
            MODE=mode,
            PRODUCT_ISSUANCE_DATE = datetime.strptime(start_date, "%Y-%m-%d").date(),
            # sSTART_DATE = datetime.strptime(policy_first_inception_date, "%Y-%m-%d").date() if type_insurance == "12" else datetime.strptime(None, "%Y-%m-%d").date(),
            
            RENEWAL_DATE = datetime.strptime(renewal_date, "%Y-%m-%d").date(),
            VEHICLE_REGISTRATION_NUMBER	= vehical_input_list[0],
            VEHICLE_TYPE = vehical_input_list[1],
            CHASIS_NUMBER = vehical_input_list[2],
            IDV_VALUE = vehical_input_list[3],
            VEHICLE_MODEL = vehical_input_list[4],
            POLICY_NUMBER = policy_number,
            NET_AMT = net_premium,
            GROSS_AMT = commission,
            #CUSTOMER_id = add_customer.id
            )
            
        
        if type_insurance == '14':
            
            add_sme = New_Insurance.objects.filter(id=id).update(
            TYPE_INSURANCE = type_insurance,
            INSURANCE_COMPANY_NAME=insurance_name,
            INSURANCE_NAME=plan_name,
            POLICY_BROKER = pb,
            PRODUCT=insurance_product,
            MODE=mode,
            PRODUCT_ISSUANCE_DATE = datetime.strptime(start_date, "%Y-%m-%d").date(),
            # sSTART_DATE = datetime.strptime(policy_first_inception_date, "%Y-%m-%d").date() if type_insurance == "12" else datetime.strptime(None, "%Y-%m-%d").date(),
            RENEWAL_DATE = datetime.strptime(renewal_date, "%Y-%m-%d").date(),
            POLICY_NUMBER = policy_number,
            SUM_ASSURED = sum_assured,
            NET_AMT = net_premium,
            GROSS_AMT = commission,
            #CUSTOMER_id = add_customer.id
            )
            

        if type_insurance == '15':
            
            add_travel = New_Insurance.objects.filter(id=id).update(
            TYPE_INSURANCE = type_insurance,
            INSURANCE_COMPANY_NAME=insurance_name,
            INSURANCE_NAME=plan_name,
            POLICY_BROKER = pb,
            PRODUCT=insurance_product,
            MODE=mode,
            PRODUCT_ISSUANCE_DATE = datetime.strptime(start_date, "%Y-%m-%d").date(),
            # sSTART_DATE = datetime.strptime(policy_first_inception_date, "%Y-%m-%d").date() if type_insurance == "12" else datetime.strptime(None, "%Y-%m-%d").date(),
            RENEWAL_DATE = datetime.strptime(renewal_date, "%Y-%m-%d").date(),
            TRAVEL_DATE = datetime.strptime(travel_date, "%Y-%m-%d").date(),
            TRAVEL_LOCATION = travel_location,
            TRAVEL_PRODUCT = travel_product,
            POLICY_NUMBER = policy_number,
            SUM_ASSURED = sum_assured,
            NET_AMT = net_premium,
            GROSS_AMT = commission,
            #CUSTOMER_id = add_customer.id
            )
            

        messages.success(request,"Customer updated successfully")
        return redirect("/buy_insurance")
    except Exception as e:
        messages.error(request,"Something went wrong")
        logger.exception(f"{e}")
        return JsonResponse({"error":f"{e}"},status=500)

@api_view(["POST"])
def add_insurance_and_customer(request):
    
    try:
        cust_dtl                = request.POST.get("cust_dtl")
        print(cust_dtl)
        pan_no                  = request.POST.get("pan")
        # aadhaar_no              = request.POST.get("aadhaar_no")
        cust_name               = request.POST.get("client_name")
        # m_name                  = request.POST.get("m_name")
        # f_name                  = request.POST.get("f_name")
        cust_dob                = request.POST.get("date_of_birth")
        # qualification           = request.POST.get("qualification")
        mob_no                  = request.POST.get("mobile")
        # comp_name               = request.POST.get("comp_name")
        # industry_type           = request.POST.get("industry_type")
        # annual_ctc              = request.POST.get("annual_ctc")
        height                  = request.POST.get("height")
        weight                  = request.POST.get("weight")
        email                   = request.POST.get("email")
        # tobacco_user            = request.POST.get("tobacco_user")
        # tobacco_qty             = request.POST.get("tobacco_qty")
        # tobacco_consume         = request.POST.get("tobacco_consume")
        # alcohol_user            = request.POST.get("alcohol_user")
        # alcohol_qty             = request.POST.get("alcohol_qty")
        # alcohol_consume         = request.POST.get("alcohol_consume")
        # medical_history         = request.POST.get("medical_history")
        # medical_dtl             = request.POST.get("medical_dtl")
        # old_comp_name           = request.POST.get("old_comp_name")
        # sum_assured             = request.POST.get("sum_assured")
        # nominee_name            = request.POST.get("nominee_name")
        # nominee_dob             = request.POST.get("nominee_dob")
        # relationship            = request.POST.get("relationship")
        # marital_status          = request.POST.get("marital_status")
        # vaccination_img         = request.FILES.get("vaccination_img")
        # pan_img                 = request.FILES.get("pan_img")
        # aadhar_img              = request.FILES.get("aadhar_img")
        # cc_img                  = request.FILES.get("cc_img")
        # profile_img             = request.FILES.get("profile_img")
        # last_edu                = request.FILES.get("last_edu")
        # salaryslip_img          = request.FILES.get("salaryslip_img")
        # combine_document        = request.FILES.get("combine_document")
        # customer_types          = request.POST.getlist("customer_types")

        user_type               = request.POST.get("u_type")
        user                    = request.POST.get("user")
        #ut                      = User.objects.get(id=user)
        # user_id                 = ut.USER_ID

        type_insurance          = request.POST.get("type_insurance")
        number_of_insured       = request.POST.get("number_of_insured")
        insurance_name          = request.POST.get("insurance_name")
        plan_name               = request.POST.get("plan_name")
        pb                      = request.POST.get("pb")
        insurance_product       = request.POST.get("insurance_product")
        mode                    = request.POST.get("mode")
        sub_mode                = request.POST.get("sub_mode")
        pt                      = request.POST.get("pt")
        ppt                     = request.POST.get("ppt")
        start_date              = request.POST.get("start_date")
        maturity_date           = request.POST.get("maturity_date")
        renewal_date            = request.POST.get("renewal_date")
        sum_assured             = request.POST.get("sum_assured")
        policy_number           = request.POST.get("policy_number")
        policy_pdf              = request.FILES.get("policy_pdf")
        rc_copy_pdf                = request.FILES.get("rc_copy_pdf")
        old_insurance_policy_pdf   = request.FILES.get("old_insurance_policy_pdf")
        net_premium             = request.POST.get("net_premium")
        commission              = request.POST.get("commission")
        commission_amt          = request.POST.get("commission_amt")
        print(type(number_of_insured))
        number_of_insured_list = []
        number_of_insured_dob_list = []
        vehical_input_list = []
        number_of_years = []
        print(type(type_insurance))
        print(pan_no)
        
        if Customer.objects.filter(PAN_NO = pan_no).exclude(IS_DELETED=True).exists():
                return JsonResponse({"error":"This Pan Card details is already exists"},status=412)
        else:
            if cust_dtl is None:
                print('here')
                add_customer = Customer.objects.create(
                    RM_EP           = ut,
                    PAN_NO          = pan_no,
                    # AADHAAR_NO      = aadhaar_no,
                    C_NAME          = cust_name ,
                    CUST_DOB        = cust_dob,
                    # M_NAME          = m_name ,
                    # F_NAME          = f_name ,
                    TYPE            = user_type,
                    # QUALIFICATION   = qualification ,
                    MOB_NO          = mob_no ,
                    # COMP_NAME       = comp_name ,
                    # INDUSTRY_TYPE   = industry_type ,
                    # ANNUAL_CTC      = annual_ctc ,
                    HEIGHT          = height ,
                    WEIGHT          = weight ,
                    EMAIL           = email ,
                    # OLD_COMP_NAME   = old_comp_name ,
                    # SUM_ASSURED     = sum_assured ,
                    # NOMINEE_NAME    = nominee_name ,
                    
                    # RELATIONSHIP    = relationship ,
                    # MARITAL_STATUS  = marital_status ,                
                    CUSTOMER_TYPES  = "Insurance",
                    CREATED_BY = User.objects.get(id=request.session['LOGIN_ID'])
                )

        if number_of_insured is not None:
            number_of_insured       = int(request.POST.get("number_of_insured"))

        
        if number_of_insured is not None:
            for i in range(1, number_of_insured+1):
                life_to_be_insured = request.POST.get("life_to_be_insured"+str(i))
                life_to_be_insured_DOB = request.POST.get("insured_date_input"+str(i))
                number_of_insured_list.append(life_to_be_insured)
                number_of_insured_dob_list.append(life_to_be_insured_DOB)
        print(number_of_insured_list)
        print(number_of_insured_dob_list)
        if type_insurance == "13":
            for i in range(0, 5):
                vehical_input = request.POST.get("vehical_input"+str(i))
                vehical_input_list.append(vehical_input)
        print(vehical_input_list)

        if type_insurance == "15":
            travel_date = request.POST.get("travel_date")
            travel_location = request.POST.get("travel_location")
            travel_product = request.POST.get('travel_product_input')

        # if type_insurance == "12":
        policy_first_inception_date = request.POST.get("policy_first_inception_date")
        print(ppt)
        
        # if ppt is None:
        #     for i in range(2, int(pt)+1):
        #         print(i)
        #         future_commission = request.POST.get("future_commission"+str(i))
        #         number_of_years.append(future_commission)
        # if ppt is not None:
        #     for i in range(2, int(ppt)+1):
        #         print(i)
        #         future_commission = request.POST.get("future_commission"+str(i))
        #         number_of_years.append(future_commission)
        
        if type_insurance == '11' or type_insurance == '12':
            add = New_Insurance.objects.create(
            TYPE_INSURANCE = type_insurance,
            INSURANCE_COMPANY_NAME=insurance_name,
            INSURANCE_NAME=plan_name,
            NUMBER_OF_INSURED = number_of_insured,
            POLICY_BROKER = pb,
            LIFE_TO_INSURED_ONE=number_of_insured_list[0] if len(number_of_insured_list) >= 1 else None,
            LIFE_TO_INSURED_DOB_ONE = datetime.strptime(number_of_insured_dob_list[0], "%Y-%m-%d").date() if len(number_of_insured_dob_list) >=1 else None,
            LIFE_TO_INSURED_TWO = number_of_insured_list[1] if len(number_of_insured_list) >= 2 else None,
            LIFE_TO_INSURED_DOB_TWO =datetime.strptime(number_of_insured_dob_list[1], "%Y-%m-%d").date() if len(number_of_insured_dob_list) >=2 else None,
            LIFE_TO_INSURED_THREE = number_of_insured_list[2] if len(number_of_insured_list) >= 3 else None,
            LIFE_TO_INSURED_DOB_THREE = datetime.strptime(number_of_insured_dob_list[2], "%Y-%m-%d").date() if len(number_of_insured_dob_list) >=3 else None,
            LIFE_TO_INSURED_FOUR = number_of_insured_list[3] if len(number_of_insured_list) == 4 else None,
            LIFE_TO_INSURED_DOB_FOUR = datetime.strptime(number_of_insured_dob_list[3], "%Y-%m-%d").date() if len(number_of_insured_dob_list) ==4 else None,
            PRODUCT=insurance_product,
            MODE=mode,
            SUB_MODE = sub_mode,
            PT = pt,
            PPT = ppt,
            PRODUCT_ISSUANCE_DATE = datetime.strptime(start_date, "%Y-%m-%d").date(),
            START_DATE = datetime.strptime(policy_first_inception_date, "%Y-%m-%d").date() if type_insurance == '12' else None,
            # sSTART_DATE = datetime.strptime(policy_first_inception_date, "%Y-%m-%d").date() if type_insurance == "12" else datetime.strptime(None, "%Y-%m-%d").date(),
            MATURITY_DATE = datetime.strptime(maturity_date, "%Y-%m-%d").date() if maturity_date is not None else None,  #datetime.strptime(03-04-2025, "%Y-%m-%d").date(),
            RENEWAL_DATE = datetime.strptime(renewal_date, "%Y-%m-%d").date(),  #datetime.strptime("03-04-2025", "%Y-%m-%d").date(),
            
            SUM_ASSURED =  sum_assured,
            POLICY_NUMBER = policy_number,
            NET_AMT = net_premium,
            GROSS_AMT = commission,
            CUSTOMER_id = add_customer.id if cust_dtl is None else int(cust_dtl)

            )
            # add_customer.save
            add.save
            print(type(add.id))
            # print(type(request.POST.get("label_ppt"+)))
            # print(type(request.POST.get("future_commission"+i)))
            for i in range(2, int(ppt)+1):
                year = "Year "+str(i)
                
                amount = request.POST.get("future_commission"+str(i))
                add_ppt_year = INSURANCE_PPT_YEAR.objects.create(INSURANCE_ID = add.id, YEAR=year, PPT_AMOUNT=amount)
                add_ppt_year.save
        

        if type_insurance == '13':
            print('here')
            add_vehicle = New_Insurance.objects.create(
            TYPE_INSURANCE = type_insurance,
            INSURANCE_COMPANY_NAME=insurance_name,
            INSURANCE_NAME=plan_name,
            NUMBER_OF_INSURED = number_of_insured,
            POLICY_BROKER = pb,
            PRODUCT=insurance_product,
            MODE=mode,
            PRODUCT_ISSUANCE_DATE = datetime.strptime(start_date, "%Y-%m-%d").date(),
            # sSTART_DATE = datetime.strptime(policy_first_inception_date, "%Y-%m-%d").date() if type_insurance == "12" else datetime.strptime(None, "%Y-%m-%d").date(),
            
            RENEWAL_DATE = datetime.strptime(renewal_date, "%Y-%m-%d").date(),
            VEHICLE_REGISTRATION_NUMBER	= vehical_input_list[0],
            VEHICLE_TYPE = vehical_input_list[1],
            CHASIS_NUMBER = vehical_input_list[2],
            IDV_VALUE = vehical_input_list[3],
            VEHICLE_MODEL = vehical_input_list[4],
            POLICY_NUMBER = policy_number,
            NET_AMT = net_premium,
            GROSS_AMT = commission,
            #CUSTOMER_id = add_customer.id
            )
            add_vehicle.save
        
        if type_insurance == '14':
            print('here')
            add_sme = New_Insurance.objects.create(
            TYPE_INSURANCE = type_insurance,
            INSURANCE_COMPANY_NAME=insurance_name,
            INSURANCE_NAME=plan_name,
            POLICY_BROKER = pb,
            PRODUCT=insurance_product,
            MODE=mode,
            PRODUCT_ISSUANCE_DATE = datetime.strptime(start_date, "%Y-%m-%d").date(),
            # sSTART_DATE = datetime.strptime(policy_first_inception_date, "%Y-%m-%d").date() if type_insurance == "12" else datetime.strptime(None, "%Y-%m-%d").date(),
            RENEWAL_DATE = datetime.strptime(renewal_date, "%Y-%m-%d").date(),
            POLICY_NUMBER = policy_number,
            SUM_ASSURED = sum_assured,
            NET_AMT = net_premium,
            GROSS_AMT = commission,
            #CUSTOMER_id = add_customer.id
            )
            add_sme.save

        if type_insurance == '15':
            print('here')
            add_travel = New_Insurance.objects.create(
            TYPE_INSURANCE = type_insurance,
            INSURANCE_COMPANY_NAME=insurance_name,
            INSURANCE_NAME=plan_name,
            POLICY_BROKER = pb,
            PRODUCT=insurance_product,
            MODE=mode,
            PRODUCT_ISSUANCE_DATE = datetime.strptime(start_date, "%Y-%m-%d").date(),
            # sSTART_DATE = datetime.strptime(policy_first_inception_date, "%Y-%m-%d").date() if type_insurance == "12" else datetime.strptime(None, "%Y-%m-%d").date(),
            RENEWAL_DATE = datetime.strptime(renewal_date, "%Y-%m-%d").date(),
            TRAVEL_DATE = datetime.strptime(travel_date, "%Y-%m-%d").date(),
            TRAVEL_LOCATION = travel_location,
            TRAVEL_PRODUCT = travel_product,
            POLICY_NUMBER = policy_number,
            SUM_ASSURED = sum_assured,
            NET_AMT = net_premium,
            GROSS_AMT = commission,
            #CUSTOMER_id = add_customer.id
            )
            add_travel.save

        messages.success(request,"Customer Add successfully")
        return redirect("/buy_insurance")


    except Exception as e:
        messages.error(request,"Something went wrong")
        logger.exception(f"{e}")
        return JsonResponse({"error":f"{e}"},status=500)

def get_new_insurance(request, id):
    values = ['id', 'TYPE_INSURANCE', 'NUMBER_OF_INSURED', 'LIFE_TO_INSURED_ONE', 'LIFE_TO_INSURED_DOB_ONE','LIFE_TO_INSURED_TWO','LIFE_TO_INSURED_DOB_TWO', 
              'LIFE_TO_INSURED_THREE', 'LIFE_TO_INSURED_DOB_THREE', 'LIFE_TO_INSURED_FOUR', 'LIFE_TO_INSURED_DOB_FOUR', 'INSURANCE_COMPANY_NAME',
              'INSURANCE_NAME', 'INSURANCE_PERIOD', 'POLICY_BROKER', 'POLICY_FIRST_INCEPTION_DATE', 'VEHICLE_REGISTRATION_NUMBER', 'VEHICLE_TYPE',
              'CHASIS_NUMBER', 'IDV_VALUE', 'VEHICLE_MODEL', 'TRAVEL_DATE', 'TRAVEL_LOCATION', 'TRAVEL_PRODUCT', 'PRODUCT', 'MODE','SUB_MODE', 'PRODUCT_ISSUANCE_DATE',
              'START_DATE','MATURITY_DATE', 'SUM_ASSURED', 'POLICY_NUMBER', 'RENEWAL_DATE', 'PPT', 'PT','PB', 'NET_AMT', 'GROSS_AMT','COMMISSION', 'COMMISSION_AMT',
              'CUSTOMER_id']
    customer_values = ['C_NAME', 'CUST_DOB', 'MOB_NO', 'EMAIL']
    year_value = ['PPT_AMOUNT']
    data = list(New_Insurance.objects.filter(id=id).values(*values))
    year = list(INSURANCE_PPT_YEAR.objects.filter(INSURANCE_ID = id).values(*year_value))
    y = []
    for i in year:
        for j in i:
            y.append(i[j])
            
    # customer = list(Customer.objects.filter(id=data[0]['CUSTOMER_id']).values(*customer_values))
    # print(customer)
    # if customer:
    #     data[0]['CUSTOMER_DATA'] = customer
    return JsonResponse({"data":data, "year": y},safe=False)

def edit_new_insurance_page(request, id):
    login_id = request.session['LOGIN_ID']
    user_type = request.session['USER_TYPE']
    user_type_id = request.session['USER_TYPE_ID']
    type_insurance = Insurance_type_master.objects.values("id","NAME")
    pb = Policy_broker_master.objects.values("id","NAME")
    values = ['id', 'TYPE_INSURANCE', 'NUMBER_OF_INSURED', 'LIFE_TO_INSURED_ONE', 'LIFE_TO_INSURED_DOB_ONE','LIFE_TO_INSURED_TWO','LIFE_TO_INSURED_DOB_TWO', 
              'LIFE_TO_INSURED_THREE', 'LIFE_TO_INSURED_DOB_THREE', 'LIFE_TO_INSURED_FOUR', 'LIFE_TO_INSURED_DOB_FOUR', 'INSURANCE_COMPANY_NAME',
              'INSURANCE_NAME', 'INSURANCE_PERIOD', 'POLICY_BROKER', 'POLICY_FIRST_INCEPTION_DATE', 'VEHICLE_REGISTRATION_NUMBER', 'VEHICLE_TYPE',
              'CHASIS_NUMBER', 'IDV_VALUE', 'VEHICLE_MODEL', 'TRAVEL_DATE', 'TRAVEL_LOCATION', 'TRAVEL_PRODUCT', 'PRODUCT', 'MODE','SUB_MODE', 'PRODUCT_ISSUANCE_DATE',
              'START_DATE','MATURITY_DATE', 'SUM_ASSURED', 'POLICY_NUMBER', 'RENEWAL_DATE', 'PPT', 'PT','PB', 'NET_AMT', 'GROSS_AMT','COMMISSION', 'COMMISSION_AMT',
              'CUSTOMER_id']
    customer_values = ['C_NAME', 'CUST_DOB', 'MOB_NO', 'EMAIL']
    data = New_Insurance.objects.get(id=id)
    fixed_type_insurance = Insurance_type_master.objects.get(id=data.TYPE_INSURANCE)
    fixed_pb =  Policy_broker_master.objects.get(id=data.POLICY_BROKER)
    customer = Customer.objects.get(id=data.CUSTOMER_id)
    if data.MODE == '1':
        mode = { 'id': '1','NAME':'Monthly'}
    if data.MODE == '3':
        mode = { 'id': '3','NAME':'Quarterly'}
    if data.MODE == '6':
        mode = { 'id': '6','NAME':'Half Annually'}
    if data.MODE == '12':
        mode = { 'id': '6','NAME':'Annually'}
    
    print(type(customer))
    return render(request,"edit_new_insurance.html",context={"type_insurance":type_insurance, "customer": customer, "data":data,"pb":pb, "fixed_type_insurance": fixed_type_insurance, 'fixed_pb': fixed_pb, 'mode': mode})

class Edit_customer(APIView):
    def get(self,request,id):
        customer_types = Customer_types.objects.all()
        data = Customer.objects.get(id=id)
        return render(request,"edit_customer.html",context={"data":data,"customer_types":customer_types})
    def post(self,request,id):
        try:
            pan_no = request.POST.get("pan_no")
            aadhaar_no = request.POST.get("aadhaar_no")
            cust_name = request.POST.get("cust_name")
            m_name = request.POST.get("m_name")
            f_name = request.POST.get("f_name")
            cust_dob = request.POST.get("cust_dob")
            qualification = request.POST.get("qualification")
            mob_no = request.POST.get("mob_no")
            comp_name = request.POST.get("comp_name")
            industry_type = request.POST.get("industry_type")
            annual_ctc = request.POST.get("annual_ctc")
            height = request.POST.get("height")
            weight = request.POST.get("weight")
            email = request.POST.get("email")
            tobacco_user = request.POST.get("tobacco_user")
            tobacco_qty = request.POST.get("tobacco_qty")
            tobacco_consume = request.POST.get("tobacco_consume")
            alcohol_user = request.POST.get("alcohol_user")
            alcohol_qty = request.POST.get("alcohol_qty")
            alcohol_consume = request.POST.get("alcohol_consume")
            medical_history = request.POST.get("medical_history")
            medical_dtl = request.POST.get("medical_dtl")
            old_comp_name = request.POST.get("old_comp_name")
            sum_assured = request.POST.get("sum_assured")
            nominee_name = request.POST.get("nominee_name")
            nominee_dob = request.POST.get("nominee_dob")
            relationship = request.POST.get("relationship")
            marital_status = request.POST.get("marital_status")
            vaccination_img = request.FILES.get("vaccination_img")
            pan_img = request.FILES.get("pan_img")
            aadhar_img = request.FILES.get("aadhar_img")
            cc_img = request.FILES.get("cc_img")
            profile_img = request.FILES.get("profile_img")
            last_edu = request.FILES.get("last_edu")
            salaryslip_img = request.FILES.get("salaryslip_img")
            combine_document = request.FILES.get("combine_document")
            customer_types = request.POST.getlist("customer_types")

            user_type = request.POST.get("u_type")
            # user = request.POST.get("user")
            # ut = User.objects.get(id=user)
            # user_id = ut.USER_ID
            # user = {user}
            # ut = {ut}
            logger.info(f"""
            user_type = {user_type}
           
            pan_no = {pan_no}
            aadhaar_no = {aadhaar_no}
            cust_name = {cust_name}
            m_name = {m_name}
            f_name = {f_name}
            cust_dob = {cust_dob}
            qualification = {qualification}
            mob_no = {mob_no}
            comp_name = {comp_name}
            industry_type = {industry_type}
            annual_ctc = {annual_ctc}
            height = {height}
            weight = {weight}
            email = {email}
            tobacco_user = {tobacco_user}
            tobacco_qty = {tobacco_qty}
            tobacco_consume = {tobacco_consume}
            alcohol_user = {alcohol_user}
            alcohol_qty = {alcohol_qty}
            alcohol_consume = {alcohol_consume}
            medical_history = {medical_history}
            medical_dtl = {medical_dtl}
            old_comp_name = {old_comp_name}
            sum_assured = {sum_assured}
            nominee_name = {nominee_name}
            nominee_dob = {nominee_dob}
            relationship = {relationship}
            marital_status = {marital_status}
            vaccination_img = {vaccination_img}
            pan_img = {pan_img}
            aadhar_img = {aadhar_img}
            cc_img = {cc_img}
            profile_img = {profile_img}
            last_edu = {last_edu}
            salaryslip_img = {salaryslip_img}
            combine_document = {combine_document}
            customer_types = {customer_types}
            """)
            if Customer.objects.filter(PAN_NO = pan_no).exclude(id=id).exclude(IS_DELETED=True).exists():
                return JsonResponse({"error":"This Pan Card details is already exists"},status=412)
            else:
                edit = Customer.objects.get(id=id)
                # edit.RM_EP = ut
                # edit.TYPE = user_type
                # if user_type == "rm":
                #     edit.RM = Relationship_Manager.objects.get(id=user_id)
                # if user_type == "ep":
                #     edit.EP = Easy_Partner.objects.get(id=user_id)

                edit.PAN_NO = pan_no
                edit.AADHAAR_NO = aadhaar_no
                edit.C_NAME = cust_name
                edit.M_NAME = m_name
                edit.F_NAME = f_name
                edit.CUST_DOB = cust_dob
                edit.QUALIFICATION = qualification
                edit.MOB_NO = mob_no
                edit.COMP_NAME = comp_name
                edit.INDUSTRY_TYPE = industry_type
                edit.ANNUAL_CTC = annual_ctc
                edit.HEIGHT = height
                edit.WEIGHT = weight
                edit.EMAIL = email
                edit.OLD_COMP_NAME = old_comp_name
                edit.SUM_ASSURED = sum_assured
                edit.NOMINEE_NAME = nominee_name
                if nominee_dob != "":
                    edit.NOMINEE_DOB = nominee_dob
                edit.RELATIONSHIP = relationship
                edit.MARITAL_STATUS = marital_status
                edit.CUSTOMER_TYPES = ",".join(customer_types)
                edit.MODIFIED_BY = User.objects.get(id=request.session['LOGIN_ID'])
                
                if vaccination_img is not None:
                    edit.VACCINATION_IMG = vaccination_img

                if pan_img is not None:
                    edit.PAN_IMG = pan_img

                if aadhar_img is not None:
                    edit.AADHAR_IMG = aadhar_img
                
                if cc_img is not None:
                    edit.CC_IMG = cc_img
                
                if profile_img is not None:
                    edit.PROFILE_IMG = profile_img

                if last_edu is not None:
                    edit.LAST_EDU = last_edu

                if salaryslip_img is not None:
                    edit.SALARYSLIP_IMG = salaryslip_img

                if combine_document is not None:
                    edit.COMBINE_DOC = combine_document
                

                if tobacco_user == "yes":
                    edit.TOBACCO_USER = True
                    edit.TOBACCO_QTY = tobacco_qty
                    edit.TOBACCO_CONSUME = tobacco_consume
                else:
                    edit.TOBACCO_USER = False
                    edit.TOBACCO_QTY = ""
                    edit.TOBACCO_CONSUME = ""

                if alcohol_user == "yes":
                    edit.ALCOHOL_USER = True
                    edit.ALCOHOL_QTY = alcohol_qty
                    edit.ALCOHOL_CONSUME = alcohol_consume
                else:
                    edit.ALCOHOL_USER = False
                    edit.ALCOHOL_QTY = ""
                    edit.ALCOHOL_CONSUME = ""

                if medical_history == "yes":
                    edit.MEDICAL_HISTORY = True
                    edit.MEDICAL_DTL = medical_dtl
                else:
                    edit.MEDICAL_HISTORY = False
                    edit.MEDICAL_DTL = ""
                
                edit.save()
                messages.success(request,"Customer Edit successfully")
                return JsonResponse({"message":"Customer Edit successfully"},status=200)
                # return redirect(f"/insurance_customer")
        except Exception as e:
            messages.error(request,"Something went wrong")
            logger.exception(f"{e}")
            return JsonResponse({"error":f"{e}"},status=500)
            # return redirect(f"/edit_insurnace_customer/{id}")
            # return JsonResponse({"error":"something went wong"},status=200)

def insurance_page(request):
    return render(request,"insurance.html")

def insurance_alert_page(request):
    return render(request,"insurance_alert.html")


def load_new_insurance(request):
    
    # login_id = request.session['LOGIN_ID']
    # user_type = request.session['USER_TYPE']
    # #user_type_id = request.session['USER_TYPE_ID']
    values = ["id","TYPE_INSURANCE","NUMBER_OF_INSURED","INSURANCE_PERIOD","PRODUCT_ISSUANCE_DATE","RENEWAL_DATE","CUSTOMER_id"]
    
    
    data = list(New_Insurance.objects.all().values(*values).order_by('-id'))
    # print(data)
    # data[2]['CUSTOMER_DATA'] = 'Vasant'
    for i in data:
        
        
        if i['TYPE_INSURANCE'] == '11':
            i['TYPE_INSURANCE'] = 'Life Insurance'
        if i['TYPE_INSURANCE'] == '12':
            i['TYPE_INSURANCE'] = 'Health Insurance'
        if i['TYPE_INSURANCE'] == '13':
            i['TYPE_INSURANCE'] = 'Vehicle'
        if i['TYPE_INSURANCE'] == '14':
            i['TYPE_INSURANCE'] = 'SME'
        if i['TYPE_INSURANCE'] == '15':
            i['TYPE_INSURANCE'] = 'Travel'
        customer_data = list(Customer.objects.filter(id=i['CUSTOMER_id']).values('RM_EP_id', 'PAN_NO', 'C_NAME', 'MOB_NO', 'EMAIL'))
        
        
        if customer_data:
            print(i)
            i['CUSTOMER_DATA'] = customer_data[0]
            rm_ep_data = list(Relationship_Manager.objects.filter(LOGIN_id = customer_data[0]['RM_EP_id']).values('NAME','EMAIL'))
            i['EP_RM_DATA'] = rm_ep_data[0]
        
    # from_date   = request.GET.get("from_date")
    # to_date     = request.GET.get("to_date")

    # if user_type == "bm" or user_type == "rm":
    #     #final_list = get_under_mapped(request)
        
    #     data = list(New_Insurance.objects.all())
    #     print(data)
    #     # data = list(New_Insurance.objects.filter(CUSTOMER__RM_EP__in=final_list).values(*values).order_by("-id"))
    # elif user_type == "admin" or user_type == "superadmin":
        
    #     data = list(New_Insurance.objects.all())
    #     print(data)
    return JsonResponse({"data": data},safe=False)

def load_insurance(request):
    login_id = request.session['LOGIN_ID']
    user_type = request.session['USER_TYPE']
    user_type_id = request.session['USER_TYPE_ID']
    values = ["id","CUSTOMER__C_NAME","CUSTOMER__MOB_NO","TYPE_INSURANCE__NAME","INSURANCE_NAME","INSURANCE_PERIOD","START_DATE","RENEWAL_DATE","CUSTOMER__RM_EP__USERNAME","CUSTOMER__RM_EP__NAME"]
    
    from_date   = request.GET.get("from_date")
    to_date     = request.GET.get("to_date")
    # if user_type =="bm":
    #     mapped_rm_id_list = list(User.objects.filter(USER_TYPE="rm",RM__BRANCH=user_type_id).values_list("id",flat=True))
    #     mapped_ep_id_list = list(User.objects.filter(USER_TYPE="ep",EP__RM=user_type_id).values_list("id",flat=True))
    #     final_list = list(set(mapped_rm_id_list + mapped_ep_id_list))
    #     data = list(Insurance.objects.filter(CUSTOMER__RM_EP__in=final_list).values(*values).order_by("-id"))
    # elif user_type == "rm":
    #     mapped_ep_id_list = list(User.objects.filter(USER_TYPE="ep",EP__RM=user_type_id).values_list("id",flat=True))
    #     mapped_ep_id_list.append(login_id)
    #     final_list = mapped_ep_id_list
    #     data = list(Insurance.objects.filter(CUSTOMER__RM_EP__in=final_list).values(*values).order_by("-id"))
    date_kwargs = {}
    if from_date is not None and from_date != "":
        date_kwargs['RENEWAL_DATE__range'] = (from_date,to_date)
    
    if user_type == "bm" or user_type == "rm":
        final_list = get_under_mapped(request)
        data = list(Insurance.objects.filter(CUSTOMER__RM_EP__in=final_list,**date_kwargs).values(*values).order_by("-id"))
    elif user_type == "admin" or user_type == "superadmin":
        data = list(Insurance.objects.filter(**date_kwargs).values(*values).order_by("-id"))
    return JsonResponse({"data":data},safe=False)

def load_alert_insurance(request):
    today = date.today()
    month = today.strftime('%m')
    data = list(Insurance.objects.filter(RENEWAL_DATE__month = month).values("id","CUSTOMER__C_NAME","CUSTOMER__MOB_NO","TYPE_INSURANCE__NAME","INSURANCE_NAME","INSURANCE_PERIOD","START_DATE","RENEWAL_DATE").order_by("-id"))
    return JsonResponse({"data":data},safe=False)

class add_insurance_alert(APIView):
    def get(self,request):
        login_id = request.session['LOGIN_ID']
        user_type = request.session['USER_TYPE']
        user_type_id = request.session['USER_TYPE_ID']
        type_insurance = Insurance_type_master.objects.values("id","NAME")
        pb = Policy_broker_master.objects.values("id","NAME")
        user = User.objects.all()
        
        # if request.session['USER_TYPE'] == "bm":
        #     mapped_rm_id_list = list(User.objects.filter(USER_TYPE="rm",RM__BRANCH=user_type_id).values_list("id",flat=True))
        #     mapped_ep_id_list = list(User.objects.filter(USER_TYPE="ep",EP__RM=user_type_id).values_list("id",flat=True))
        #     final_list = list(set(mapped_rm_id_list + mapped_ep_id_list))
        #     logger.info(f"bm final list = {final_list}")
        #     data = Customer.objects.filter(RM_EP__in=final_list).values("id","C_NAME","MOB_NO").order_by("-id")
        # elif request.session['USER_TYPE'] == "rm":
        #     mapped_ep_id_list = list(User.objects.filter(USER_TYPE="ep",EP__RM=user_type_id).values_list("id",flat=True))
        #     mapped_ep_id_list.append(login_id)
        #     final_list = mapped_ep_id_list
        #     logger.info(f"rm final list = {final_list}")
        #     data = Customer.objects.filter(RM_EP__in=final_list).values("id","C_NAME","MOB_NO").order_by("-id")
        v = ["id","C_NAME","MOB_NO","PAN_NO"]
        if user_type == "bm" or user_type == "rm":
            final_list = get_under_mapped(request)
            # logger.info(f"final_list = {final_list}")
            data = Customer.objects.filter(RM_EP__in=final_list).values(*v).exclude(IS_DELETED=True).order_by("-id")
        elif request.session['USER_TYPE'] == "admin" or request.session['USER_TYPE'] == "superadmin":
            data = Customer.objects.values(*v).exclude(IS_DELETED=True).order_by("-id")
        return render(request,"add_insurance_alert.html",context={"data":data,"type_insurance":type_insurance,"pb":pb, "user": user})
    def post(self,request):
        try:
            cust_dtl = request.POST.get("cust_dtl")
            type_insurance = request.POST.get("type_insurance")
            insurance_name = request.POST.get("insurance_name")
            period = request.POST.get("period")
            start_date = request.POST.get("start_date")
            ppt = request.POST.get("ppt")
            pt = request.POST.get("pt")
            pb = request.POST.get("pb")
            net_premium = request.POST.get("net_premium")
            gross_premium = request.POST.get("gross_premium")
            commission = request.POST.get("commission")
            commission_amt = request.POST.get("commission_amt")

            logger.info(f"""
                cust_dtl = {cust_dtl}
                type_insurance = {type_insurance}
                insurance_name = {insurance_name}
                period = {period}
                start_date = {start_date}
                ppt = {ppt}
                pt = {pt}
                pb = {pb}
                net_premium = {net_premium}
                gross_premium = {gross_premium}
                commission = {commission}
                commission_amt = {commission_amt}
            """)
            
            new_start_date = datetime.strptime(start_date, "%Y-%m-%d").date()
            renewal_date = new_start_date + relativedelta(months = int(period)) 
            add = Insurance.objects.create(
                CUSTOMER = Customer.objects.get(id = cust_dtl) ,
                TYPE_INSURANCE = Insurance_type_master.objects.get(id = type_insurance) ,
                INSURANCE_NAME  = insurance_name ,
                INSURANCE_PERIOD = period ,
                START_DATE = start_date ,
                RENEWAL_DATE = renewal_date,
                PPT = ppt ,
                PT = pt ,
                PB = Policy_broker_master.objects.get(id = pb) ,
                NET_AMT = net_premium ,
                GROSS_AMT = gross_premium ,
                COMMISSION = commission ,
                COMMISSION_AMT = commission_amt ,
                CREATED_BY = User.objects.get(id=request.session['LOGIN_ID'])
            )
            logger.info(f"expiry_date = {renewal_date}")
            messages.success(request,"Insurance Alert Add successfully")
            #get previous url fpr redirect
            return redirect(f"/buy_insurance")
        except Exception as e:
            messages.error(request,"Something went wrong")
            logger.exception(f"{e}")
            return redirect(f"/add_insurance_alert")

def get_insurance(request,id):
    a = Insurance.objects.filter(id=id)
    data = list(a.values())
    data[0]['CUSTOMER_NAME'] = a[0].CUSTOMER.C_NAME
    data[0]['CUSTOMER__RM_EP__NAME'] = a[0].CUSTOMER.RM_EP.NAME
    data[0]['PB_NAME'] = a[0].PB.NAME
    data[0]['TYPE_INSURANCE_NAME'] = a[0].TYPE_INSURANCE.NAME

    return JsonResponse(data,safe=False,status=200)

class edit_insurance_alert(APIView):
    def get(self,request,id):
        login_id = request.session['LOGIN_ID']
        user_type = request.session['USER_TYPE']
        user_type_id = request.session['USER_TYPE_ID']
        type_insurance = Insurance_type_master.objects.values("id","NAME")
        pb = Policy_broker_master.objects.values("id","NAME")
        data = Customer.objects.values("id","C_NAME","MOB_NO")
        ialert = Insurance.objects.get(id=id)
        # if request.session['USER_TYPE'] == "bm":
        #     mapped_rm_id_list = list(User.objects.filter(USER_TYPE="rm",RM__BRANCH=user_type_id).values_list("id",flat=True))
        #     mapped_ep_id_list = list(User.objects.filter(USER_TYPE="ep",EP__RM=user_type_id).values_list("id",flat=True))
        #     final_list = list(set(mapped_rm_id_list + mapped_ep_id_list))
        #     logger.info(f"bm final list = {final_list}")
        #     data = Customer.objects.filter(RM_EP__in=final_list).values("id","C_NAME","MOB_NO").order_by("-id")
        # elif request.session['USER_TYPE'] == "rm":
        #     mapped_ep_id_list = list(User.objects.filter(USER_TYPE="ep",EP__RM=user_type_id).values_list("id",flat=True))
        #     mapped_ep_id_list.append(login_id)
        #     final_list = mapped_ep_id_list
        #     logger.info(f"rm final list = {final_list}")
        #     data = Customer.objects.filter(RM_EP__in=final_list).values("id","C_NAME","MOB_NO").order_by("-id")
        if user_type == "bm" or user_type == "rm":
            final_list = get_under_mapped(request)
            # logger.info(f"final_list = {final_list}")
            data = Customer.objects.filter(RM_EP__in=final_list).values("id","C_NAME","MOB_NO").order_by("-id")
        elif request.session['USER_TYPE'] == "admin" or request.session['USER_TYPE'] == "superadmin":
            data = Customer.objects.values("id","C_NAME","MOB_NO").order_by("-id")
        return render(request,"edit_insurance_alert.html",context={"data":data,"type_insurance":type_insurance,"ialert":ialert,"pb":pb})
    def post(self,request,id):
        try:
            cust_dtl = request.POST.get("cust_dtl")
            type_insurance = request.POST.get("type_insurance")
            insurance_name = request.POST.get("insurance_name")
            period = request.POST.get("period")
            start_date = request.POST.get("start_date")
            ppt = request.POST.get("ppt")
            pt = request.POST.get("pt")
            pb = request.POST.get("pb")
            net_premium = request.POST.get("net_premium")
            gross_premium = request.POST.get("gross_premium")
            commission = request.POST.get("commission")
            commission_amt = request.POST.get("commission_amt")

            logger.info(f"""
                cust_dtl = {cust_dtl}
                type_insurance = {type_insurance}
                insurance_name = {insurance_name}
                period = {period}
                start_date = {start_date}
                ppt = {ppt}
                pt = {pt}
                pb = {pb}
                net_premium = {net_premium}
                gross_premium = {gross_premium}
                commission = {commission}
                commission_amt = {commission_amt}
            """)
            
            

            new_start_date = datetime.strptime(start_date, "%Y-%m-%d").date()
            renewal_date = new_start_date + relativedelta(months = int(period)) 
            edit = Insurance.objects.get(id=id)
            # logger.info(f"start_date = {start_date} available start date {edit.START_DATE}")
            # edit.CUSTOMER = Customer.objects.get(id = cust_dtl)
            # if new_start_date != edit.START_DATE :
            #     u_d = Update_insurance_alert.objects.create(
            #     INSURACE = edit,
            #     INSURANCE_PERIOD = edit.INSURANCE_PERIOD,
            #     START_DATE = edit.START_DATE,
            #     RENEWAL_DATE = edit.RENEWAL_DATE,
            #     )

            #     logger.info(f"Start date and end date Not same")
            # else:
            #     logger.info(f"Start date and end date same")


            # edit.CUSTOMER = Customer.objects.get(id = cust_dtl)
            edit.TYPE_INSURANCE = Insurance_type_master.objects.get(id = type_insurance)
            edit.INSURANCE_NAME  = insurance_name
            edit.INSURANCE_PERIOD = period
            edit.START_DATE = start_date
            edit.RENEWAL_DATE = renewal_date
            edit.PPT = ppt
            edit.PT = pt
            edit.PB = Policy_broker_master.objects.get(id = pb)
            edit.NET_AMT = net_premium
            edit.GROSS_AMT = gross_premium
            edit.COMMISSION = commission
            edit.COMMISSION_AMT = commission_amt
            edit.MODIFIED_BY = User.objects.get(id=request.session['LOGIN_ID'])
            edit.save()
            logger.info(f"expiry_date = {renewal_date}")
            messages.success(request,"Insurance Alert Edit successfully")
            return redirect(f"/buy_insurance")
        except Exception as e:
            messages.error(request,"Something went wrong")
            logger.exception(f"{e}")
            return redirect(f"/edit_insurance_alert/{id}")

def delete_insurance_alert(request,id):
    try:
        Insurance.objects.get(id=id).delete()
        return JsonResponse({"message":"Insurance Record Deleted successfully"},status=200)
    except Exception as e:
        messages.error(request,"Something went wrong")
        logger.exception(f"{e}")
        return JsonResponse({"error":f"{e}"},safe=False,status=500)

def insurance_alert_crontab():
    try:
        logger.info(f"enter insurance")
        today_date = date.today()
        data =  Insurance.objects.all()
        for i in data:
            r_date = i.RENEWAL_DATE
            r_day = r_date - today_date
            r_day = r_day.days
            if r_day == 20 :
                logger.info(f"21 days remaining {i.CUSTOMER.C_NAME} | {i.CUSTOMER.MOB_NO}")
            if r_day == 10 :
                logger.info(f"11 days remaining {i.CUSTOMER.C_NAME} | {i.CUSTOMER.MOB_NO}")
            if r_day == 5 :
                logger.info(f"6 days remaining {i.CUSTOMER.C_NAME} | {i.CUSTOMER.MOB_NO}")
        return JsonResponse("sucesss",safe=False)
    except Exception as e:
        # messages.error(request,"Something went wrong")
        logger.exception(f"{e}")
        return JsonResponse({"error":f"{e}"},safe=False,status=500)

def attendance_page(request):
    # context = {'user_types':}
    return render(request,"attendance.html")

class add_attendace(APIView):
    def post(self,request):
        try:
            u_type = request.POST.get("u_type")
            user = request.POST.get("user")
            a_date = request.POST.get("a_date")
            in_time = request.POST.get("in_time")
            out_time = request.POST.get("out_time")
            remark = request.POST.get("remark")

            logger.info(f"""
                u_type = {u_type}
                user = {user}
                a_date = {a_date}
                in_time = {in_time}
                out_time = {out_time}
                remark = {remark}
            """)
            if Attendance_user.objects.filter(USER=user,DATE=a_date).exists():
                return JsonResponse({"error":"This User Attendance found For selected date please find and edit"},status=412)
            else:
                ad = Attendance_user.objects.create(
                    USER = User.objects.get(id=user),
                    DATE = a_date,
                    PUNCH_IN = in_time,
                    PUNCH_OUT = out_time,
                    REMARK = remark,
                    CREATED_BY = User.objects.get(id=request.session['LOGIN_ID'])
                )
            return JsonResponse({"message":"Attendace Add SuccessFully"},status=200)
        except Exception as e:
            # messages.error(request,"Something went wrong")
            logger.exception(f"{e}")
            return JsonResponse({"error":f"{e}"},safe=False,status=500)

class edit_attendace(APIView):
    def get(self,request,id):
        data = list(Attendance_user.objects.filter(id=id).values("USER__USER_TYPE","USER__id","DATE","PUNCH_IN","PUNCH_OUT","REMARK"))
        return JsonResponse(data,safe=False)
    def post(self,request,id):
        try:
            u_type = request.POST.get("u_type")
            user = request.POST.get("user")
            a_date = request.POST.get("a_date")
            in_time = request.POST.get("in_time")
            out_time = request.POST.get("out_time")
            remark = request.POST.get("remark")

            logger.info(f"""
                u_type = {u_type}
                user = {user}
                a_date = {a_date}
                in_time = {in_time}
                out_time = {out_time}
                remark = {remark}
            """)
            if Attendance_user.objects.filter(USER=user,DATE=a_date).exclude(id=id).exists():
                return JsonResponse({"error":"This User Attendance found For selected date please find and edit"},status=412)
            else:
                edit = Attendance_user.objects.get(id=id)
                edit.USER = User.objects.get(id=user)
                edit.DATE = a_date
                edit.PUNCH_IN = in_time
                edit.PUNCH_OUT = out_time
                edit.REMARK = remark
                edit.MODIFIED_BY = User.objects.get(id=request.session['LOGIN_ID'])
                edit.save()
            
            return JsonResponse("Attendace Edit SuccessFully",safe=False,status=200)
        except Exception as e:
            # messages.error(request,"Something went wrong")
            logger.exception(f"{e}")
            return JsonResponse({"error":f"{e}"},safe=False,status=500)

def load_user_type(request):
    ut = request.GET.get("ut")
    login_id = request.session['LOGIN_ID']
    user_type = request.session['USER_TYPE']
    user_type_id = request.session['USER_TYPE_ID']
    # logger.info(f"ut = {ut} , login_id = {login_id} , user_type = {user_type} , user_type_id = {user_type_id}")
    data = []

    # if user_type == "bm":
    #     if ut == "rm":
    #         mapped_rm_id_list = list(User.objects.filter(USER_TYPE="rm",RM__BRANCH=user_type_id).values_list("id",flat=True))
    #         data = list(User.objects.filter(USER_TYPE=ut,id__in=mapped_rm_id_list).values())
    #     if ut == "ep":
    #         mapped_ep_id_list = list(User.objects.filter(USER_TYPE="ep",EP__RM=user_type_id).values_list("id",flat=True))
    #         data = list(User.objects.filter(USER_TYPE=ut,id__in=mapped_ep_id_list).values())
    # if user_type == "rm":
    #     if ut == "rm":
    #         data = list(User.objects.filter(USER_TYPE=ut,id=login_id).values())
    #     if ut == "ep":
    #         mapped_ep_id_list = list(User.objects.filter(EP__RM=user_type_id).values_list("id",flat=True))
    #         logger.info(f"mapped_ep_id_list = {mapped_ep_id_list}")
    #         mapped_ep_id_list.append(login_id)
    #         final_list = mapped_ep_id_list
    #         data = list(User.objects.filter(USER_TYPE=ut,id__in=final_list).values())

    if user_type == "bm" or user_type == "rm":
        final_list = get_under_mapped(request)
        # if ut == "rm":
        data = list(User.objects.filter(USER_TYPE=ut,id__in=final_list).values())
        # else:
        #     data = list(User.objects.filter(USER_TYPE=ut,id__in=final_list,OWNER =True).values())
        # logger.info(f"final_list = {final_list}")
    else:
        if ut == "bm":
            data = list(User.objects.filter(USER_TYPE=ut,OWNER =True).values())
        elif ut == "branch_manager":
            data = list(User.objects.filter(USER_TYPE="bm").values())
        else:
            data = list(User.objects.filter(USER_TYPE=ut).values())
    return JsonResponse(data,safe=False)

def load_attendance(request):
    login_id = request.session['LOGIN_ID']
    user_type = request.session['USER_TYPE']
    user_type_id = request.session['USER_TYPE_ID']

    # logger.info(f"""login_id = {login_id}""")
    v = ["id","DATE","PUNCH_IN","PUNCH_OUT","USER__USERNAME","USER__USER_TYPE","USER__NAME","REMARK"]

    if user_type == "bm" or user_type == "rm":
        # if user_type =="bm":
        #     mapped_rm_id_list = list(User.objects.filter(USER_TYPE="rm",RM__BRANCH=user_type_id).values_list("id",flat=True))
        #     mapped_ep_id_list = list(User.objects.filter(USER_TYPE="ep",EP__RM=user_type_id).values_list("id",flat=True))
        #     final_list = list(set(mapped_rm_id_list + mapped_ep_id_list))
        #     final_list.append(login_id)
        # if user_type == "rm":
        #     mapped_ep_id_list = list(User.objects.filter(USER_TYPE="ep",EP__RM=user_type_id).values_list("id",flat=True))
        #     mapped_ep_id_list.append(login_id)
        #     final_list = mapped_ep_id_list
        # logger.info(f"""final list = {final_list} """)
        final_list = get_under_mapped(request)
        # logger.info(f"final_list = {final_list}")
        data = list(Attendance_user.objects.filter(USER__in = final_list).values(*v).order_by('-id'))
    elif user_type == "bo":
        data = list(Attendance_user.objects.filter(USER__id=login_id).values(*v).order_by('-id'))
    else:
        data = list(Attendance_user.objects.filter().values(*v).order_by('-id'))
    return JsonResponse({"data":data},safe=False)

@api_view(["POST"])
def delete_attendance(request,id):
    try:
        a = Attendance_user.objects.get(id=id)
        a.delete()
        return JsonResponse("Attendance deleted successfully",safe=False,status=200)
    except Exception as e:
        logger.exception(e)
        return JsonResponse("Something went wrong",safe=False,status=500)

def punch_in(request):
    try:
        login_id = request.session['LOGIN_ID']
        t_d = date.today()

        now = datetime.now()
        current_time = now.strftime("%H:%M")
        if Attendance_user.objects.filter(USER=login_id,DATE=t_d).exists():
            return JsonResponse({"error":"You are Already Punch In Today"},status=412)
        else:
            punch = Attendance_user.objects.create(
                USER = User.objects.get(id=login_id),
                DATE = t_d,
                PUNCH_IN = current_time,
                CREATED_BY = User.objects.get(id=request.session['LOGIN_ID'])
            )
            return JsonResponse({"message":"Punch In successfully"},status=200)
    except Exception as e:
        messages.error(request,"Something went wrong")
        logger.exception(f"{e}")
        return JsonResponse({"error":f"{e}"},safe=False,status=500)

def punch_out(request):
    try:
        login_id = request.session['LOGIN_ID']
        t_d = date.today()
        now = datetime.now()
        current_time = now.strftime("%H:%M")
        if Attendance_user.objects.filter(USER=login_id,DATE=t_d).exists():
            a = Attendance_user.objects.get(USER=login_id,DATE=t_d)
            out = a.PUNCH_OUT
            if out == None:
                a.PUNCH_OUT = current_time
                a.MODIFIED_BY = User.objects.get(id=request.session['LOGIN_ID'])
                a.save()
                return JsonResponse({"message":"Punch Out successfully"},status=200)
            else:
                return JsonResponse({"error":"You are Already Punch Out Today"},status=412)
        else:
            return JsonResponse({"error":"Please Punch In First"},status=412)
    except Exception as e:
        messages.error(request,"Something went wrong")
        logger.exception(f"{e}")
        return JsonResponse({"error":f"{e}"},safe=False,status=500)


def leads_page(request):
    return render(request,"leads.html")

def load_leads(request):
    user_type    = request.session['USER_TYPE']
    user_type_id = request.session['USER_TYPE_ID']

    v = ["id","C_NAME","REQUIRE","QUALIFICATION","MOB_NO","ANNUAL_CTC","EMAIL","RM_EP__NAME","RM_EP__USERNAME"]

    if user_type == "bm" or user_type == "rm":
        final_list = get_under_mapped(request)
        # logger.info(f"final list = {final_list}")
        data = list(Leads.objects.filter(RM_EP__in=final_list).values(*v).order_by("-id"))
    
    else:
        data = list(Leads.objects.filter().values(*v).order_by("-id"))

    # if user_type == "rm":
    #     data = list(Leads.objects.filter(RM__id=user_type_id).values(*v).order_by("-id"))
    # elif user_type == "ep":
    #     data = list(Leads.objects.filter(EP__id=user_type_id).values("id","C_NAME","REQUIRE","QUALIFICATION","MOB_NO","ANNUAL_CTC","EMAIL").order_by("-id"))
    # else:
    #     data = list(Leads.objects.values("id","C_NAME","REQUIRE","QUALIFICATION","MOB_NO","ANNUAL_CTC","EMAIL").order_by("-id"))
    return JsonResponse({"data":data},safe=False)
# def add_insurance_customer_master(request):
#     return render(request,"add_insurance_customer_master.html")
def load_lead_cust(request):
    user_type    = request.session['USER_TYPE']
    user_type_id = request.session['USER_TYPE_ID']
    user = request.GET.get("user")
    u_type = request.GET.get("u_type")
    values = ["id","C_NAME","REQUIRE","QUALIFICATION","MOB_NO","ANNUAL_CTC","EMAIL"]
    if user_type == "rm":
        data = list(Leads.objects.filter(RM_EP = user,LEAD_TYPE = u_type).values(*values).order_by("-id"))
    else:
        data = list(Leads.objects.filter(LEAD_TYPE = u_type).values(*values).order_by("-id"))
    return JsonResponse({"data":data},safe=False)

class Add_leads(APIView):
    def get(self,request):
        return render(request,"add_lead.html")
    def post(self,request):
        try:
            # user_id = request.session['USER_TYPE_ID']
            # user_type = request.session['USER_TYPE']
            
            pan_no = request.POST.get("pan_no")
            cust_require = request.POST.get("cust_require")
            cust_name = request.POST.get("cust_name")
            m_name = request.POST.get("m_name")
            f_name = request.POST.get("f_name")
            cust_dob = request.POST.get("cust_dob")
            qualification = request.POST.get("qualification")
            mob_no = request.POST.get("mob_no")
            annual_ctc = request.POST.get("annual_ctc")
            marital_status = request.POST.get("marital_status")
            email = request.POST.get("email")
            tobacco_user = request.POST.get("tobacco_user")
            tobacco_qty = request.POST.get("tobacco_qty")
            tobacco_consume = request.POST.get("tobacco_consume")
            alcohol_user = request.POST.get("alcohol_user")
            alcohol_qty = request.POST.get("alcohol_qty")
            alcohol_consume = request.POST.get("alcohol_consume")
            medical_history = request.POST.get("medical_history")
            medical_dtl = request.POST.get("medical_dtl")

            user_type = request.POST.get("u_type")
            user = request.POST.get("user")
            ut = User.objects.get(id=user)
            user_id = ut.USER_ID
            
            logger.info(f"""
            user_type = {user_type}
            user = {user}
            pan_no = {pan_no}
            user_id ={user_id}
            user_type ={user_type}
            cust_require ={cust_require}
            cust_name = {cust_name}
            m_name = {m_name}
            f_name = {f_name}
            cust_dob = {cust_dob}
            qualification = {qualification}
            mob_no = {mob_no}
            annual_ctc = {annual_ctc}
            email = {email}
            marital_status = {marital_status}
            tobacco_user = {tobacco_user}
            tobacco_qty = {tobacco_qty}
            tobacco_consume = {tobacco_consume}
            alcohol_user = {alcohol_user}
            alcohol_qty = {alcohol_qty}
            alcohol_consume = {alcohol_consume}
            medical_history = {medical_history}
            medical_dtl = {medical_dtl}
            """)

            add = Leads.objects.create(
                RM_EP = ut ,
                LEAD_TYPE = user_type,
                PAN_NO = pan_no,
                REQUIRE = cust_require ,
                C_NAME = cust_name ,
                M_NAME = m_name ,
                F_NAME = f_name ,
                
                QUALIFICATION = qualification ,
                MOB_NO = mob_no ,
                ANNUAL_CTC = annual_ctc ,
                EMAIL = email ,
                MARITAL_STATUS = marital_status ,
                CREATED_BY = User.objects.get(id=request.session['LOGIN_ID'])
            )
            if cust_dob != "":
                add.CUST_DOB = cust_dob

            if user_type == "bm":
                add.BM = Branch_Manager.objects.get(id = user_id)

            if user_type == "rm":
                add.RM = Relationship_Manager.objects.get(id = user_id)
                
            if user_type == "ep":
                add.EP = Easy_Partner.objects.get(id = user_id)

            if tobacco_user == "yes":
                add.TOBACCO_USER = True
                add.TOBACCO_QTY = tobacco_qty
                add.TOBACCO_CONSUME = tobacco_consume
            else:
                add.TOBACCO_QTY = ""
                add.TOBACCO_CONSUME = ""

            if alcohol_user == "yes":
                add.ALCOHOL_USER = True
                add.ALCOHOL_QTY = alcohol_qty
                add.ALCOHOL_CONSUME = alcohol_consume
            else:
                add.ALCOHOL_QTY = ""
                add.ALCOHOL_CONSUME = ""

            if medical_history == "yes":
                add.MEDICAL_HISTORY = True
                add.MEDICAL_DTL = medical_dtl
            else:
                add.MEDICAL_DTL = ""

            add.save()
            messages.success(request,"Lead Add successfully")
            return JsonResponse({"message":"Lead Add successfully"},status=200)
            # return redirect("/leads")
        except Exception as e:
            messages.error(request,"Something went wrong")
            logger.exception(f"{e}")
            # return redirect("/add_leads")
            return JsonResponse({"error":"something went wong"},status=500)

class Edit_leads(APIView):
    def get(self,request,id):
        data = Leads.objects.get(id=id)
        return render(request,"edit_lead.html",context={"data":data})
    def post(self,request,id):
        try:
            pan_no = request.POST.get("pan_no")
            cust_require = request.POST.get("cust_require")
            cust_name = request.POST.get("cust_name")
            m_name = request.POST.get("m_name")
            f_name = request.POST.get("f_name")
            cust_dob = request.POST.get("cust_dob")
            qualification = request.POST.get("qualification")
            mob_no = request.POST.get("mob_no")
            annual_ctc = request.POST.get("annual_ctc")
            email = request.POST.get("email")
            marital_status = request.POST.get("marital_status")
            tobacco_user = request.POST.get("tobacco_user")
            tobacco_qty = request.POST.get("tobacco_qty")
            tobacco_consume = request.POST.get("tobacco_consume")
            alcohol_user = request.POST.get("alcohol_user")
            alcohol_qty = request.POST.get("alcohol_qty")
            alcohol_consume = request.POST.get("alcohol_consume")
            medical_history = request.POST.get("medical_history")
            medical_dtl = request.POST.get("medical_dtl")
            
            
            user_type = request.POST.get("u_type")
            user = request.POST.get("user")
            ut = User.objects.get(id=user)
            user_id = ut.USER_ID

            logger.info(f"""
            user_type = {user_type}
            user = {user}
            cust_require ={cust_require}
            cust_name = {cust_name}
            m_name = {m_name}
            f_name = {f_name}
            cust_dob = {cust_dob}
            qualification = {qualification}
            mob_no = {mob_no}
            annual_ctc = {annual_ctc}
            email = {email}
            marital_status = {marital_status}
            tobacco_user = {tobacco_user}
            tobacco_qty = {tobacco_qty}
            tobacco_consume = {tobacco_consume}
            alcohol_user = {alcohol_user}
            alcohol_qty = {alcohol_qty}
            alcohol_consume = {alcohol_consume}
            medical_history = {medical_history}
            medical_dtl = {medical_dtl}
            """)
            edit = Leads.objects.get(id=id)
            edit.RM_EP = ut
            edit.PAN_NO = pan_no
            edit.LEAD_TYPE = user_type
            edit.REQUIRE = cust_require
            edit.C_NAME = cust_name
            edit.M_NAME = m_name
            edit.F_NAME = f_name
            edit.CUST_DOB = cust_dob
            edit.QUALIFICATION = qualification
            edit.MOB_NO = mob_no
            edit.ANNUAL_CTC = annual_ctc
            edit.EMAIL = email
            edit.MARITAL_STATUS = marital_status

            if user_type == "rm":
                edit.RM = Relationship_Manager.objects.get(id = user_id)

            if user_type == "rm":
                edit.RM = Relationship_Manager.objects.get(id = user_id)
                
            if user_type == "ep":
                edit.EP = Easy_Partner.objects.get(id = user_id)

            if tobacco_user == "yes":
                edit.TOBACCO_USER = True
                edit.TOBACCO_QTY = tobacco_qty
                edit.TOBACCO_CONSUME = tobacco_consume
            else:
                edit.TOBACCO_USER = False
                edit.TOBACCO_QTY = ""
                edit.TOBACCO_CONSUME = ""

            if alcohol_user == "yes":
                edit.ALCOHOL_USER = True
                edit.ALCOHOL_QTY = alcohol_qty
                edit.ALCOHOL_CONSUME = alcohol_consume
            else:
                edit.ALCOHOL_USER = False
                edit.ALCOHOL_QTY = ""
                edit.ALCOHOL_CONSUME = ""

            if medical_history == "yes":
                edit.MEDICAL_HISTORY = True
                edit.MEDICAL_DTL = medical_dtl
            else:
                edit.MEDICAL_HISTORY = False
                edit.MEDICAL_DTL = ""
            edit.MODIFIED_BY = User.objects.get(id=request.session['LOGIN_ID'])
            edit.save()
            messages.success(request,"Leads Edit successfully")
            # return redirect(f"/leads")
            return JsonResponse({"message":"Lead Edit successfully"},status=200)
        except Exception as e:
            messages.error(request,"Something went wrong")
            logger.exception(f"{e}")
            # return redirect(f"/edit_leads/{id}")
            return JsonResponse({"error":"something went wong"},status=500)
            # return JsonResponse({"error":"something went wong"},status=200)


def followup_page(request):
    return render(request,"followup.html")

class add_followup(APIView):
    def post(self,request):
        try:
            user_type = request.POST.get("u_type")
            user = request.POST.get("user")
            ut = User.objects.get(id=user)
            # user_id = ut.USER_ID
            cust = request.POST.get("cust")
            followup_date = request.POST.get("followup_date")
            followup_time = request.POST.get("followup_time")
            remark = request.POST.get("remark")

            logger.info(f"""
                user_type = {user_type}
                user = {user}
                cust = {cust}
                followup_date = {followup_date}
                followup_time = {followup_time}
                remark = {remark}
            """)
            add = Followups.objects.create(
                RM_EP = ut,
                TYPE = user_type,
                LEADS = Leads.objects.get(id=cust) ,
                DATE = followup_date ,
                TIME = followup_time ,
                REMARK = remark ,
                CREATED_BY = User.objects.get(id=request.session['LOGIN_ID'])
            )
            return JsonResponse({"message":"Followup Add successfully"},status=200)
        except Exception as e:
            # messages.error(request,"Something went wrong")
            logger.exception(f"{e}")
            # return redirect("/add_easy_partner_brokerage")
            return JsonResponse({"error":"something went wong"},status=200)

class edit_followup(APIView):
    def get(self,request,id):
        data = list(Followups.objects.filter(id=id).values())
        return JsonResponse(data,safe=False)
    def post(self,request,id):
        try:
            # cust = request.POST.get("cust")
            # user_type = request.POST.get("u_type")
            # user = request.POST.get("user")
            # ut = User.objects.get(id=user)
            # user_id = ut.USER_ID
            followup_date = request.POST.get("followup_date")
            followup_time = request.POST.get("followup_time")
            remark = request.POST.get("remark")

            logger.info(f"""
                followup_date = {followup_date}
                followup_time = {followup_time}
                remark = {remark}
            """)
            edit = Followups.objects.get(id=id)
            # edit.RM_EP = ut
            # edit.TYPE = user_type
            # edit.LEADS = Leads.objects.get(id=cust)
            edit.DATE = followup_date
            edit.TIME = followup_time
            edit.REMARK = remark
            edit.MODIFIED_BY = User.objects.get(id=request.session['LOGIN_ID'])
            edit.save()
            return JsonResponse({"message":"Followup updated successfully"},status=200)
        except Exception as e:
            # messages.error(request,"Something went wrong")
            logger.exception(e)
            # return redirect("/add_easy_partner_brokerage")
            return JsonResponse({"error":"something went wong"},status=500)

@api_view(["POST"])
def delete_followup(request):
    try:
        id = request.data.get("id")
        Followups.objects.filter(id=id).delete()
        return JsonResponse("Follow up deleted successfully",safe=False,status=200)
    except Exception as e:
        logger.exception(e)
        return JsonResponse("Something went wrong",safe=False,status=500)

def load_followups(request):
    # user_id = request.session['USER_TYPE_ID']
    # user_type = request.session['USER_TYPE']

    login_id = request.session['LOGIN_ID']
    user_type = request.session['USER_TYPE']
    user_type_id = request.session['USER_TYPE_ID']

    v = ["id","DATE","TIME","REMARK","RM_EP__NAME","RM_EP__USERNAME","LEADS__C_NAME"]

    if user_type == "bm" or user_type == "rm":
        # if user_type =="bm":
        #     mapped_rm_id_list = list(User.objects.filter(USER_TYPE="rm",RM__BRANCH=user_type_id).values_list("id",flat=True))
        #     mapped_ep_id_list = list(User.objects.filter(USER_TYPE="ep",EP__RM=user_type_id).values_list("id",flat=True))
        #     final_list = list(set(mapped_rm_id_list + mapped_ep_id_list))
        # if user_type == "rm":
        #     mapped_ep_id_list = list(User.objects.filter(USER_TYPE="ep",EP__RM=user_type_id).values_list("id",flat=True))
        #     mapped_ep_id_list.append(login_id)
        #     final_list = mapped_ep_id_list
        final_list = get_under_mapped(request)
        # logger.info(f"final_list = {final_list}")
        data = list(Followups.objects.filter(RM_EP__in = final_list).values(*v).order_by('-id'))
    # elif user_type == "admin" or user_type == "superadmin":
    else:
        data = list(Followups.objects.filter().values(*v).order_by('-id'))
    # if user_type == "bm":
    #     data = list(Followups.objects.filter(LEADS__LEAD_TYPE="rm", LEADS__RM__id = user_id).values(*v).order_by('-id'))
    # elif user_type == "rm":
    #     data = list(Followups.objects.filter(LEADS__LEAD_TYPE="rm", LEADS__RM__id = user_id).values(*v).order_by('-id'))
    # elif user_type == "ep":
    #     data = list(Followups.objects.filter(LEADS__LEAD_TYPE="ep", LEADS__EP__id = user_id).values(*v).order_by('-id'))
    # else:
    #     data = list(Followups.objects.values(*v).order_by('-id'))
    return JsonResponse({"data":data},safe=False)

def meetings_page(request):
    return render(request,"meetings.html")

@api_view(["POST"])
def add_meeting(request):
    try:
        user_type = request.POST.get("u_type")
        user = request.POST.get("user")
        ut = User.objects.get(id=user)

        cust_type = request.data.get("cust_t")
        cust = request.data.get("cust")
        date = request.data.get("followup_date")
        time = request.data.get("followup_time")
        remark = request.data.get("remark")

        logger.info(f"""
                    cust_type = {cust_type}
                    cust = {cust}
                    date = {date}
                    time = {time}
                    remark = {remark}
                    user_type = {request.session["USER_TYPE"]}
                    user = {request.session['LOGIN_ID']}
                    """)

        a = Meetings.objects.create(
            RM_EP = ut,
            TYPE = cust_type,
            DATE = date,
            TIME = time,
            REMARK = remark,
            USER_TYPE = request.session["USER_TYPE"],
            USER = request.session['LOGIN_ID'],
            CREATED_BY = User.objects.get(id=request.session['LOGIN_ID'])
        )

        if cust_type == "lead":
            a.LEADS = Leads.objects.get(id=cust)
        # if cust_type == "mf_customer":
        #     a.MF_CUST = Registration_personal_details.objects.get(id=cust)
        if cust_type == "customer":
            a.I_CUST = Customer.objects.get(id=cust)

        a.save()
        return JsonResponse("Meeting added successfully",safe=False,status=200)
    except Exception as e:
        logger.exception(e)
        return JsonResponse("somethin went wrong",safe=False,status=500)
    

@api_view(["POST"])
def edit_meeting(request):
    try:
        id = request.data.get('id')
        date = request.data.get("followup_date")
        time = request.data.get("followup_time")
        remark = request.data.get("remark")

        logger.info(f""" edit meeting
                    id = {id}
                    date = {date}
                    time = {time}
                    remark = {remark}
                    user_type = {request.session["USER_TYPE"]}
                    user = {request.session['LOGIN_ID']}
                    """)
        a = Meetings.objects.filter(id=id).update(DATE=date,TIME=time,REMARK=remark)
        return JsonResponse("Meeting updated successfully",safe=False,status=200)
    except Exception as e:
        logger.exception(e)
        return JsonResponse("something went wrong",safe=False,status=500)

@api_view(["POST"])
def delete_meeting(request):
    try:
        id = request.data.get("id")
        Meetings.objects.filter(id=id).delete()
        return JsonResponse("Meeting deleted successfully",safe=False,status=200)
    except Exception as e:
        logger.exception(e)
        return JsonResponse("Something went wrong",safe=False,status=500)


def get_meeting(request,id):
    data = list(Meetings.objects.filter(id=id).values())
    return JsonResponse(data,safe=False,status=200)

def load_meetings(request):
    user = request.session['LOGIN_ID']
    user_type = request.session['USER_TYPE']
    # logger.info(f"user = {user} user_type={user_type}")
    
    v = ["id","DATE","TIME","REMARK","RM_EP__NAME","RM_EP__USERNAME","LEADS__C_NAME","LEADS__MOB_NO","I_CUST__C_NAME","I_CUST__MOB_NO","TYPE"]

    if user_type == "bm" or user_type == "rm":
        final_list = get_under_mapped(request)
        # logger.info(f"final list = {final_list}")
        data = list(Meetings.objects.filter(RM_EP__in=final_list).values(*v).order_by("-id"))
    else:
        data = list(Meetings.objects.filter().values(*v).order_by("-id"))
    return JsonResponse({"data":data},safe=False,status=200)

def filter_customer(request):
    try:
        customer_type = request.GET.get('customer_type')
        user_type_id = request.GET.get('user')
        user_type = request.GET.get('u_type')
        # user_type = request.session['USER_TYPE']
        # user_type_id = request.session['USER_TYPE_ID']
        logger.info(f"""
                    customer_type = {customer_type}
                    user_type = {user_type}
                    user_type_id = {user_type_id}
                    """)
        v = ['id','C_NAME','MOB_NO','PAN_NO']
        kwargs,data = {},[]
        kwargs['RM_EP'] = user_type_id
        if customer_type == "lead":
            kwargs['LEAD_TYPE'] = user_type
            logger.info(f"sasadas{kwargs['LEAD_TYPE']}")
            # kwargs[f'{user_type.upper()}'] = user_type_id
            data = list(Leads.objects.filter(**kwargs).values(*v))

        # if customer_type == "mf_customer":
        #     # data = Leads.objects.filter(**kwargs).values()
        #     data = []

        if customer_type == "customer":
            kwargs['TYPE'] = user_type
            
            # kwargs[f'{user_type.upper()}'] = user_type_id
            data = list(Customer.objects.filter(**kwargs).exclude(IS_DELETED=True).values(*v))
        # d = list(Leads.objects.filter(LEAD_TYPE ="rm",RM_EP="9").values('id','C_NAME','MOB_NO'))
        # logger.info(f'd = {d}')
        return JsonResponse(data,safe=False,status=200)
    except Exception as e:
        logger.exception(e)
        return JsonResponse(e,safe=False,status=500)

def meetings_customer1(request):
    customer_type = request.GET.get('customer_type')
    user_type = request.session['USER_TYPE']
    user_type_id = request.session['USER_TYPE_ID']

    logger.info(f"""
                 new_customer_type = {customer_type}
                new_user_type = {user_type}
                new_user_type_id = {user_type_id}
                 """)

    if user_type == "rm" or user_type == "ep":
        col_name = Q(RM_EP__id = user_type_id)
    if user_type == "admin":
        col_name = Q()

    if customer_type == "lead":
        data = list(Leads.objects.filter(col_name).values("id","C_NAME","MOB_NO"))
    if customer_type == "customer":
        data = list(Customer.objects.filter(col_name).values("id","C_NAME","MOB_NO"))
    # if user_type == "rm":
    #     if customer_type == "customer_lead":
    #         data = list(Leads.objects.filter(RM__id=user_type_id).values("C_NAME","MOB_NO"))
    #     if customer_type == "mf_customer":
    #         data = list(Registration_personal_details.objects.filter().values("NAME","MOBILE"))
    #     if customer_type == "insurance_customer":
    #         logger.info(Customer.objects.filter(RM__id=user_type_id).query)
    #         data = list(Customer.objects.filter(RM__id=user_type_id).values("C_NAME","MOB_NO"))

    # if user_type == "ep":
    #     if customer_type == "customer_lead":
    #         data = list(Leads.objects.filter(EP__id=user_type_id).values("C_NAME","MOB_NO"))
    #     if customer_type == "mf_customer":
    #         data = list(Registration_personal_details.objects.filter().values("NAME","MOBILE"))
    #     if customer_type == "insurance_customer":
    #         data = list(Customer.objects.filter(EP__id=user_type_id).values("C_NAME","MOB_NO"))

    return JsonResponse(data,safe=False,status=200)

def notification_page(request):
    return render(request,"notification.html")

@api_view(["POST"])
def send_notification(request):
    try:
        notify_cust_t = request.POST.get("cust_t")
        notify_cust = request.POST.getlist("notify_cust")
        notify_title = request.POST.get("notify_title")
        notify_desc = request.POST.get("notify_desc")

        logger.info(f"""
        notify_cust_t = {notify_cust_t}
        notify_cust = {notify_cust}
        notify_title = {notify_title}
        notify_desc = {notify_desc}
        """)

        notify_cust = ','.join(notify_cust)

        logger.info(f"notify_cust = {notify_cust}")

        
        if notify_cust_t == "lead":
            type = "lead"
        if notify_cust_t == "customer":
            type = "customer"

        Notifications.objects.create(
            CUSTOMER_IDS = notify_cust ,
            TYPE = type ,
            TITLE = notify_title ,
            DESCRIPTION = notify_desc,
            USER_TYPE = request.session["USER_TYPE"],
            USER = request.session['LOGIN_ID']
        )
        # for i in range(len(notify_cust)):
        #     if notify_cust_t == "customer_lead":
        #         data = Leads.objects.get(id=notify_cust[i])
        #     if notify_cust_t == "mf_customer":
        #         data = list(Registration_personal_details.objects.filter().values("NAME","MOBILE"))
        #     if notify_cust_t == "insurance_customer":
        #         data = list(Customer.objects.filter(id=i).values("C_NAME","MOB_NO"))
        return JsonResponse({"message":"Notification send successfully"},status=200)
    except Exception as e:
        # messages.error(request,"Something went wrong")
        logger.exception(f"{e}")
        # return redirect("/add_easy_partner_brokerage")
        return JsonResponse({"error":"something went wong"},status=200)

def load_notifications(request):
    data = list(Notifications.objects.filter(USER_TYPE=request.session["USER_TYPE"],USER=request.session['LOGIN_ID']).values())
    return JsonResponse({"data":data},safe=False,status=200)

def get_notification_users(request,id):
    notification_obj = Notifications.objects.get(id=id)
    customer_ids = notification_obj.CUSTOMER_IDS.split(",")
    logger.info(f"customer ids = {customer_ids}")
    data = []
    if notification_obj.TYPE == "lead":
        data = list(Leads.objects.filter(id__in=customer_ids).values('id','C_NAME','MOB_NO'))
    if notification_obj.TYPE == "customer":
        data = list(Customer.objects.filter(id__in=customer_ids).values('id','C_NAME','MOB_NO'))
    # if notification_obj.TYPE == "i_customer":
    #     data = list(Customer.objects.filter(id__in=customer_ids).values('id','C_NAME','MOB_NO'))
    return JsonResponse(data,safe=False,status=200)

def sip_calculator_page(request):
    return render(request,"calculator/sip_calculator.html")

def sip_calculator(request):
    amount      = request.GET.get("amount")
    yearlyRate  = request.GET.get("yearly_rate")
    years       = request.GET.get("years")

    # logger.info(f"""
    #     amount = {amount}
    #     yearlyRate = {yearlyRate}
    #     years = {years}
    # """)

    amount = float(amount)
    yearlyRate = float(yearlyRate)
    years = int(years)
    monthlyRate = yearlyRate/12/100
    months = years * 12
    invest_amt = round(amount * months)
    futureValue = amount * ((((1 + monthlyRate)**(months))-1) * (1 + monthlyRate))/monthlyRate
    futureValue = round(futureValue)
    est_return = futureValue - invest_amt
    # logger.info(f"The expected amount you will get is{futureValue}")
    # format_number(i_amount, locale='en_IN')
    # print("The expected amount you will get is:",futureValue)
    response = {
            "invest_amt"    : format_number(invest_amt, locale='en_IN'),
            "est_return"    : format_number(est_return, locale='en_IN'),
            "futureValue"   : format_number(round(futureValue), locale='en_IN')  # Future value of the investment after SWP
        }
    return JsonResponse(response,safe=False,status=200)

def sip_lumpsum_calculator_page(request):
    return render(request,"calculator/sip_lumpsum_calculator.html")


def sip_lumpsum_calculator(request):
    try:
        amount = request.GET.get("amount")
        yearly_rate = request.GET.get("yearly_rate")
        years = request.GET.get("years")

        logger.info(f"""
            amount = {amount}
            yearlyRate = {yearly_rate}
            years = {years}
        """)

        amount = float(amount)
        yearlyRate = float(yearly_rate)
        years = int(years)
        
        futureValue = round(amount*(1+yearlyRate/100)**years)
        est_return = futureValue - amount

        logger.info(f"The expected amount you will get is{futureValue}")
        # print("The expected amount you will get is:",futureValue)
        response = {
            "invest_amt"    : format_number(amount, locale='en_IN'),
            "est_return"    : format_number(est_return, locale='en_IN'),
            "futureValue"   : format_number(round(futureValue), locale='en_IN')  # Future value of the investment after SWP
        }
        # {"invest_amt":amount,"est_return":est_return,"futureValue":futureValue}

        return JsonResponse(response,safe=False,status=200)
    except Exception as e:
        # messages.error(request,"Something went wrong")
        logger.exception(f"{e}")
        # return redirect("/add_easy_partner_brokerage")
        return JsonResponse({"error":"something went wong"},status=200)

def swp_calculator_page(request):
    return render(request,"calculator/swp_calculator.html")

# def swp_calculator(request):
#     try:
#         i_amount = int(request.GET.get("i_amount"))
#         mw = int(request.GET.get("w_m"))
#         ri = float(request.GET.get("ir"))
#         y = int(request.GET.get("years"))
#         ti = i_amount
#         # mw = 1000
#         # ri = 10
#         # y = 1
#         tm = y*12

#         total_interest = []
#         for i in range(1,tm+1):
#             print("i",i)
#             ti = ti - mw
#             interest = ti*(ri/1200)
#             total_interest.append(round(interest))
#             ti  = interest + ti

#         withdraw_amt = mw * tm
#         total_interest = sum(total_interest)
#         return JsonResponse({"invest_amt":i_amount,"withdraw_amt":withdraw_amt,"total_interest":total_interest,"futureValue":round(ti)},safe=False,status=200)
#     except Exception as e:
#         # messages.error(request,"Something went wrong")
#         logger.exception(f"{e}")
#         # return redirect("/add_easy_partner_brokerage")
#         return JsonResponse({"error":"something went wong"},status=200)


def swp_calculator(request):
    try:
#         amount
# yearly_rate
# years
        # Retrieve inputs from GET parameters
        i_amount    = int(request.GET.get("amount"))  # Initial Investment
        mw          = int(request.GET.get("withdrawal_per_month"))  # Monthly Withdrawal
        ri          = float(request.GET.get("yearly_rate"))  # Interest Rate (annual)
        y           = int(request.GET.get("years"))  # Duration in years
        
        # Initialize variables
        ti = i_amount  # Total investment at the start
        tm = y * 12  # Total number of months

        total_interest = []  # To keep track of interest for each month

        for month in range(1, tm + 1):
            # Deduct monthly withdrawal from current balance
            ti -= mw
            
            # Calculate interest on the remaining balance, allowing negative balance
            interest = ti * (ri / 1200)  # Monthly interest rate
            total_interest.append(round(interest))
            
            # Update balance by adding the interest
            ti += interest

        # Calculate total withdrawal and interest earned
        withdraw_amt = mw * tm  # Full withdrawal over the entire period
        total_interest_sum = sum(total_interest)

        # Prepare the response
        response = {
            "invest_amt": format_number(i_amount, locale='en_IN'),
            "withdraw_amt": format_number(withdraw_amt, locale='en_IN'),
            "total_interest": format_number(total_interest_sum, locale='en_IN'),
            "futureValue": format_number(round(ti), locale='en_IN')  # Future value of the investment after SWP
        }
        
        return JsonResponse(response, safe=False, status=200)
    except Exception as e:
        logger.exception(f"Error in SWP calculation: {e}")
        return JsonResponse({"error": "Something went wrong"}, status=500)

    
def step_up_sip_calculator(request):
    # Retrieve parameters from the request
    amount          = request.GET.get("amount")
    yearlyRate      = request.GET.get("yearly_rate")
    years           = request.GET.get("years")
    step_up_percent = request.GET.get("step_up_percent")

    # Convert parameters to appropriate types
    amount = float(amount)
    yearlyRate = float(yearlyRate)
    years = int(years)
    step_up_percent = float(step_up_percent)

    monthlyRate = yearlyRate / 12 / 100  # Monthly interest rate

    invest_amt = 0  # Total invested amount
    future_value = 0  # Future value of the investment

    # Calculate future value of Step-Up SIP for each year
    for year in range(years):
        yearly_sip = amount * ((1 + step_up_percent / 100) ** year)  # SIP for this year
        months_remaining = (years - year) * 12  # Months left for that year's SIP to grow

        # Future value for the SIP of the current year
        fv_yearly_sip = yearly_sip * ((((1 + monthlyRate)**months_remaining) - 1) * (1 + monthlyRate)) / monthlyRate
        
        # Add current year's future value and investment to totals
        future_value += fv_yearly_sip
        invest_amt += yearly_sip * 12  # Total investment in the current year

    invest_amt = round(invest_amt)  # Round invested amount
    future_value = round(future_value)  # Round future value
    est_return = future_value - invest_amt  # Estimated return

    # Prepare response data with formatted values
    response = {
        "invest_amt"    : format_number(invest_amt, locale='en_IN'),
        "est_return"    : format_number(est_return, locale='en_IN'),
        "futureValue"   : format_number(future_value, locale='en_IN')  # Future value of the investment after step-up SIP
    }
    return JsonResponse(response, safe=False, status=200)

def child_education_plan_calculator(request):
    # Input parameters from the request
    years = int(request.GET.get("years"))  # Number of years to goal
    current_cost = float(request.GET.get("current_cost"))  # Education cost today (₹)
    inflation_rate = float(request.GET.get("inflation_rate")) / 100  # Assumed inflation rate (%)
    existing_inv = float(request.GET.get("existing_inv"))  # Existing investment (₹)
    return_existing_inv = float(request.GET.get("return_existing_inv")) / 100  # Return on existing investment (%)
    lumpsum_inv = float(request.GET.get("lumpsum_inv"))  # Planned lump sum investment (₹)
    return_new_inv = float(request.GET.get("return_new_inv")) / 100  # Return on new investment (%)

    # Step 1: Calculate future education cost adjusted for inflation
    future_education_cost = current_cost * ((1 + inflation_rate) ** years)

    # Step 2: Calculate future value of the existing investment
    future_value_existing_inv = existing_inv * ((1 + return_existing_inv) ** years)

    # Step 3: Calculate future value of the new lump sum investment
    future_value_new_inv = lumpsum_inv * ((1 + return_new_inv) ** years)

    # Step 4: Total future value of investments
    total_investment_value = future_value_existing_inv + future_value_new_inv

    # Step 5: Calculate shortfall or surplus (future education cost - total investment value)
    shortfall_or_surplus = future_education_cost - total_investment_value
    if shortfall_or_surplus > 0:
        plan_status = "Shortfall"
    else:
        plan_status = "Surplus"

    # Step 6: Format and prepare response data
    response = {
        "current_education_cost": format_number(current_cost, locale='en_IN'),
        "future_education_cost": format_number(future_education_cost, locale='en_IN'),
        "future_value_existing_inv": format_number(future_value_existing_inv, locale='en_IN'),
        "future_value_new_inv": format_number(future_value_new_inv, locale='en_IN'),
        "total_investment_value": format_number(total_investment_value, locale='en_IN'),
        "shortfall_or_surplus": format_number(abs(shortfall_or_surplus), locale='en_IN'),
        "plan_status": plan_status  # Whether you have a shortfall or surplus
    }

    # Return the response as JSON
    return JsonResponse(response, safe=False, status=200)
    

from django.http import JsonResponse
from babel.numbers import format_number

def child_education_plan_fundbazar(request):
    # Input parameters from the request
    years = int(request.GET.get("years"))  # Number of years to goal
    current_cost = float(request.GET.get("current_cost"))  # Education cost today (₹)
    inflation_rate = float(request.GET.get("inflation_rate")) / 100  # Assumed inflation rate (%)
    sip_amount = float(request.GET.get("sip_amount"))  # Planned monthly SIP investment (₹)
    return_sip = float(request.GET.get("return_sip")) / 100  # Annual return on SIP (%)
    lumpsum_inv = float(request.GET.get("lumpsum_inv"))  # Planned lump sum investment (₹)
    return_lumpsum = float(request.GET.get("return_lumpsum")) / 100  # Annual return on lump sum investment (%)

    # Step 1: Calculate future education cost adjusted for inflation
    future_education_cost = current_cost * ((1 + inflation_rate) ** years)

    # Step 2: Calculate future value of the SIP (Systematic Investment Plan)
    monthly_rate_sip = return_sip / 12  # Monthly return rate for SIP
    total_months = years * 12  # Total months for SIP
    future_value_sip = sip_amount * (((1 + monthly_rate_sip) ** total_months - 1) / monthly_rate_sip) * (1 + monthly_rate_sip)

    # Step 3: Calculate future value of the lump sum investment
    future_value_lumpsum = lumpsum_inv * ((1 + return_lumpsum) ** years)

    # Step 4: Total future investment value (SIP + Lump sum)
    total_investment_value = future_value_sip + future_value_lumpsum

    # Step 5: Calculate shortfall or surplus (future education cost - total investment value)
    shortfall_or_surplus = future_education_cost - total_investment_value
    if shortfall_or_surplus > 0:
        plan_status = "Shortfall"
    else:
        plan_status = "Surplus"

    # Step 6: Format and prepare response data
    response = {
        "current_education_cost": format_number(current_cost, locale='en_IN'),
        "future_education_cost": format_number(future_education_cost, locale='en_IN'),
        "future_value_sip": format_number(future_value_sip, locale='en_IN'),
        "future_value_lumpsum": format_number(future_value_lumpsum, locale='en_IN'),
        "total_investment_value": format_number(total_investment_value, locale='en_IN'),
        "shortfall_or_surplus": format_number(abs(shortfall_or_surplus), locale='en_IN'),
        "plan_status": plan_status
    }

    # Return the response as JSON
    return JsonResponse(response, safe=False, status=200)


def policy_broker_page(request):
    return render(request,"policy_broker.html")

class add_policy_broker(APIView):
    def post(self,request):
        try:
            broker_name = request.POST.get("broker_name")
            logger.info(f"""
                broker_name = {broker_name}
            """)
            if Policy_broker_master.objects.filter(NAME=broker_name).exists():
                return JsonResponse({"error":"This Insurance Name Already Exist"},status=412)
            else:
                add = Policy_broker_master.objects.create(
                    NAME = broker_name,
                    CREATED_BY = User.objects.get(id=request.session['LOGIN_ID'])
                )
            # messages.success(request,"Sub Broker Brokerage Add successfully")
            # return redirect("/easy_partner_brokerage")
                return JsonResponse({"message":"Broker Name Add successfully"},status=200)
        except Exception as e:
            # messages.error(request,"Something went wrong")
            logger.exception(f"{e}")
            # return redirect("/add_easy_partner_brokerage")
            return JsonResponse({"error":"something went wong"},status=200)

class edit_policy_broker(APIView):
    def get(self,request,id):
        data = list(Policy_broker_master.objects.filter(id=id).values("NAME"))
        return JsonResponse(data,safe=False)
    def post(self,request,id):
        try:
            broker_name = request.POST.get("broker_name")
            logger.info(f"""
                broker_name = {broker_name}
            """)
            if Policy_broker_master.objects.filter(NAME=broker_name).exclude(id=id).exists():
                return JsonResponse({"error":"This Broker Name Already Exist"},status=412)
            else:
                edit = Policy_broker_master.objects.get(id=id)
                edit.NAME = broker_name
                edit.MODIFIED_BY = User.objects.get(id=request.session['LOGIN_ID'])
                edit.save()
            # messages.success(request,"Sub Broker Brokerage Add successfully")
            # return redirect("/easy_partner_brokerage")
                return JsonResponse({"message":"Broker Name Edited successfully"},status=200)
        except Exception as e:
            # messages.error(request,"Something went wrong")
            logger.exception(f"{e}")
            # return redirect("/add_easy_partner_brokerage")
            return JsonResponse({"error":"something went wong"},status=200)

def load_policy_broker(request):
    data = list(Policy_broker_master.objects.values("id","NAME").order_by('-id'))
    return JsonResponse({"data":data},safe=False)
    
# buy fd , pms 

def buy_fd_page(request):
    return render(request,"buy_fd_table.html")

@api_view(['POST'])
def add_buy_fd(request):
    try:
        user = request.POST.get("user")
        user_type = request.POST.get("u_type")
        buy_type = request.POST.get("buy_type")
        customer = request.POST.get("customer")
        start_date = request.POST.get("s_date")
        end_date = request.POST.get("e_date")
        company_name = request.POST.get("comp_name")
        tenure = request.POST.get("tenure")
        interest_rate = request.POST.get("roi")
        amt = request.POST.get("amt")
        brokerage_percentage = request.POST.get("b_percentage")
        brokerage_amt = request.POST.get("b_amt")

        logger.info(f"""
            user = {user}
            user_type = {user_type}
            buy_type = {buy_type}
            customer = {customer}
            start_date = {start_date}
            end_date = {end_date}
            company_name = {company_name}
            tenure = {tenure}
            interest_rate = {interest_rate}
            amt = {amt}
            brokerage_percentage = {brokerage_percentage}
            brokerage_amt = {brokerage_amt}
        """)

        a = Buy_FD.objects.create(
            USER_TYPE = user_type,
            EP_RM = User.objects.get(id=user),
            BUY_TYPE = buy_type,
            CUSTOMER = Customer.objects.get(id=customer),
            START_DATE = start_date,
            END_DATE = end_date,
            COMPANY_NAME = company_name,
            TENURE = tenure,
            INTEREST_RATE = interest_rate,
            AMOUNT = amt,
            BROKERAGE_PERCENTAGE = brokerage_percentage,
            BROKERAGE_AMOUNT = brokerage_amt,
            CREATED_BY = User.objects.get(id=request.session['LOGIN_ID'])
        )

        if buy_type in ['fd','bond','ncd']:
            a.INTEREST_RATE = interest_rate
            a.save()

        return JsonResponse({'message':f'{buy_type.title()} added successfully'},safe=False,status=200)
    except Exception as e:
        logger.exception(e)
        return JsonResponse("Something went wrong", safe=False, status=500)
    

@api_view(['POST'])
def edit_buy_fd(request,id):
    try:
        user = request.POST.get("user")
        user_type = request.POST.get("u_type")
        buy_type = request.POST.get("buy_type")
        customer = request.POST.get("customer")
        start_date = request.POST.get("s_date")
        end_date = request.POST.get("e_date")
        company_name = request.POST.get("comp_name")
        tenure = request.POST.get("tenure")
        interest_rate = request.POST.get("roi")
        amt = request.POST.get("amt")
        brokerage_percentage = request.POST.get("b_percentage")
        brokerage_amt = request.POST.get("b_amt")

        logger.info(f"""
            user = {user}
            user_type = {user_type}
            buy_type = {buy_type}
            customer = {customer}
            start_date = {start_date}
            end_date = {end_date}
            company_name = {company_name}
            tenure = {tenure}
            interest_rate = {interest_rate}
            amt = {amt}
            brokerage_percentage = {brokerage_percentage}
            brokerage_amt = {brokerage_amt}
        """)
        a = Buy_FD.objects.get(id=id)
        # a.USER_TYPE = user_type
        # a.EP_RM = User.objects.get(id=user)
        a.BUY_TYPE = buy_type
        # a.CUSTOMER = Customer.objects.get(id=customer)
        a.START_DATE = start_date
        a.END_DATE = end_date
        a.COMPANY_NAME = company_name
        a.TENURE = tenure
        a.INTEREST_RATE = interest_rate
        a.AMOUNT = amt
        a.BROKERAGE_PERCENTAGE = brokerage_percentage
        a.BROKERAGE_AMOUNT = brokerage_amt
        a.MODIFIED_BY = User.objects.get(id=request.session['LOGIN_ID'])

        if buy_type in ['fd','bond','ncd']:
            a.INTEREST_RATE = interest_rate
            
        else:
            a.INTEREST_RATE = None
        a.save()

        return JsonResponse(f"{buy_type.title()} added successfully",safe=False,status=200)
    except Exception as e:
        logger.exception(e)
        return JsonResponse("Something went wrong", safe=False, status=500)

def delete_buy_fd(request,id):
    try:
        a = Buy_FD.objects.get(id=id)
        a.delete()
        return JsonResponse("Buy FD deleted successfully",safe=False,status=200)
    except Exception as e:
        logger.exception(e)
        return JsonResponse("Something went wrong",safe=False,status=500)
    


def get_buy_fd(request,id):
    try:
        a = Buy_FD.objects.filter(id=id)
        data = list(a.values())
        data[0]['CUSTOMER_NAME'] = a[0].CUSTOMER.C_NAME
        data[0]['CUSTOMER_PAN'] = a[0].CUSTOMER.PAN_NO
        data[0]['EP_RM_NAME'] = a[0].EP_RM.NAME
        # logger.info(f"data = {data}")
        return JsonResponse(data,safe=False,status=200)
    except Exception as e:
        logger.exception(e)
        return JsonResponse("Something went wrong",safe=False,status=500)


def load_buy_fd(request):
    login_id = request.session['LOGIN_ID']
    user_type = request.session['USER_TYPE']
    user_type_id = request.session['USER_TYPE_ID']
    values = [ "id","USER_TYPE","EP_RM_id","BUY_TYPE","CUSTOMER_id","CUSTOMER__C_NAME","CUSTOMER__PAN_NO","START_DATE","END_DATE","COMPANY_NAME","TENURE","INTEREST_RATE","AMOUNT","BROKERAGE_PERCENTAGE","BROKERAGE_AMOUNT","CREATED_BY_id","MODIFIED_BY_id","EP_RM__USERNAME","EP_RM__NAME"]
    # if user_type =="bm":
    #     mapped_rm_id_list = list(User.objects.filter(USER_TYPE="rm",RM__BRANCH=user_type_id).values_list("id",flat=True))
    #     mapped_ep_id_list = list(User.objects.filter(USER_TYPE="ep",EP__RM=user_type_id).values_list("id",flat=True))
    #     final_list = list(set(mapped_rm_id_list + mapped_ep_id_list))
    #     logger.info(f"final_list = {final_list}")
    #     data = list(Buy_FD.objects.filter(EP_RM__in=final_list).values(*values))
    # elif user_type == "rm":
    #     mapped_ep_id_list = list(User.objects.filter(USER_TYPE="ep",EP__RM=user_type_id).values_list("id",flat=True))
    #     mapped_ep_id_list.append(login_id)
    #     final_list = mapped_ep_id_list
    #     logger.info(f"final_list = {final_list}")
    #     data = list(Buy_FD.objects.filter(EP_RM__in=final_list).values(*values))
    if user_type == "bm" or user_type == "rm":
        final_list = get_under_mapped(request)
        # logger.info(f"final_list = {final_list}")
        data = list(Buy_FD.objects.filter(EP_RM__in=final_list).values(*values).order_by("-id"))
    elif user_type == "admin" or user_type == "superadmin":
        data = list(Buy_FD.objects.values(*values).order_by("-id"))
    return JsonResponse({"data":data})



class PermissionManagement(APIView):
    def get(self,request):
        modules = Modules.objects.all()
        return render(request,"crm_permission_management.html",context={"modules":modules})

@api_view(['POST'])
def add_role_permission(request):
    try:
        user_type = request.POST.get("user_type")
        allowed_modules = request.POST.getlist("allowed_modules")
    
        logger.info(f"""
            user_type = {user_type}
            allowed_modules = {allowed_modules}
            """)
        if User_Role_Permission.objects.filter(USER_TYPE = user_type).exists():
            return JsonResponse("This User type is Already exists", safe=False, status=412)
        else:
            a = User_Role_Permission.objects.create(
                USER_TYPE = user_type,
                ALLOWED_MODULES = ",".join(allowed_modules),
                CREATED_BY = User.objects.get(id=request.session['LOGIN_ID'])
            )
            return JsonResponse(f"Permission added successfully",safe=False,status=200)
    except Exception as e:
        logger.exception(e)
        return JsonResponse("Something went wrong", safe=False, status=500)

def get_role_permission(request,id):
    try:
        a = User_Role_Permission.objects.filter(id=id)
        data = list(a.values())
        return JsonResponse(data,safe=False,status=200)
    except Exception as e:
        logger.exception(e)
        return JsonResponse("Something went wrong",safe=False,status=500)

def load_role_permission(request):
    data = list(User_Role_Permission.objects.exclude(USER_TYPE="superadmin").values())
    return JsonResponse({"data":data},safe=False)

@api_view(['POST'])
def edit_role_permission(request,id):
    try:
        user_type = request.POST.get("user_type")
        allowed_modules = request.POST.getlist("allowed_modules")
    
        logger.info(f"""
            user_type = {user_type}
            allowed_modules = {allowed_modules}
            """)
        if User_Role_Permission.objects.filter(USER_TYPE = user_type).exclude(id=id).exists():
            return JsonResponse("This User type is Already exists", safe=False, status=412)
        else:
            e = User_Role_Permission.objects.get(id=id)
            e.USER_TYPE = user_type
            e.ALLOWED_MODULES = ",".join(allowed_modules)
            e.MODIFIED_BY = User.objects.get(id=request.session['LOGIN_ID'])
            # for i in allowed_modules:
            #     m = Modules.objects.filter(NAME=i)
            #     logger.info(f"allow_url = {m[URL]}")
                    # URL=

            e.save()
            return JsonResponse(f"Permission Edited successfully",safe=False,status=200)
    except Exception as e:
        logger.exception(e)
        return JsonResponse("Something went wrong", safe=False, status=500)

def delete_role_permission(request,id):
    try:
        a = User_Role_Permission.objects.get(id=id)
        a.delete()
        return JsonResponse("User Role deleted successfully",safe=False,status=200)
    except Exception as e:
        logger.exception(e)
        return JsonResponse("Something went wrong",safe=False,status=500)
    

# payment module

def payment(request):
    return render(request,"payment_table.html")


def payment_table(request):
    all_ep = User.objects.filter(USER_TYPE="ep")
    data = []
    for i in range(len(all_ep)):
        tmp = {}
        ep = all_ep[i]
        # logger.info(f"""query result = {Insurance.objects.filter(CUSTOMER__TYPE="ep",CUSTOMER__RM_EP=ep.id)}""")
        insurance_commission = 0
        fd_commission = 0
        mf_commission = 0
        
        if Insurance.objects.filter(CUSTOMER__TYPE="ep",CUSTOMER__RM_EP=ep.id).exists():
            insurance_commission = Insurance.objects.filter(CUSTOMER__TYPE="ep",CUSTOMER__RM_EP=ep.id).aggregate(Sum('COMMISSION_AMT',default=0))['COMMISSION_AMT__sum']
        if Buy_FD.objects.filter(USER_TYPE="ep",EP_RM=ep.id).exists():
            fd_commission = Buy_FD.objects.filter(USER_TYPE="ep",EP_RM=ep.id).aggregate(Sum('BROKERAGE_AMOUNT',default=0))['BROKERAGE_AMOUNT__sum']
        if Buy_MF.objects.filter(USER_TYPE="ep",EP_RM=ep.id):
            # mf_commission = Buy_MF.objects.filter(USER_TYPE="ep",EP_RM=ep.id).aggregate(Sum('EP_AMT',default=0))['EP_AMT__sum']
            mf_commission = Buy_MF.objects.filter(USER_TYPE="ep",EP_RM=ep.id).aggregate(Sum('EP_AMT',default=0))['EP_AMT__sum']
        
        total_earned_commission = fd_commission + mf_commission + insurance_commission
        total_paid_commission = Commission_paid.objects.filter(EP=ep.id).aggregate(Sum('AMOUNT',default=0))['AMOUNT__sum']
        total_due_commission =  total_earned_commission - total_paid_commission
        # logger.info(f"{i} - {ep.id} - {total_commission}")
        tmp['id'] = ep.id
        tmp['ep_name'] = ep.NAME
        tmp['insurance_commission'] = str(round(insurance_commission, 2))
        tmp['fd_commission'] = str(round(fd_commission, 2))
        tmp['mf_commission'] = str(round(mf_commission, 2))
        tmp['total_earned_commission'] = str(round(total_earned_commission, 2))
        tmp['total_paid_commission'] = str(round(total_paid_commission, 2))
        tmp['total_due_commission'] = str(round(total_due_commission, 2))
        data.append(tmp)
        # logger.info(f"{i} - {ep.id} - {total_earned_commission}")
    # return JsonResponse("hello",safe=False,status=200)
    return JsonResponse({"data":data},safe=False,status=200)

def all_ep(request):
    data = list(User.objects.filter(USER_TYPE = "ep").values())
    return JsonResponse(data,safe=False,status=200)

@api_view(["POST"])
def add_pay_out(request):
    try:
        ep = request.data.get("ep")
        amount = request.data.get("amount")
        transaction_date = request.data.get("transaction_date")
        transaction_check_no = request.data.get("transaction_check_no")

        logger.info(f""" url: pay_out_add
        ep = {ep}
        amount = {amount}
        transaction_date = {transaction_date}
        transaction_check_no = {transaction_check_no}
        """)
        

        a = Commission_paid.objects.create(
            EP = User.objects.get(id=ep),
            AMOUNT = amount,
            TRANSACTION_DATE = transaction_date,
            TRANSACTION_CHECK_NO = transaction_check_no,
            CREATED_BY = User.objects.get(id=request.session['LOGIN_ID'])
        )
        return JsonResponse("Pay out addedd successfully",safe=False,status=200)
    except Exception as e:
        logger.exception(e)
        return JsonResponse("Something went wrong",safe=False,status=500)


@api_view(["POST"])
def edit_pay_out(request):
    try:
        id = request.data.get("id")
        ep = request.data.get("ep")
        amount = request.data.get("amount")
        transaction_date = request.data.get("transaction_date")
        transaction_check_no = request.data.get("transaction_check_no")

        logger.info(f""" url: pay_out_edit
        ep = {ep}
        amount = {amount}
        transaction_date = {transaction_date}
        transaction_check_no = {transaction_check_no}
        """)

        a = Commission_paid.objects.get(id=id)
        a.EP = User.objects.get(id=ep)
        a.AMOUNT = amount
        a.TRANSACTION_DATE = transaction_date
        a.TRANSACTION_CHECK_NO = transaction_check_no
        a.MODIFIED_BY = User.objects.get(id=request.session['LOGIN_ID'])
        a.save()
        return JsonResponse("Pay out d successfully",safe=False,status=200)
    except Exception as e:
        logger.exception(e)
        return JsonResponse("Something went wrong",safe=False,status=500)


def delete_pay_out(request,id):
    try:
        Commission_paid.objects.filter(id=id).delete()
        return JsonResponse("Pay out deleted successfully",safe=False,status=200)
    except Exception as e:
        logger.exception(e)
        return JsonResponse("Something went wrong",safe=False,status=500)

def get_ep_pay_out(request,id):
    data = list(Commission_paid.objects.filter(EP=id).values())
    return JsonResponse({"data":data},safe=False,status=200)

def get_pay_out(request,id):
    data = list(Commission_paid.objects.filter(id=id).values())
    return JsonResponse(data,safe=False,status=200)

def payout_history(request,id):
    ep = User.objects.get(id=id)
    return render(request,"payout_history.html",context={"ep":ep})


def unauthorized(request):
    return render(request,"unauthorized.html")


def ep_dashboard_api(request):
    id = request.session['LOGIN_ID']
    ep = User.objects.get(id=id)
    data = {}
    customer_count = Customer.objects.filter(TYPE="ep",RM_EP=id).count()
    fd_commission = Buy_FD.objects.filter(USER_TYPE="ep",EP_RM=ep.id).aggregate(Sum('BROKERAGE_AMOUNT',default=0))['BROKERAGE_AMOUNT__sum']
    total_earned_commission = fd_commission
    total_paid_commission = Commission_paid.objects.filter(EP=ep.id).aggregate(Sum('AMOUNT',default=0))['AMOUNT__sum']
    
    fd_business = Buy_FD.objects.filter(USER_TYPE="ep",EP_RM=id).aggregate(Sum('AMOUNT',default=0))['AMOUNT__sum']
    total_business = fd_business
    data['customer_count'] = customer_count
    data['total_business'] = total_business
    data['total_commission'] = total_earned_commission
    data['received_amount'] = total_paid_commission
    data['pending_amt'] = total_earned_commission - total_paid_commission
    return JsonResponse(data,safe=False,status=200)


def buy_mf_page(request):
    return render(request,"buy_mf_table.html")

@api_view(["POST"])
def add_buy_mf(request):
    try:
        user_type = request.data.get('u_type')
        user = request.data.get('user')
        date = request.data.get('date')
        customer = request.data.get('customer')
        customer_status = request.data.get('customer_status')
        scheme_name = request.data.get('scheme_name')
        amount_invested = request.data.get('amount_invested')
        mode = request.data.get('mode')
        buy_type = request.data.get('buy_type')

        logger.info(f"""
            user_type = {user_type}
            user = {user}
            date = {date}
            customer = {customer}
            customer_status = {customer_status}
            scheme_name = {scheme_name}
            amount_invested = {amount_invested}
            mode = {mode}
            buy_type = {buy_type}
        """)
        cust_obj = Customer.objects.get(id=customer)
        a = Buy_MF.objects.create(
            USER_TYPE = user_type,
            EP_RM = User.objects.get(id=user),
            DATE = date,
            CUSTOMER = cust_obj,
            CUSTOMER_STATUS = customer_status,
            SCHEME_NAME = scheme_name,
            AMOUNT_INVESTED = amount_invested,
            MODE = mode,
            BUY_TYPE = buy_type,
        )
        if MF_master.objects.filter(SCHEME = scheme_name).exists():
            if cust_obj.TYPE == "ep":
                mf = MF_master.objects.get(SCHEME = scheme_name)
                ei_p = mf.NET_A_GST
                ep_p = cust_obj.EP.MF_C_P
                
                
                ei_amt = round((float(amount_invested)*float(ei_p))/100,2)

                ep_amt = round((float(ei_amt)*float(ep_p))/100,2)
                a.EI_PERCENT = ei_p
                a.EI_AMT = ei_amt
                a.EP_PERCENT = ep_p
                a.EP_AMT = ep_amt
                a.save()
        return JsonResponse("Buy MF record added successfully",safe=False,status=200)
    except Exception as e:
        logger.exception(e)
        return JsonResponse("Something went wrong",safe=False,status=500)
    

@api_view(["POST"])
def edit_buy_mf(request,id):
    try:
        # id = request.data.get('id')
        user_type = request.data.get('u_type')
        user = request.data.get('user')
        date = request.data.get('date')
        customer = request.data.get('customer')
        customer_status = request.data.get('customer_status')
        scheme_name = request.data.get('scheme_name')
        amount_invested = request.data.get('amount_invested')
        mode = request.data.get('mode')
        buy_type = request.data.get('buy_type')

        logger.info(f"""
            id = {id}
            user_type = {user_type}
            user = {user}
            date = {date}
            customer = {customer}
            customer_status = {customer_status}
            scheme_name = {scheme_name}
            amount_invested = {amount_invested}
            mode = {mode}
            buy_type = {buy_type}
        """)

        a = Buy_MF.objects.get(id=id)
        # a.USER_TYPE = user_type
        # a.EP_RM = User.objects.get(id=user)
        a.DATE = date
        # a.CUSTOMER = Customer.objects.get(id=customer)
        a.CUSTOMER_STATUS = customer_status
        a.SCHEME_NAME = scheme_name
        a.AMOUNT_INVESTED = amount_invested
        a.MODE = mode
        a.BUY_TYPE = buy_type
        a.save()


        return JsonResponse("Buy MF record updated successfully",safe=False,status=200)
    except Exception as e:
        logger.exception(e)
        return JsonResponse("Something went wrong",safe=False,status=500)
    
@api_view(["POST"])
def delete_buy_mf(request,id):
    try:
        Buy_MF.objects.filter(id=id).delete()
        return JsonResponse("Buy MF record deleted successfully",safe=False,status=200)
    except Exception as e:
        logger.exception(e)
        return JsonResponse("Something went wrong",safe=False,status=500)

def get_buy_mf(request,id):
    a = Buy_MF.objects.filter(id=id)
    data = list(a.values())
    data[0]['CUSTOMER_NAME'] = a[0].CUSTOMER.C_NAME
    data[0]['CUSTOMER_PAN'] = a[0].CUSTOMER.PAN_NO
    data[0]['EP_RM_NAME'] = a[0].EP_RM.NAME
    return JsonResponse(data,safe=False,status=200)

# def load_scheme(request):
#     data = list(MF_master.objects.values("SCHEME"))
#     return JsonResponse(data,safe=False)

def load_buy_mf(request):
    login_id = request.session['LOGIN_ID']
    user_type = request.session['USER_TYPE']
    user_type_id = request.session['USER_TYPE_ID']
    v = ["id","EP_RM","EP_RM__NAME","EP_RM__USERNAME","USER_TYPE","DATE","CUSTOMER","CUSTOMER__C_NAME","CUSTOMER__PAN_NO","CUSTOMER_STATUS","SCHEME_NAME","AMOUNT_INVESTED","MODE","BUY_TYPE"]
    if user_type == "bm" or user_type == "rm":
        final_list = get_under_mapped(request)
        logger.info(f"final list = {final_list}")
        data = list(Buy_MF.objects.filter(RM_EP__in=final_list).values(*v).order_by("-id"))
    if user_type == "admin" or user_type == "superadmin":
        data = list(Buy_MF.objects.values(*v).order_by("-id"))
    return JsonResponse({"data":data},safe=False)

@api_view(["POST"])
def delete_buy_mf(request,id):
    try:
        a = Buy_MF.objects.get(id=id)
        a.delete()
        return JsonResponse("Buy MF deleted successfully",safe=False,status=200)
    except Exception as e:
        logger.exception(e)
        return JsonResponse("Something went wrong",safe=False,status=500)


def admin_list(request):
    return render(request,"admin.html")

@api_view(["POST"])
def create_admin(request):
    try:
        login_id = request.session['LOGIN_ID']
        admin_name = request.POST.get("admin_name")
        username_a = request.POST.get("username_a")
        a_pass = request.POST.get("a_pass")
        c_pass = request.POST.get("c_pass")
        logger.info(f"""
            admin_name = {admin_name}
            username_a = {username_a}
            a_pass = {a_pass}
            c_pass = {c_pass}
        """)
        if User.objects.filter(USERNAME=username_a).exists():
            return JsonResponse("This Username is already Exists",safe=False,status=412)
        else:
            a = User.objects.create(
                NAME = admin_name,
                USERNAME = username_a,
                PASSWORD = c_pass,
                USER_TYPE = "admin",
                CREATED_BY = User.objects.get(id = login_id)
            )
            return JsonResponse("Admin Created Successfully",safe=False,status=200)
    except Exception as e:
        logger.exception(e)
        return JsonResponse("Something went wrong",safe=False,status=500)

def get_admin(request,id):
    data = list(User.objects.filter(id=id).values("id","NAME","USERNAME"))
    return JsonResponse(data,safe=False,status=200)

@api_view(["POST"])
def edit_admin(request,id):
    try:
        login_id = request.session['LOGIN_ID']
        admin_name = request.POST.get("admin_name")

        logger.info(f"""
            admin_name = {admin_name}
            """)
        a = User.objects.get(id=id)
        a.NAME = admin_name
        a.MODIFIED_BY = User.objects.get(id = login_id)
        a.save()
        return JsonResponse("Admin Edited Successfully",safe=False,status=200)
    except Exception as e:
        logger.exception(e)
        return JsonResponse("Something went wrong",safe=False,status=500)

def load_admin(request):
    data = list(User.objects.filter(USER_TYPE="admin").order_by("-id").values("id","NAME","USERNAME"))
    return JsonResponse({"data":data},safe=False)

def demat_account_page(request):
    return render(request,"demat_account.html")

@api_view(["POST"])
def add_demat_account(request):
    try:
        login_id        = request.session['LOGIN_ID']
        customer        = request.POST.get("customer")
        depositary_type = request.POST.get("depositary_type")
        acc_no          = request.POST.get("acc_no")
        client_id       = request.POST.get("client_id")
        demat_date      = request.POST.get("demat_date")
        commission      = request.POST.get("commission")

        logger.info(f"""
            customer = {customer}
            depositary_type = {depositary_type}
            acc_no = {acc_no}
            client_id = {client_id}
            demat_date = {demat_date}
            commission   = {commission}
        """)
        if Demat_account.objects.filter(DEMAT_CUST__id=customer).exists():
            return JsonResponse("This Customer Demat Account Already Exists",safe=False,status=500)
        else:
            Demat_account.objects.create(
                DEMAT_CUST          = Customer.objects.get(id=customer),
                DEPOSITORY_TYPE     = depositary_type,
                ACC_NO              = acc_no,
                CLIENT_ID           = client_id,
                ACC_DATE            = demat_date,
                COMMISSION          = commission,
                CREATED_BY          = User.objects.get(id = login_id)
            )
            return JsonResponse("demat Add successfully",safe=False,status=200)
    except Exception as e:
        logger.exception(e)
        return JsonResponse("Something Went Wrong",safe=False,status=500)

def get_demat_account(request,id):
    a = Demat_account.objects.filter(id=id)
    data = list(a.values())
    data[0]["DEMAT_CUST__C_NAME"] = a[0].DEMAT_CUST.C_NAME
    return JsonResponse(data,safe=False)

@api_view(["POST"])
def edit_demat_account(request,id):
    try:
        login_id        = request.session['LOGIN_ID']
        customer        = request.POST.get("customer")
        depositary_type = request.POST.get("depositary_type")
        acc_no          = request.POST.get("acc_no")
        client_id       = request.POST.get("client_id")
        demat_date      = request.POST.get("demat_date")
        commission      = request.POST.get("commission")

        logger.info(f"""
            customer = {customer}
            depositary_type = {depositary_type}
            acc_no = {acc_no}
            client_id = {client_id}
            demat_date = {demat_date}
            commission   = {commission}
        """)
        if Demat_account.objects.filter(DEMAT_CUST__id=customer).exclude(id=id).exists():
            return JsonResponse("This Customer Demat Account Already Exists",safe=False,status=500)
        else:
            edit                    = Demat_account.objects.get(id=id)
            edit.DEMAT_CUST         = Customer.objects.get(id=customer)
            edit.DEPOSITORY_TYPE    = depositary_type
            edit.ACC_NO             = acc_no
            edit.CLIENT_ID          = client_id
            edit.COMMISSION         = commission
            edit.CREATED_BY         = User.objects.get(id = login_id)
            edit.save()
            return JsonResponse("demat Edit successfully",safe=False,status=200)
    except Exception as e:
        logger.exception(e)
        return JsonResponse("Something Went Wrong",safe=False,status=500)

def load_demat_account(request):
    user_type = request.session['USER_TYPE']
    v = ["id","DEMAT_CUST__RM_EP__NAME","DEMAT_CUST__RM_EP__USERNAME","DEMAT_CUST__C_NAME","DEMAT_CUST__MOB_NO","DEPOSITORY_TYPE","ACC_NO","CLIENT_ID","ACC_DATE","COMMISSION"]
    if user_type == "bm" or user_type == "rm":
        final_list = get_under_mapped(request)
        # logger.info(f"final list = {final_list}")
        data = list(Demat_account.objects.filter(DEMAT_CUST__RM_EP__in=final_list).values(*v).order_by("-id"))
    else:
        data = list(Demat_account.objects.values(*v).order_by("-id"))
    return JsonResponse({"data":data},safe=False)

def transfer_customer(request):
    try:
        cust_id     = request.POST.get("trans_cust_id")
        user_type   = request.POST.get("u_type")
        user        = request.POST.get("user")
        logger.info(f"""
            cust_id     =   {cust_id}
            user_type   = {user_type}
            user        =      {user}
            """)
        if Customer.objects.filter(id=cust_id,RM_EP__id=user).exists():
            return JsonResponse("Customer Already mapped this User",safe=False,status=412)
        else:
            ut = User.objects.get(id=user)
            user_id = ut.USER_ID

            old_cust = Customer.objects.get(id=cust_id)
            pan_no = old_cust.PAN_NO
            old_cust.id = None
            old_cust.save()

            # old_cust.IS_DELETED = True
            # old_cust.save()
            Customer.objects.filter(PAN_NO=pan_no).update(IS_DELETED = True)
            # new_cust = Customer.objects.get(PAN_NO=pan_no,IS_DELETED = False)
            if user_type == "bm":
                old_cust.BM = Branch_Manager.objects.get(id=user_id)
                old_cust.RM = None
                old_cust.EP = None
                # old_cust.RM = Relationship_Manager.objects.get(id=None)
                # old_cust.EP = Easy_Partner.objects.get(id=None)
            if user_type == "rm":
                old_cust.BM = None
                old_cust.RM = Relationship_Manager.objects.get(id=user_id)
                old_cust.EP = None
            if user_type == "ep":
                old_cust.BM = None
                old_cust.RM = None
                old_cust.EP = Easy_Partner.objects.get(id=user_id)

            old_cust.RM_EP      = ut
            old_cust.TYPE       = user_type
            old_cust.IS_DELETED = False
            old_cust.CREATED_BY = User.objects.get(id=request.session['LOGIN_ID'])
            old_cust.save()
            return JsonResponse("sucesss",safe=False,status=200)
    except Exception as e:
        logger.exception(e)
        return JsonResponse("Something Went Wrong",safe=False,status=500)

def daily_buy_reports(request):
    return render(request,"daily_buy_reports.html")


def daily_reports_api(request):
    try:
        from_date = request.GET.get("from_date")
        to_date = request.GET.get("to_date")

        date_q = Q()
        final_q = Q()

        logger.info(f"""
            from_date = {from_date}
            to_date = {to_date}
            from_date_type = {type(to_date)}
            to_date_type = {type(to_date)}
        """)

        if from_date != "" and from_date != None:
            logger.info("iff")
            # manual_from_date = datetime.strptime(from_date, "%Y-%m-%d").date()
            # f_d = manual_from_date.strftime('%d')
            # f_m = manual_from_date.strftime('%m')
            # f_y = manual_from_date.strftime('%Y')

            # manual_to_date = datetime.strptime(to_date, "%Y-%m-%d").date()
            # t_d = manual_to_date.strftime('%d')
            # t_m = manual_to_date.strftime('%m')
            # t_y = manual_to_date.strftime('%Y')

            from_date = f"{from_date} 00:00:00"
            to_date = f"{to_date} 23:59:59"
            date_q = Q(CREATED_DATE__range = (from_date,to_date))
            # date_q = Q(CREATED_DATE__range = (datetime(int(f_y), int(f_m), int(f_d)),datetime(int(t_y), int(t_m), int(t_d))))
            # date_q = Q(CREATED_DATE__gte = datetime(int(f_y), int(f_m), int(f_d)),CREATED_DATE__lte = datetime(int(t_y), int(t_m), int(t_d)))
            final_q = date_q
        else:
            logger.info("else")
            today_date = date.today()
            # final_q = Q(CREATED_DATE__startswith =(today_date-timedelta(days=1)))
            final_q = Q(CREATED_DATE__startswith =(today_date))

        cust = ["CUSTOMER__C_NAME","CUSTOMER__MOB_NO","CUSTOMER__PAN_NO","TABLE_NAME","CREATED_DATE"]
        i           = ["id","CUSTOMER__RM_EP__USERNAME","CUSTOMER__RM_EP__NAME"]
        fd_mf       = [ "id","BUY_TYPE","EP_RM__USERNAME","EP_RM__NAME","TABLE_NAME"]
        demat_acc   = ["id","DEMAT_CUST__RM_EP__NAME","DEMAT_CUST__RM_EP__USERNAME","DEMAT_CUST__C_NAME","DEMAT_CUST__MOB_NO","DEMAT_CUST__PAN_NO","DEPOSITORY_TYPE","TABLE_NAME","COMMISSION","CREATED_DATE"]

        # ["id","EP_RM__NAME","EP_RM__USERNAME","USER_TYPE"]

        # c = logger.info(f"date = {b.CREATED_DATE.day}")
        insurance   = list(Insurance.objects.filter(final_q).values(*cust,*i,"GROSS_AMT"))
        buy_fd      = list(Buy_FD.objects.filter(final_q).values(*cust,*fd_mf,"AMOUNT"))
        buy_mf      = list(Buy_MF.objects.filter(final_q).values(*cust,*fd_mf,"AMOUNT_INVESTED"))
        demat       = list(Demat_account.objects.filter(final_q).values(*demat_acc))

        data = list(chain(insurance,buy_fd,buy_mf,demat))

        data = sorted(data, key=lambda x: x["CREATED_DATE"])
        return JsonResponse({"data":data},safe=False,status=200)
    except Exception as e:
        logger.exception(e)
        return JsonResponse("Something Went Wrong",safe=False,status=500)

# def daily_reports_filter_api(request):
#     from_date = request.GET.get("from_date")
#     to_date = request.GET.get("to_date")

#     cust = ["CUSTOMER__C_NAME","CUSTOMER__MOB_NO","CUSTOMER__PAN_NO","TABLE_NAME"]

#     i = ["id","CUSTOMER__RM_EP__USERNAME","CUSTOMER__RM_EP__NAME"]
#     fd_mf = [ "id","BUY_TYPE","EP_RM__USERNAME","EP_RM__NAME"]

#     logger.info(f"""
#         from_date = {from_date}
#         to_date = {to_date}
#     """)
#     date_q = Q()
#     final_q = Q()

#     if from_date != "" and from_date != None:
#         date_q = Q(INVOICE_DATE__range = [f"{from_date}", f"{to_date}"])
#         final_q = date_q

#     insurance   = list(Insurance.objects.filter().values(*cust,*i))
#     buy_fd      = list(Buy_FD.objects.filter(final_q).values(*cust,*fd_mf))
#     buy_mf      = list(Buy_MF.objects.filter(final_q).values(*cust,*fd_mf))

#     data = list(chain(insurance,buy_fd,buy_mf))

#     return JsonResponse({"data":data},safe=False)





