from .models import Enc_password, Registration_nominee_details, Registration_personal_details,Registration_mfu_details,Registration_holder_details,Registration_bank_details , Registration_nominee_details , Nominee_details, Header_Checklist
import logging
logger = logging.getLogger(__name__)

def can_registration_api(id,app_type,api_use):
  profile             = Registration_personal_details.objects.get(id=id)
  mfu                 = Registration_mfu_details.objects.get(USER=id)
  holder_details      = Registration_holder_details.objects.filter(USER=id,IS_DELETED=False)
  bank_details        = Registration_bank_details.objects.filter(USER=id,IS_DELETED=False)
  header_checklist    = Header_Checklist.objects.get(APP_TYPE=app_type,CHECKLIST_USE_FOR="can",IS_DELETED=False)
 
  if mfu.INVESTOR_CATEGORY.CODE != "M":
    r_nominee_detail    = Registration_nominee_details.objects.get(USER=id,IS_DELETED=False)
  nominee_detail      = Nominee_details.objects.filter(USER=id,IS_DELETED=False)
  # enc_pass            = Enc_password.objects.last()
  holder_record = []
  bank_record = []
  nominee_record = []
 # <PRI_MOB_BELONGSTO> {'' if i.PRI_MOB_BELONGSTO is None or app_type == 'prod' else 'SE'}</PRI_MOB_BELONGSTO> <!--  SE-SELF,F-FAMILY -->
#  <PRI_EMAIL_BELONGSTO>{'' if i.PRI_EMAIL_BELONGSTO is None or app_type == 'prod' else 'SE'}</PRI_EMAIL_BELONGSTO> <!--  SE-SELF,F-FAMILY -->
  for i in holder_details:
    record = f"""<HOLDER_RECORD>
                <HOLDER_TYPE>{i.HOLDER_TYPE}</HOLDER_TYPE> <!-- PR,SE,TH,GU -->
                    <NAME>{i.HOLDER_NAME}</NAME>
                    <DOB>{i.HOLDER_DOB}</DOB>
                    <PAN_EXEMPT_FLAG>N</PAN_EXEMPT_FLAG>
                    <PAN_PEKRN_NO>{'' if i.PAN_NO is None else i.PAN_NO}</PAN_PEKRN_NO>
                    <AADHAAR_NO></AADHAAR_NO> <!-- As of version 5.5 of eCAN specification, this should be blank always. -->
                    <RELATIONSHIP>{'' if i.RELATIONSHIP_WITH_MINOR is None else i.RELATIONSHIP_WITH_MINOR}</RELATIONSHIP> <!-- Applicable only for Gaurdian Holder -->
                    <REL_PROOF>{'' if i.PROOF_OF_RELATIONSHIP is None else i.PROOF_OF_RELATIONSHIP}</REL_PROOF> <!-- Applicable only for Gaurdian Holder -->
                    <NOM_VER_FLAG></NOM_VER_FLAG>
				            <NOM_VER_IP></NOM_VER_IP>
                    <CONTACT_DETAIL>
                        <RES_ISD>{'' if i.RESIDENCE_ISD is None else i.RESIDENCE_ISD}</RES_ISD>
                        <RES_STD>{'' if i.RESIDENCE_STD is None else i.RESIDENCE_STD}</RES_STD>
                        <RES_PHONE_NO>{'' if i.RESIDENCE_PHONE_NO is None or i.RESIDENCE_PHONE_NO =="null" else i.RESIDENCE_PHONE_NO}</RES_PHONE_NO>
                        <MOB_ISD_CODE>{'' if i.MOB_ISD_CODE is None else i.MOB_ISD_CODE}</MOB_ISD_CODE>
                        <PRI_MOB_NO>{'' if i.PRI_MOB_NO is None else i.PRI_MOB_NO}</PRI_MOB_NO>
                        <PRI_MOB_BELONGSTO>{'SE' if i.PRI_MOB_BELONGSTO == 'S' or i.PRI_MOB_BELONGSTO == 'SE' else i.PRI_MOB_BELONGSTO}</PRI_MOB_BELONGSTO> <!--  S-SELF,F-FAMILY -->
                        <ALT_MOB_NO>{'' if i.ALT_MOB_NO is None else i.ALT_MOB_NO}</ALT_MOB_NO>
                        <OFF_ISD>{'' if i.OFF_ISD is None else i.OFF_ISD}</OFF_ISD>
                        <OFF_STD>{'' if i.OFF_STD is None else i.OFF_STD}</OFF_STD>
                        <OFF_PHONE_NO>{'' if i.OFF_PHONE_NO is None else i.OFF_PHONE_NO}</OFF_PHONE_NO>
                        <PRI_EMAIL>{'' if i.PRI_EMAIL is None else i.PRI_EMAIL}</PRI_EMAIL>
                        <PRI_EMAIL_BELONGSTO>{'SE' if i.PRI_EMAIL_BELONGSTO == 'S' or i.PRI_EMAIL_BELONGSTO == 'SE' else i.PRI_EMAIL_BELONGSTO}</PRI_EMAIL_BELONGSTO> <!--  SE-SELF,F-FAMILY -->
                        <ALT_EMAIL{'' if i.ALT_EMAIL is None else i.ALT_EMAIL}></ALT_EMAIL>
                        <PRI_MOB_VER_FLAG></PRI_MOB_VER_FLAG>
                        <PRI_EMAIL_VER_FLAG></PRI_EMAIL_VER_FLAG>
                        <PRI_MOB_IP_ADDR></PRI_MOB_IP_ADDR>
                        <PRI_EMAIL_IP_ADDR></PRI_EMAIL_IP_ADDR>
                        <PRI_MOB_VER_TS></PRI_MOB_VER_TS>
                        <PRI_EMAIL_VER_TS></PRI_EMAIL_VER_TS>
                    </CONTACT_DETAIL>
                    <OTHER_DETAIL>
                      <GROSS_INCOME>{'' if i.INCOME_TYPE != "gross_annual_income" else i.GROSS_ANNUAL_INCOME.CODE}</GROSS_INCOME>
                      <NET_WORTH>{'' if i.NETWORTH_IN_RUPEES is None else i.NETWORTH_IN_RUPEES}</NET_WORTH>
                      <NET_DATE>{'' if i.NETWORTH_AS_ON_DATE is None else i.NETWORTH_AS_ON_DATE}</NET_DATE>
                      <SOURCE_OF_WEALTH>{'' if i.SOURCE_OF_WEALTH is None else i.SOURCE_OF_WEALTH.CODE}</SOURCE_OF_WEALTH>
                      <SOURCE_OF_WEALTH_OTH>{'' if i.SOURCE_OF_WEALTH_OTHERS is None else i.SOURCE_OF_WEALTH_OTHERS}</SOURCE_OF_WEALTH_OTH>
                      <KRA_ADDR_TYPE>{'' if i.KRA_ADDRESS_TYPE is None else i.KRA_ADDRESS_TYPE.CODE}</KRA_ADDR_TYPE>
                      <OCCUPATION>{'' if i.OCCUPATION is None else i.OCCUPATION.CODE}</OCCUPATION>
                      <OCCUPATION_OTH>{'' if i.OCCUPATION_OTHERS is None else i.OCCUPATION_OTHERS}</OCCUPATION_OTH>
                      <PEP>{'' if i.PEP_STATUS is None else i.PEP_STATUS.CODE}</PEP>
                      <ANY_OTH_INFO>{i.ANY_OTHER_INFORMATION}</ANY_OTH_INFO>
                    </OTHER_DETAIL>
                    <FATCA_DETAIL>
                      <BIRTH_CITY>{'' if i.BIRTH_CITY is None else i.BIRTH_CITY}</BIRTH_CITY>
                      <BIRTH_COUNTRY>{'' if i.BIRTH_COUNTRY is None else i.BIRTH_COUNTRY.CODE}</BIRTH_COUNTRY>
                      <BIRTH_COUNTRY_OTH>{'' if i.BIRTH_COUNTRY_OTH is None else i.BIRTH_COUNTRY_OTH}</BIRTH_COUNTRY_OTH>
                      <CITIZENSHIP>{'' if i.CITIZENSHIP is None else i.CITIZENSHIP.CODE}</CITIZENSHIP>
                      <CITIZENSHIP_OTH>{'' if i.CITIZENSHIP_OTH is None else i.CITIZENSHIP_OTH}</CITIZENSHIP_OTH>
                      <NATIONALITY>{'' if i.NATIONALITY is None else i.NATIONALITY.CODE}</NATIONALITY>
                      <NATIONALITY_OTH>{'' if i.NATIONALITY_OTH is None else i.NATIONALITY_OTH}</NATIONALITY_OTH>
                      <TAX_RES_FLAG>{'' if i.TAX_RES_FLAG is None else i.TAX_RES_FLAG}</TAX_RES_FLAG>
                      <TAXS_RECORDS>
                          <!--Multiple Record-->
                          <TAX_RECORD>
                              <SEQ_NUM>{'' if i.TAX_RES_FLAG == "N" else "1"}</SEQ_NUM>
                              <TAX_COUNTRY>{'' if i.TAX_COUNTRY is None else i.TAX_COUNTRY.CODE}</TAX_COUNTRY>
                              <TAX_COUNTRY_OTH>{'' if i.TAX_COUNTRY_OTH is None else i.TAX_COUNTRY_OTH}</TAX_COUNTRY_OTH>
                              <TAX_REF_NO>{'' if i.TAX_REF_NO is None else i.TAX_REF_NO}</TAX_REF_NO>
                              <IDENTI_TYPE>{'' if i.IDENTI_TYPE is None else i.IDENTI_TYPE.CODE}</IDENTI_TYPE>
                              <IDENTI_TYPE_OTH>{'' if i.IDENTI_TYPE_OTH is None else i.IDENTI_TYPE_OTH}</IDENTI_TYPE_OTH>
                          </TAX_RECORD>
                      </TAXS_RECORDS>
                    </FATCA_DETAIL>
                </HOLDER_RECORD>"""
    holder_record.append(record)
  holder_record = '\n                '.join(holder_record)

  for  index, i in enumerate(bank_details,start=1):
    record=f"""<BANK_RECORD>
                <SEQ_NUM>{index}</SEQ_NUM>
                <DEFAULT_ACC_FLAG>{"Y" if i.DEFAULT_BANK else "N"}</DEFAULT_ACC_FLAG>
                <ACCOUNT_NO>{i.ACC_NO}</ACCOUNT_NO>
                <ACCOUNT_TYPE>{i.ACC_TYPE.BANK_ACCOUNT_TYPE}</ACCOUNT_TYPE>
                <BANK_ID>{i.BANK_NAME.CODE}</BANK_ID>
                <MICR_CODE>{i.MICR_NO}</MICR_CODE>
                <IFSC_CODE>{i.IFSC_CODE}</IFSC_CODE>
                <PROOF>{i.BANK_PROOF.CODE}</PROOF>
                <RUP_VER_FLG></RUP_VER_FLG>
                <RUP_BENE_NAME></RUP_BENE_NAME>
                <RUP_THRESHOLD></RUP_THRESHOLD>
                <RUP_IP_ADDR></RUP_IP_ADDR>
                <RUP_TS></RUP_TS>
            </BANK_RECORD>"""
    bank_record.append(record)
  bank_record = '\n                '.join(bank_record)

 
  if mfu.INVESTOR_CATEGORY.CODE != "M":
    for  index, i in enumerate(nominee_detail,start=1):
      record=f"""<NOMINEE_RECORD>
                  <SEQ_NUM>{index}</SEQ_NUM>
                  <NOMINEE_NAME>{i.NOMINEE_NAME}</NOMINEE_NAME>
                  <RELATION>{i.RELATIONSHIP_WITH_CLIENT}</RELATION>
                  <PERCENTAGE>{i.NOMINEE_PERCENTAGE}</PERCENTAGE>
                  <DOB>{i.NOMINEE_DOB}</DOB>
                  <NOM_GURI_NAME>{i.GUARDIAN_NAME if i.NOMINEE_IS_MINOR else ''}</NOM_GURI_NAME>
                  <NOM_GURI_REL>{i.GUARDIAN_RELATION if i.NOMINEE_IS_MINOR else ''}</NOM_GURI_REL>
                  <NOM_GURI_DOB>{i.GUARDIAN_DOB if i.NOMINEE_IS_MINOR else ''}</NOM_GURI_DOB>
              </NOMINEE_RECORD>"""
      nominee_record.append(record)
    nominee_record = '\n                '.join(nominee_record)
  payload = f"""<?xml version="1.0" encoding="UTF-8"?>
              <CANIndFillEezzReq xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance" xsi:noNamespaceSchemaLocation="CANIndFillEezzReq.xsd">
                <REQ_HEADER>
                  <ENTITY_ID>{header_checklist.ENTITY_ID}</ENTITY_ID>
                  <UNIQUE_ID>2</UNIQUE_ID>
                  <REQUEST_TYPE>CANINDREG</REQUEST_TYPE>
                  <LOG_USER_ID>{header_checklist.LOGIN_ID}</LOG_USER_ID>
                  <EN_ENCR_PASSWORD>{header_checklist.EN_ENCR_PASSWORD}</EN_ENCR_PASSWORD>
                  <VERSION_NO>1.00</VERSION_NO>
                  <TIMESTAMP>2023-01-10T11:15:30</TIMESTAMP>
                </REQ_HEADER>
                <REQ_BODY>
                  <REQ_ENT_VIA></REQ_ENT_VIA>
                  <REQ_EVENT>{'CM' if api_use == 'CM' else 'CR'}</REQ_EVENT> <!-- CR - CAN CREATION EVENT , CM  CAN Modification Event-->
                  <CAN>{profile.CAN if api_use == 'CM' else ''}</CAN> <!--  Only for CAN Modification -->
                  <REG_TYPE>E</REG_TYPE> <!--  Physical,Electronic (P,E) -->
                  <PROOF_UPLOAD_BY_CAN>Y</PROOF_UPLOAD_BY_CAN> <!--  Y-YES ,N - NO -->
                  <ENABLE_ONLINE_ACCESS_FLAG>Y</ENABLE_ONLINE_ACCESS_FLAG> <!--  Y-YES ,N - NO -->
                  <ENTITY_EMAIL_DETAILS>
                      <EMAIL_ID>{profile.EMAIL}</EMAIL_ID>
                      <EMAIL_ID></EMAIL_ID>
                  </ENTITY_EMAIL_DETAILS>
                  <HOLDING_TYPE>{mfu.HOLDING_NATURE.CODE}</HOLDING_TYPE>
                  <INV_CATEGORY>{mfu.INVESTOR_CATEGORY.CODE}</INV_CATEGORY>
                  <TAX_STATUS>{mfu.TAX_STATUS.TAX_STATUS}</TAX_STATUS>
                  <HOLDER_COUNT>{mfu.HOLDING_COUNT}</HOLDER_COUNT>
                  <HOLDER_RECORDS>
                      {holder_record}
                  </HOLDER_RECORDS>
                  <ARN_DETAILS>
                  <!--  RIA Code need to add -->
                  <ARN_NO></ARN_NO>
                  <RIA_CODE></RIA_CODE>
                  <!-- RIA Code -->
                  <EUIN_CODE></EUIN_CODE>
                  </ARN_DETAILS>
                  <DP_DETAILS>
                    <NSDL_DP_ID></NSDL_DP_ID>
                    <NSDL_CLIENT_ID></NSDL_CLIENT_ID>
                    <NSDL_PROOF_ID></NSDL_PROOF_ID>
                    <NSDL_VER_FLAG></NSDL_VER_FLAG>
                    <CDSL_DP_ID></CDSL_DP_ID>
                    <CDSL_CLIENT_ID></CDSL_CLIENT_ID>
                    <CDSL_PROOF_ID></CDSL_PROOF_ID>
                    <CDSL_VER_FLAG></CDSL_VER_FLAG>
                  </DP_DETAILS>
                  <BANK_DETAILS>
                  <!--Multiple Record-->
                      {bank_record}
                  </BANK_DETAILS>
                  <NOMINEE_DETAILS>
                      <NOM_DECL_LVL>{'' if mfu.INVESTOR_CATEGORY.CODE == "M" else "C"}</NOM_DECL_LVL>
                      <NOMIN_OPT_FLAG>{'' if mfu.INVESTOR_CATEGORY.CODE == "M" else r_nominee_detail.NOMINEE_OPTION}</NOMIN_OPT_FLAG>
                      <NOM_VERIFY_TYPE>{'' if mfu.INVESTOR_CATEGORY.CODE == "M" else r_nominee_detail.NOMINEE_VERIFICATION_TYPE}</NOM_VERIFY_TYPE>
                      <NOMINEES_RECORDS>
                        {nominee_record}
                      </NOMINEES_RECORDS>
                  </NOMINEE_DETAILS>
                </REQ_BODY>
              </CANIndFillEezzReq>
              """
  return payload

# def registration_anyone_survivor(id):
#   profile = Registration_personal_details.objects.get(id=id)
#   pass

# def registration_joint(id):
#   profile = Registration_personal_details.objects.get(id=id)
#   pass