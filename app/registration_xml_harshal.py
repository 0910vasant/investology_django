from .models import Enc_password,CanCreationStatus, Registration_nominee_details, Registration_personal_details,Registration_bank_details,Registration_bank_details,Registration_communication_details
import logging
import datetime
from rest_framework.decorators import api_view,renderer_classes,APIView
from rest_framework_xml.renderers import XMLRenderer 
from rest_framework_xml.parsers import XMLParser 
from .serializers import CanModificationRegSerializers
from django.http import HttpResponse
import json
from django.views.decorators.csrf import csrf_exempt

from django.http import JsonResponse
from rest_framework.response import Response
logger = logging.getLogger(__name__)

def can_registration_api(id):
  profile         = Registration_personal_details.objects.get(id=id)
  # mfu             = Registration_mfu_details.objects.get(USER=id)
  # bank            = Registration_bank_details.objects.filter(USER=id,DEPOSITORY=False).first()
  # depository      = Registration_bank_details.objects.filter(USER=id,DEPOSITORY=True).first()
  communication   = Registration_communication_details.objects.get(USER=id)
  # kyc             = Registration_kyc_details.objects.get(USER=id)
  
  # holding_type = profile.ACCOUNT_TYPE.CODE
  # if holding_type == "SI":
  #   holder = f"""<HOLDER_TYPE>PR</HOLDER_TYPE> <!-- PR,SE,TH,GU -->
  #               <NAME>Kabilesh</NAME>
  #               <DOB>1983-01-20</DOB>
  #               <PAN_EXEMPT_FLAG>N</PAN_EXEMPT_FLAG>
  #               <PAN_PEKRN_NO></PAN_PEKRN_NO>"""
  #   pass
  # if holding_type == "JO":
  #   pass
  # if holding_type == "AS":
  #   pass
  
  if Registration_nominee_details.objects.filter(USER=id).exists():
    nominee_flag = "Y"
    nominee         = Registration_nominee_details.objects.get(USER=id)
  else:
    nominee_flag = "N"
  logger.info(f"nominee_flag = {nominee_flag}")
  # fatca           = Registration_fatca_details.objects.get(USER=id)
  enc_pass        = Enc_password.objects.last()

  tax_record = []
  # if fatca.TAX_RESIDENT_OF_OTHER_COUNTRY == "yes":
  #   for index,i in enumerate(fatca.TAX_DETAILS.all()):
  #     # logger.info(f"index = {index} i = {i}")
  #     tax_tmp =  f"""<TAX_RECORD>
  #                 <SEQ_NUM>{index+1}</SEQ_NUM>
  #                 <TAX_COUNTRY>{i.COUNTRY.CODE}</TAX_COUNTRY>
  #                 <TAX_COUNTRY_OTH>{i.OTHER_COUNTRY}</TAX_COUNTRY_OTH>
  #                 <TAX_REF_NO>{i.TAX_REFERENCE_NUMBER}</TAX_REF_NO>
  #                 <IDENTI_TYPE>{i.IDENTIFICATION_TYPE.CODE}</IDENTI_TYPE>
  #                 <IDENTI_TYPE_OTH>{i.OTHERS_IDENTIFICATION_TYPE}</IDENTI_TYPE_OTH>
  #               </TAX_RECORD>"""
  #     tax_record.append(tax_tmp)
  #   tax_record = '\n                '.join(tax_record)
    # logger.info(f"tax_record = {tax_record}")
  nominee_record = []
  if nominee_flag == "Y":
    for index,i in enumerate(nominee.NOMINEE_DETAILS.all()):
      logger.info(f"index = {index}")
      nominee_tmp = f"""<NOMINEE_RECORD>
            <SEQ_NUM>{index+1}</SEQ_NUM>
            <NOMINEE_NAME>{i.NOMINEE_NAME}</NOMINEE_NAME>
            <RELATION>{i.RELATIONSHIP_WITH_CLIENT}</RELATION>
            <PERCENTAGE>{i.NOMINEE_PERCENTAGE}</PERCENTAGE>
            <DOB>{i.NOMINEE_DOB}</DOB>
            <NOM_GURI_NAME>{'' if i.GUARDIAN_NAME != "None" else i.GUARDIAN_NAME}</NOM_GURI_NAME>
            <NOM_GURI_REL>{'' if i.GUARDIAN_RELATION != "None" else i.GUARDIAN_RELATION}</NOM_GURI_REL>
            <NOM_GURI_DOB>{'' if i.GUARDIAN_DOB != "None" else i.GUARDIAN_DOB}</NOM_GURI_DOB>
          </NOMINEE_RECORD>"""
      nominee_record.append(nominee_tmp)
    nominee_record = '\n          '.join(nominee_record)
  else:
    nominee_tmp = ""
    nominee_record = nominee_tmp

  
  bank_record = []
  for index,i in enumerate(bank.BANK_DETAILS.all()):
    if i.DEFAULT_BANK is True:
      bank_default_flag = "Y"
    else:
      bank_default_flag = "N"
    bank_record_tmp = f"""<BANK_RECORD>
          <SEQ_NUM>{index+1}</SEQ_NUM>
          <DEFAULT_ACC_FLAG>{bank_default_flag}</DEFAULT_ACC_FLAG>
          <ACCOUNT_NO>{i.ACC_NO}</ACCOUNT_NO>
          <ACCOUNT_TYPE>{i.ACC_TYPE.BANK_ACCOUNT_TYPE}</ACCOUNT_TYPE>
          <BANK_ID>065</BANK_ID>
          <MICR_CODE>{i.MICR_NO}</MICR_CODE>
          <IFSC_CODE>{i.NEFT_IFSC}</IFSC_CODE>
          <PROOF>{i.BANK_PROOF.CODE}</PROOF>
        </BANK_RECORD>"""
    bank_record.append(bank_record_tmp)
  bank_record = '\n                '.join(bank_record)
# <PRI_MOB_BELONGSTO>A</PRI_MOB_BELONGSTO>
# <PRI_EMAIL_BELONGSTO>A</PRI_EMAIL_BELONGSTO>
# <PAN_PEKRN_NO>{profile.PAN_NO}</PAN_PEKRN_NO>
  payload= f"""<?xml version="1.0" encoding="UTF-8"?>
  <CANIndFillEezzReq xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance" xsi:noNamespaceSchemaLocation="CANIndFillEezzReq.xsd">
    <REQ_HEADER>
      <ENTITY_ID>40007K</ENTITY_ID>
      <UNIQUE_ID>2</UNIQUE_ID>
      <REQUEST_TYPE>CANINDREG</REQUEST_TYPE>
      <LOG_USER_ID>EASYINVUAT</LOG_USER_ID>
      <EN_ENCR_PASSWORD>{enc_pass.ENC_PASSWORD}</EN_ENCR_PASSWORD>
      <VERSION_NO>1.00</VERSION_NO>
      <TIMESTAMP>2023-01-10T11:15:30</TIMESTAMP>
    </REQ_HEADER>
    <REQ_BODY>
      <REQ_EVENT>CR</REQ_EVENT>
      <!-- CR - CAN CREATION EVENT , CM  CAN Modification Event-->
      <CAN></CAN>
      <!--  Only for CAN Modification -->
      <REG_TYPE>E</REG_TYPE>
      <!--  Physical,Electronic (P,E) -->
      <PROOF_UPLOAD_BY_CAN>N</PROOF_UPLOAD_BY_CAN>
      <!--  Y-YES ,N - NO -->
      <ENABLE_ONLINE_ACCESS_FLAG>Y</ENABLE_ONLINE_ACCESS_FLAG>
      <!--  Y-YES ,N - NO -->
      <ENTITY_EMAIL_DETAILS>
          <EMAIL_ID>{profile.EMAIL}</EMAIL_ID>
          <EMAIL_ID></EMAIL_ID>
      </ENTITY_EMAIL_DETAILS>
      <HOLDING_TYPE>{mfu.HOLDING_NATURE.CODE}</HOLDING_TYPE>
      <INV_CATEGORY>{mfu.INVESTOR_CATEGORY.CODE}</INV_CATEGORY>
      <TAX_STATUS>{mfu.TAX_STATUS.TAX_STATUS_CODE}</TAX_STATUS>
      <HOLDER_COUNT>1</HOLDER_COUNT>
      <HOLDER_RECORDS>
        <HOLDER_RECORD>
          <HOLDER_TYPE>PR</HOLDER_TYPE>
            <!-- PR,SE,TH,GU -->
            <NAME>{mfu.PRIMARY_HOLDER_NAME}</NAME>
            <DOB>{mfu.PRIMARY_HOLDER_DOB}</DOB>
            <PAN_EXEMPT_FLAG>N</PAN_EXEMPT_FLAG>
            <PAN_PEKRN_NO>{profile.PAN_NO}</PAN_PEKRN_NO>
            <AADHAAR_NO></AADHAAR_NO>
            <!-- As of version 5.5 of eCAN specification, this should be blank always. -->
            <RELATIONSHIP></RELATIONSHIP>
            <!-- Applicable only for Gaurdian Holder -->
            <REL_PROOF></REL_PROOF>
            <!-- Applicable only for Gaurdian Holder -->
            <CONTACT_DETAIL>
              <RES_ISD></RES_ISD>
              <RES_STD></RES_STD>
              <RES_PHONE_NO></RES_PHONE_NO>
              <MOB_ISD_CODE></MOB_ISD_CODE>
              <PRI_MOB_NO>{profile.MOBILE}</PRI_MOB_NO>
              
              <!--  S-SELF,F-FAMILY -->
              <ALT_MOB_NO></ALT_MOB_NO>
              <OFF_ISD></OFF_ISD>
              <OFF_STD></OFF_STD>
              <OFF_PHONE_NO></OFF_PHONE_NO>
              <PRI_EMAIL>{profile.EMAIL}</PRI_EMAIL>
              
              <!--  S-SELF,F-FAMILY -->
              <ALT_EMAIL></ALT_EMAIL>
            </CONTACT_DETAIL>
            <OTHER_DETAIL>
              <GROSS_INCOME></GROSS_INCOME>
              <NET_WORTH></NET_WORTH>
              <NET_DATE></NET_DATE>
              <SOURCE_OF_WEALTH></SOURCE_OF_WEALTH>
              <SOURCE_OF_WEALTH_OTH></SOURCE_OF_WEALTH_OTH>
              <KRA_ADDR_TYPE>{kyc.KRA_ADDRESS_TYPE.CODE}</KRA_ADDR_TYPE>
              <OCCUPATION>{kyc.OCCUPATION.CODE}</OCCUPATION>
              <OCCUPATION_OTH></OCCUPATION_OTH>
              <PEP>NA</PEP>
              <ANY_OTH_INFO></ANY_OTH_INFO>
            </OTHER_DETAIL>
            <FATCA_DETAIL>
              <BIRTH_CITY>{fatca.BIRTH_CITY}</BIRTH_CITY>
              <BIRTH_COUNTRY>{fatca.BIRTH_COUNTRY.CODE}</BIRTH_COUNTRY>
              <BIRTH_COUNTRY_OTH></BIRTH_COUNTRY_OTH>
              <CITIZENSHIP>{fatca.CITIZENSHIP.CODE}</CITIZENSHIP>
              <CITIZENSHIP_OTH></CITIZENSHIP_OTH>
              <NATIONALITY>{fatca.NATIONALITY.CODE}</NATIONALITY>
              <NATIONALITY_OTH></NATIONALITY_OTH>
              <TAX_RES_FLAG>{fatca.TAX_RESIDENT_OF_OTHER_COUNTRY[0].upper()}</TAX_RES_FLAG>
              <TAXS_RECORDS>
                <!--Multiple Record-->
                
                {tax_record}
              </TAXS_RECORDS>
            </FATCA_DETAIL>
        </HOLDER_RECORD>
      </HOLDER_RECORDS>
      <ARN_DETAILS>
      <!--  RIA Code need to add -->
      <ARN_NO></ARN_NO>
      <RIA_CODE></RIA_CODE>
      <!-- RIA Code -->
      <EUIN_CODE></EUIN_CODE>
      </ARN_DETAILS>
      <BANK_DETAILS>
      <!--Multiple Record-->
        {bank_record}
      </BANK_DETAILS>
      <NOMINEE_DETAILS>
        <NOM_DECL_LVL>C</NOM_DECL_LVL>
        <NOMIN_OPT_FLAG>{nominee_flag}</NOMIN_OPT_FLAG>
        <NOM_VERIFY_TYPE>E</NOM_VERIFY_TYPE>
        <NOMINEES_RECORDS>
          {nominee_record}
        </NOMINEES_RECORDS>
      </NOMINEE_DETAILS>
    </REQ_BODY>
  </CANIndFillEezzReq>
  """
  return payload


def registration_anyone_survivor(id):
  profile = Registration_personal_details.objects.get(id=id)
  pass


def registration_joint(id):
  profile = Registration_personal_details.objects.get(id=id)
  pass


# To check Status of Can of User
def can_creation_status(pk):
  try:
    user = Registration_personal_details.objects.get(pk=pk)
    status = CanCreationStatus.objects.get(USER=user)
    can_status=status.CAN_STATUS
    return JsonResponse(data=can_status,status=200)
  except Exception as e:
    logger.exception(e)
    return JsonResponse("Something Went Wrong",safe=False,status=500)

# @api_view(['POST'])
# @renderer_classes((XMLRenderer))
# def can_modification_api(request,pk):
#   # parser_classes = [XMLParser]
#   # renderer_classes = [XMLRenderer]
#   user=Registration_personal_details.objects.filter(pk=pk)
#   logger.info(f"user={user}")
#   serializers=CanModificationRegSerializers(user)
#   logger.info(f"user={serializers.data}")
#   # logger.info(f"user={user}")
#   return Response("",status=200)

# class CanModification(APIView):
#     renderer_classes = [XMLRenderer]
#     def get(self, request,pk):
#         user=Registration_personal_details.objects.filter(pk=pk)
#         serializer = CanModificationRegSerializers(user, many=True)
#         return Response(serializer.data)
# @api_view(['POST'])
@csrf_exempt
@api_view(['PUT'])
def can_modification_api(request):
    data = json.loads(request.body)
    holder_detail_holding_type = data.get("Holder_Detail", {}).get("HOLDING_TYPE", "")
    holder_detail_inv_category = data.get("Holder_Detail", {}).get("INV_CATEGORY", "")
    holder_detail_tax_status = data.get("Holder_Detail", {}).get("TAX_STATUS", "")
    holder_detail_holder_count = data.get("Holder_Detail", {}).get("HOLDER_COUNT", "")
    holder_record_detail_holder_type = data.get("Holder_Record_Detail", {}).get("HOLDER_TYPE", "")
    holder_record_detail_name = data.get("Holder_Record_Detail", {}).get("NAME", "")
    holder_record_detail_dob = data.get("Holder_Record_Detail", {}).get("DOB", "")
    holder_record_detail_pan_exempt_flag = data.get("Holder_Record_Detail", {}).get("PAN_EXEMPT_FLAG", "")
    holder_record_detail_pan_pekrn_no = data.get("Holder_Record_Detail", {}).get("PAN_PEKRN_NO", "")
    holder_record_detail_aadhaar_no = data.get("Holder_Record_Detail", {}).get("AADHAAR_NO", "")
    holder_record_detail_relationship = data.get("Holder_Record_Detail", {}).get("RELATIONSHIP", "")
    holder_record_detail_rel_proof = data.get("Holder_Record_Detail", {}).get("REL_PROOF", "")
    holder_record_detail_nom_ver_flag = data.get("Holder_Record_Detail", {}).get("NOM_VER_FLAG", "")
    holder_kyc_detail_kyc_status = data.get("Holder_KYC_Detail", {}).get("KYC_STATUS", "")
    res_addr_detail_addr1 = data.get("RES_ADDR_DETAIL", {}).get("ADDR1", "")
    res_addr_detail_addr2 = data.get("RES_ADDR_DETAIL", {}).get("ADDR2", "")
    res_addr_detail_addr3 = data.get("RES_ADDR_DETAIL", {}).get("ADDR3", "")
    res_addr_detail_city = data.get("RES_ADDR_DETAIL", {}).get("CITY", "")
    res_addr_detail_pincode = data.get("RES_ADDR_DETAIL", {}).get("PINCODE", "")
    res_addr_detail_state = data.get("RES_ADDR_DETAIL", {}).get("STATE", "")
    res_addr_detail_country = data.get("RES_ADDR_DETAIL", {}).get("COUNTRY", "")
    per_addr_detail_addr1 = data.get("PER_ADDR_DETAIL", {}).get("ADDR1", "")
    per_addr_detail_addr2 = data.get("PER_ADDR_DETAIL", {}).get("ADDR2", "")
    per_addr_detail_addr3 = data.get("PER_ADDR_DETAIL", {}).get("ADDR3", "")
    per_addr_detail_city = data.get("PER_ADDR_DETAIL", {}).get("CITY", "")
    per_addr_detail_pincode = data.get("PER_ADDR_DETAIL", {}).get("PINCODE", "")
    per_addr_detail_state = data.get("PER_ADDR_DETAIL", {}).get("STATE", "")
    per_addr_detail_country = data.get("PER_ADDR_DETAIL", {}).get("COUNTRY", "")
    holder_contact_detail_res_isd = data.get("Holder_Contact_Detail", {}).get("RES_ISD", "")
    holder_contact_detail_res_std = data.get("Holder_Contact_Detail", {}).get("RES_STD", "")
    holder_contact_detail_res_phone_no = data.get("Holder_Contact_Detail", {}).get("RES_PHONE_NO", "")
    holder_contact_detail_mob_isd_code = data.get("Holder_Contact_Detail", {}).get("MOB_ISD_CODE", "")
    holder_contact_detail_pri_mob_no = data.get("Holder_Contact_Detail", {}).get("PRI_MOB_NO", "")
    holder_contact_detail_pri_mob_belongsto = data.get("Holder_Contact_Detail", {}).get("PRI_MOB_BELONGSTO", "")
    holder_contact_detail_alt_mob_no = data.get("Holder_Contact_Detail", {}).get("ALT_MOB_NO", "")
    holder_contact_detail_off_isd = data.get("Holder_Contact_Detail", {}).get("OFF_ISD", "")
    holder_contact_detail_off_std = data.get("Holder_Contact_Detail", {}).get("OFF_STD", "")
    holder_contact_detail_off_phone_no = data.get("Holder_Contact_Detail", {}).get("OFF_PHONE_NO", "")
    holder_contact_detail_pri_email = data.get("Holder_Contact_Detail", {}).get("PRI_EMAIL", "")
    holder_contact_detail_pri_email_belongsto = data.get("Holder_Contact_Detail", {}).get("PRI_EMAIL_BELONGSTO", "")
    holder_contact_detail_alt_email = data.get("Holder_Contact_Detail", {}).get("ALT_EMAIL", "")
    holder_contact_detail_pri_mob_ver_flag = data.get("Holder_Contact_Detail", {}).get("PRI_MOB_VER_FLAG", "")
    holder_contact_detail_pri_email_ver_flag = data.get("Holder_Contact_Detail", {}).get("PRI_EMAIL_VER_FLAG", "")
    holder_contact_detail_pri_mob_ip_addr = data.get("Holder_Contact_Detail", {}).get("PRI_MOB_IP_ADDR", "")
    holder_contact_detail_pri_email_ip_addr = data.get("Holder_Contact_Detail", {}).get("PRI_EMAIL_IP_ADDR", "")
    holder_contact_detail_pri_email_ver_ts = data.get("Holder_Contact_Detail", {}).get("PRI_EMAIL_VER_TS", "")
    holder_contact_pri_mob_ver_ts = data.get("Holder_Contact", {}).get("PRI_MOB_VER_TS", "")
    additional_kyc_details_gross_income = data.get("Additional_KYC_Details", {}).get("GROSS_INCOME", "")
    additional_kyc_details_net_worth = data.get("Additional_KYC_Details", {}).get("NET_WORTH", "")
    additional_kyc_details_net_date = data.get("Additional_KYC_Details", {}).get("NET_DATE", "")
    additional_kyc_details_source_of_wealth = data.get("Additional_KYC_Details", {}).get("SOURCE_OF_WEALTH", "")
    additional_kyc_details_source_of_wealth_oth = data.get("Additional_KYC_Details", {}).get("SOURCE_OF_WEALTH_OTH", "")
    additional_kyc_details_kra_addr_type = data.get("Additional_KYC_Details", {}).get("KRA_ADDR_TYPE", "")
    additional_kyc_details_occupation = data.get("Additional_KYC_Details", {}).get("OCCUPATION", "")
    additional_kyc_details_occupation_oth = data.get("Additional_KYC_Details", {}).get("OCCUPATION_OTH", "")
    additional_kyc_details_pep = data.get("Additional_KYC_Details", {}).get("PEP", "")
    additional_kyc_details_any_oth_info = data.get("Additional_KYC_Details", {}).get("ANY_OTH_INFO", "")
    fatca_detail_birth_city = data.get("FATCA_Detail", {}).get("BIRTH_CITY", "")
    fatca_detail_birth_country = data.get("FATCA_Detail", {}).get("BIRTH_COUNTRY", "")
    fatca_detail_birth_country_oth = data.get("FATCA_Detail", {}).get("BIRTH_COUNTRY_OTH", "")
    fatca_detail_citizenship = data.get("FATCA_Detail", {}).get("CITIZENSHIP", "")
    fatca_detail_citizenship_oth = data.get("FATCA_Detail", {}).get("CITIZENSHIP_OTH", "")
    fatca_detail_nationality = data.get("FATCA_Detail", {}).get("NATIONALITY", "")
    fatca_detail_nationality_oth = data.get("FATCA_Detail", {}).get("NATIONALITY_OTH", "")
    fatca_detail_tax_res_flag = data.get("FATCA_Detail", {}).get("TAX_RES_FLAG", "")
    fatca_tax_record_seq_num = data.get("FATCA_Tax_Record", {}).get("SEQ_NUM", "")
    fatca_tax_record_tax_country = data.get("FATCA_Tax_Record", {}).get("TAX_COUNTRY", "")
    fatca_tax_record_tax_country_oth = data.get("FATCA_Tax_Record", {}).get("TAX_COUNTRY_OTH", "")
    fatca_tax_record_tax_ref_no = data.get("FATCA_Tax_Record", {}).get("TAX_REF_NO", "")
    fatca_tax_record_identi_type = data.get("FATCA_Tax_Record", {}).get("IDENTI_TYPE", "")
    fatca_tax_record_identi_type_oth = data.get("FATCA_Tax_Record", {}).get("IDENTI_TYPE_OTH", "")
    arn_details_arn_no = data.get("ARN_Details", {}).get("ARN_NO", "")
    arn_details_ria_code = data.get("ARN_Details", {}).get("RIA_CODE", "")
    arn_details_euin_code = data.get("ARN_Details", {}).get("EUIN_CODE", "")
    dp_details_nsdl_dp_id = data.get("DP_Details", {}).get("NSDL_DP_ID", "")
    dp_details_nsdl_client_id = data.get("DP_Details", {}).get("NSDL_CLIENT_ID", "")
    dp_details_nsdl_proof_id = data.get("DP_Details", {}).get("NSDL_PROOF_ID", "")
    dp_details_nsdl_ver_flag = data.get("DP_Details", {}).get("NSDL_VER_FLAG", "")
    dp_details_cdsl_dp_id = data.get("DP_Details", {}).get("CDSL_DP_ID", "")
    dp_details_cdsl_client_id = data.get("DP_Details", {}).get("CDSL_CLIENT_ID", "")
    dp_details_cdsl_proof_id = data.get("DP_Details", {}).get("CDSL_PROOF_ID", "")
    dp_details_cdsl_ver_flag = data.get("DP_Details", {}).get("CDSL_VER_FLAG", "")
    bank_details= data.get("Bank_Details",[])
    bank_detail_xml=""
    for bank in bank_details:
      bank_detail_xml+=f"""
        <Bank_Details>
            <SEQ_NUM>{bank.get('SEQ_NUM','')}</SEQ_NUM>
            <DEFAULT_ACC_FLAG>{bank.get('DEFAULT_ACC_FLAG','')}</DEFAULT_ACC_FLAG>
            <ACCOUNT_NO>{bank.get('ACCOUNT_NO','')}</ACCOUNT_NO>
            <ACCOUNT_TYPE>{bank.get('ACCOUNT_TYPE','')}</ACCOUNT_TYPE>
            <BANK_ID>{bank.get('BANK_ID','')}</BANK_ID>
            <MICR_CODE>{bank.get('MICR_CODE','')}</MICR_CODE>
            <IFSC_CODE>{bank.get('IFSC_CODE','')}</IFSC_CODE>
            <PROOF>{bank.get('PROOF','')}</PROOF>
            <RUP_VER_FLG>{bank.get('RUP_VER_FLG','')}</RUP_VER_FLG>
            <RUP_BENE_NAME>{bank.get('RUP_BENE_NAME','')}</RUP_BENE_NAME>
            <RUP_THRESHOLD>{bank.get('RUP_THRESHOLD','')}</RUP_THRESHOLD>
        </Bank_Details>
"""
    # for multiple Nominee Record Details 
    nominee_record_details = data.get("Nominee_Record_Details", [])
    nominee_record_details_xml = ""
    for record_detail in nominee_record_details:
        nominee_record_details_xml += f"""
        <Nominee_Record_Detail>
            <SEQ_NUM>{record_detail.get('SEQ_NUM', '')}</SEQ_NUM>
            <NOMINEE_NAME>{record_detail.get('NOMINEE_NAME', '')}</NOMINEE_NAME>
            <RELATION>{record_detail.get('RELATION', '')}</RELATION>
            <PERCENTAGE>{record_detail.get('PERCENTAGE', '')}</PERCENTAGE>
            <DOB>{record_detail.get('DOB', '')}</DOB>
            <NOM_GURI_NAME>{record_detail.get('NOM_GURI_NAME', '')}</NOM_GURI_NAME>
            <NOM_GURI_REL>{record_detail.get('NOM_GURI_REL', '')}</NOM_GURI_REL>
            <NOM_GURI_DOB>{record_detail.get('NOM_GURI_DOB', '')}</NOM_GURI_DOB>
        </Nominee_Record_Detail>
        """
    # for multiple Nominee  Details 
    nominee_details = data.get("Nominee_Details", [])
    nominee_details_xml = ""
    for nominee_detail in nominee_details:
        nominee_details_xml += f"""
        <Nominee_Detail>
            <NOM_DECL_LVL>{nominee_detail.get('NOM_DECL_LVL', '')}</NOM_DECL_LVL>
            <NOMIN_OPT_FLAG>{nominee_detail.get('NOMIN_OPT_FLAG', '')}</NOMIN_OPT_FLAG>
            <NOM_VERIFY_TYPE>{nominee_detail.get('NOM_VERIFY_TYPE', '')}</NOM_VERIFY_TYPE>
        </Nominee_Detail>
        """
    entity_id=data.get('entity_id',"")
    unique_id = data.get("UNIQUE_ID", "")
    request_type = data.get("REQUEST_TYPE", "")
    log_user_id = data.get("LOG_USER_ID", "")
    en_encr_password = data.get("EN_ENCR_PASSWORD", "")
    version_no = data.get("VERSION_NO", "")
    timestamp = datetime.datetime.now().isoformat()
    can_value=data.get("CAN","")
    reg_type=data.get("REG_TYPE","")
    proof_upload_by_can=data.get("PROOF_UPLOAD_BY_CAN","")
    enable_online_access_flag=data.get("ENABLE_ONLINE_ACCESS_FLAG","")
    



    payload= f"""
  <?xml version="1.0" encoding="UTF-8"?>
    <CANIndFillEezzReq xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance" xsi:noNamespaceSchemaLocation="CANIndFillEezzReq.xsd">
      <REQ_HEADER>
        <ENTITY_ID>{entity_id}</ENTITY_ID>
        <UNIQUE_ID>{unique_id}</UNIQUE_ID>
        <REQUEST_TYPE>{request_type}</REQUEST_TYPE>
        <LOG_USER_ID>{log_user_id}</LOG_USER_ID>
        <EN_ENCR_PASSWORD>{en_encr_password}</EN_ENCR_PASSWORD>
        <VERSION_NO>{version_no}</VERSION_NO>
        <TIMESTAMP>{timestamp}</TIMESTAMP>
      </REQ_HEADER>
      <REQ_BODY>
        <REQ_EVENT>CM</REQ_EVENT>
        <CAN></CAN>
        <!--  Only for CAN Modification -->
        <REG_TYPE>E</REG_TYPE>
        <!--  Physical,Electronic (P,E) -->
        <PROOF_UPLOAD_BY_CAN>N</PROOF_UPLOAD_BY_CAN>
        <!--  Y-YES ,N - NO -->
        <ENABLE_ONLINE_ACCESS_FLAG>Y</ENABLE_ONLINE_ACCESS_FLAG>
        <!--  Y-YES ,N - NO -->
        <ENTITY_EMAIL_DETAILS>
            <EMAIL_ID>gel@gmail.com</EMAIL_ID>
            <EMAIL_ID></EMAIL_ID>
        </ENTITY_EMAIL_DETAILS>
    <Holder_Detail>
          <HOLDING_TYPE>{holder_detail_holding_type}</HOLDING_TYPE>
          <INV_CATEGORY>{holder_detail_inv_category}</INV_CATEGORY>
          <TAX_STATUS>{holder_detail_tax_status}</TAX_STATUS>
          <HOLDER_COUNT>{holder_detail_holder_count}</HOLDER_COUNT>
      </Holder_Detail>
      <Holder_Record_Detail>
          <HOLDER_TYPE>{holder_record_detail_holder_type}</HOLDER_TYPE>
          <NAME>{holder_record_detail_name}</NAME>
          <DOB>{holder_record_detail_dob}</DOB>
          <PAN_EXEMPT_FLAG>{holder_record_detail_pan_exempt_flag}</PAN_EXEMPT_FLAG>
          <PAN_PEKRN_NO>{holder_record_detail_pan_pekrn_no}</PAN_PEKRN_NO>
          <AADHAAR_NO>{holder_record_detail_aadhaar_no}</AADHAAR_NO>
          <RELATIONSHIP>{holder_record_detail_relationship}</RELATIONSHIP>
          <REL_PROOF>{holder_record_detail_rel_proof}</REL_PROOF>
          <NOM_VER_FLAG>{holder_record_detail_nom_ver_flag}</NOM_VER_FLAG>
      </Holder_Record_Detail>
      <Holder_KYC_Detail>
          <KYC_STATUS>{holder_kyc_detail_kyc_status}</KYC_STATUS>
      </Holder_KYC_Detail>
      <RES_ADDR_DETAIL>
          <ADDR1>{res_addr_detail_addr1}</ADDR1>
          <ADDR2>{res_addr_detail_addr2}</ADDR2>
          <ADDR3>{res_addr_detail_addr3}</ADDR3>
          <CITY>{res_addr_detail_city}</CITY>
          <PINCODE>{res_addr_detail_pincode}</PINCODE>
          <STATE>{res_addr_detail_state}</STATE>
          <COUNTRY>{res_addr_detail_country}</COUNTRY>
      </RES_ADDR_DETAIL>
      <PER_ADDR_DETAIL>
          <ADDR1>{per_addr_detail_addr1}</ADDR1>
          <ADDR2>{per_addr_detail_addr2}</ADDR2>
          <ADDR3>{per_addr_detail_addr3}</ADDR3>
          <CITY>{per_addr_detail_city}</CITY>
          <PINCODE>{per_addr_detail_pincode}</PINCODE>
          <STATE>{per_addr_detail_state}</STATE>
          <COUNTRY>{per_addr_detail_country}</COUNTRY>
      </PER_ADDR_DETAIL>
      <Holder_Contact_Detail>
          <RES_ISD>{holder_contact_detail_res_isd}</RES_ISD>
          <RES_STD>{holder_contact_detail_res_std}</RES_STD>
          <RES_PHONE_NO>{holder_contact_detail_res_phone_no}</RES_PHONE_NO>
          <MOB_ISD_CODE>{holder_contact_detail_mob_isd_code}</MOB_ISD_CODE>
          <PRI_MOB_NO>{holder_contact_detail_pri_mob_no}</PRI_MOB_NO>
          <PRI_MOB_BELONGSTO>{holder_contact_detail_pri_mob_belongsto}</PRI_MOB_BELONGSTO>
          <ALT_MOB_NO>{holder_contact_detail_alt_mob_no}</ALT_MOB_NO>
          <OFF_ISD>{holder_contact_detail_off_isd}</OFF_ISD>
          <OFF_STD>{holder_contact_detail_off_std}</OFF_STD>
          <OFF_PHONE_NO>{holder_contact_detail_off_phone_no}</OFF_PHONE_NO>
          <PRI_EMAIL>{holder_contact_detail_pri_email}</PRI_EMAIL>
          <PRI_EMAIL_BELONGSTO>{holder_contact_detail_pri_email_belongsto}</PRI_EMAIL_BELONGSTO>
          <ALT_EMAIL>{holder_contact_detail_alt_email}</ALT_EMAIL>
          <PRI_MOB_VER_FLAG>{holder_contact_detail_pri_mob_ver_flag}</PRI_MOB_VER_FLAG>
          <PRI_EMAIL_VER_FLAG>{holder_contact_detail_pri_email_ver_flag}</PRI_EMAIL_VER_FLAG>
          <PRI_MOB_IP_ADDR>{holder_contact_detail_pri_mob_ip_addr}</PRI_MOB_IP_ADDR>
          <PRI_EMAIL_IP_ADDR>{holder_contact_detail_pri_email_ip_addr}</PRI_EMAIL_IP_ADDR>
          <PRI_EMAIL_VER_TS>{holder_contact_detail_pri_email_ver_ts}</PRI_EMAIL_VER_TS>
      </Holder_Contact_Detail>
      <Holder_Contact>
          <PRI_MOB_VER_TS>{holder_contact_pri_mob_ver_ts}</PRI_MOB_VER_TS>
      </Holder_Contact>
      <Additional_KYC_Details>
          <GROSS_INCOME>{additional_kyc_details_gross_income}</GROSS_INCOME>
          <NET_WORTH>{additional_kyc_details_net_worth}</NET_WORTH>
          <NET_DATE>{additional_kyc_details_net_date}</NET_DATE>
          <SOURCE_OF_WEALTH>{additional_kyc_details_source_of_wealth}</SOURCE_OF_WEALTH>
          <SOURCE_OF_WEALTH_OTH>{additional_kyc_details_source_of_wealth_oth}</SOURCE_OF_WEALTH_OTH>
          <KRA_ADDR_TYPE>{additional_kyc_details_kra_addr_type}</KRA_ADDR_TYPE>
          <OCCUPATION>{additional_kyc_details_occupation}</OCCUPATION>
          <OCCUPATION_OTH>{additional_kyc_details_occupation_oth}</OCCUPATION_OTH>
          <PEP>{additional_kyc_details_pep}</PEP>
          <ANY_OTH_INFO>{additional_kyc_details_any_oth_info}</ANY_OTH_INFO>
      </Additional_KYC_Details>
      <FATCA_Detail>
          <BIRTH_CITY>{fatca_detail_birth_city}</BIRTH_CITY>
          <BIRTH_COUNTRY>{fatca_detail_birth_country}</BIRTH_COUNTRY>
          <BIRTH_COUNTRY_OTH>{fatca_detail_birth_country_oth}</BIRTH_COUNTRY_OTH>
          <CITIZENSHIP>{fatca_detail_citizenship}</CITIZENSHIP>
          <CITIZENSHIP_OTH>{fatca_detail_citizenship_oth}</CITIZENSHIP_OTH>
          <NATIONALITY>{fatca_detail_nationality}</NATIONALITY>
          <NATIONALITY_OTH>{fatca_detail_nationality_oth}</NATIONALITY_OTH>
          <TAX_RES_FLAG>{fatca_detail_tax_res_flag}</TAX_RES_FLAG>
      </FATCA_Detail>
      <FATCA_Tax_Record>
          <SEQ_NUM>{fatca_tax_record_seq_num}</SEQ_NUM>
          <TAX_COUNTRY>{fatca_tax_record_tax_country}</TAX_COUNTRY>
          <TAX_COUNTRY_OTH>{fatca_tax_record_tax_country_oth}</TAX_COUNTRY_OTH>
          <TAX_REF_NO>{fatca_tax_record_tax_ref_no}</TAX_REF_NO>
          <IDENTI_TYPE>{fatca_tax_record_identi_type}</IDENTI_TYPE>
          <IDENTI_TYPE_OTH>{fatca_tax_record_identi_type_oth}</IDENTI_TYPE_OTH>
      </FATCA_Tax_Record>
      <ARN_Details>
          <ARN_NO>{arn_details_arn_no}</ARN_NO>
          <RIA_CODE>{arn_details_ria_code}</RIA_CODE>
          <EUIN_CODE>{arn_details_euin_code}</EUIN_CODE>
      </ARN_Details>
      <DP_Details>
          <NSDL_DP_ID>{dp_details_nsdl_dp_id}</NSDL_DP_ID>
          <NSDL_CLIENT_ID>{dp_details_nsdl_client_id}</NSDL_CLIENT_ID>
          <NSDL_PROOF_ID>{dp_details_nsdl_proof_id}</NSDL_PROOF_ID>
          <NSDL_VER_FLAG>{dp_details_nsdl_ver_flag}</NSDL_VER_FLAG>
          <CDSL_DP_ID>{dp_details_cdsl_dp_id}</CDSL_DP_ID>
          <CDSL_CLIENT_ID>{dp_details_cdsl_client_id}</CDSL_CLIENT_ID>
          <CDSL_PROOF_ID>{dp_details_cdsl_proof_id}</CDSL_PROOF_ID>
          <CDSL_VER_FLAG>{dp_details_cdsl_ver_flag}</CDSL_VER_FLAG>
      </DP_Details>
      {bank_detail_xml}
      {nominee_details_xml}
      {nominee_record_details_xml}
      </REQ_BODY>
    </CANIndFillEezzReq>
    """
    return HttpResponse(payload, content_type='application/xml')


