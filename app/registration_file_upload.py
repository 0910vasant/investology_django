import requests
from app.models import Registration_bank_details,Registration_mfu_details, Registration_holder_details, Registration_personal_details, Scan_pan,Header_Checklist

import logging
logger = logging.getLogger(__name__)


def file_upload(id,app_type):
    try:
        logger.info(f"entered in file upload function and id = {id}")
        profile             = Registration_personal_details.objects.get(id=id)
        mfu                 = Registration_mfu_details.objects.get(USER=id)
        holder_details      = Registration_holder_details.objects.filter(USER=id,IS_DELETED=False).order_by("-id")
        default_bank        = Registration_bank_details.objects.get(USER=id,IS_DELETED=False,DEFAULT_BANK=True)
        header_checklist    = Header_Checklist.objects.get(APP_TYPE=app_type,CHECKLIST_USE_FOR="can",IS_DELETED=False)
        
        url = f"{header_checklist.BASE_URL}/MFUImageServerUpload"

        response_array = []

        for i in holder_details:
            file            = i.HOLDER_PAN_IMG
            file_name       = file.name
            logger.info(f"holder_details file_name  = {file_name}")
            if file_name:
                logger.info(f"enter if file {i.HOLDER_TYPE}")
                param8 = "1#PC"
                
                img_name        = file_name.replace("Holder Pan Image/","")
                # logger.info(f"file path = {file.path} name = {img_name}")


                payload = {
                    'param1': header_checklist.LOGIN_ID,
                    'param2': header_checklist.EN_ENCR_PASSWORD,
                    'param3': header_checklist.ENTITY_ID,
                    'param4': 'ECAN',
                    'param5': 'AD',
                    'param6': profile.CAN,
                    'param7': '',
                    'param8': param8
                }

                files=[
                    ('file',(f"{img_name}",open(f'./media/{file}','rb'),'image/jpg'))
                ]
            
                headers = {}
                logger.info(f"""
                    payload{i.id}   = {payload}
                    file_path       = {file.path}
                    img_name        = {img_name}
                    file{i.id}      = {files}
                """)

                response = requests.request("POST", url, headers=headers, data=payload, files=files, verify=False, timeout=5)
                logger.info(f"response{i.id} = {response.text}")
                response_array.append(response)

        # for index,i in enumerate(response_array):
        #     logger.info(f"response{index} = {i.text}")


        for i in range(1,3):
            # if (mfu.INVESTOR_CATEGORY.CODE == "M" and HOLDER_TYPE == "PR"):
            #     holder.MINOR_BIRTH_CERTIFICATE  = minor_birth_certificate
            logger.info(f"i = {i}")
            upload_document = False
            if i == 1:
                if Registration_mfu_details.objects.filter(USER=id,INVESTOR_CATEGORY__CODE = "M").exists():
                    upload_document = True
                    param8          = "3#BC"
                    file            = Registration_holder_details.objects.get(USER=id,HOLDER_TYPE="PR",IS_DELETED=False).MINOR_BIRTH_CERTIFICATE
                    # img_name        = file.name
                    img_name        = file.name.replace("Minor Birth Certificate/","")
            if i == 2:
                upload_document = True
                param8 = "2#BP"
                file = default_bank.BANK_PROOF_FILE
                # img_name = file.name
                img_name = file.name.replace("bank_proof/","")

            if upload_document is True:
                payload={
                    'param1': header_checklist.LOGIN_ID,
                    'param2': header_checklist.EN_ENCR_PASSWORD,
                    'param3': header_checklist.ENTITY_ID,
                    'param4': 'ECAN',
                    'param5': 'AD',
                    'param6': profile.CAN,
                    'param7': '',
                    'param8': param8
                }

                files=[
                    ('file',(f"{img_name}",open(f'./media/{file}','rb'),'image/jpg'))
                ]

                logger.info(f"""
                    payload{i}   = {payload}
                    img_name     = {img_name}
                    file_path    = {file.path}
                    file{i}      = {files}
                """)

                headers = {}

                response = requests.request("POST", url, headers=headers, data=payload, files=files, verify=False, timeout=5)
                logger.info(f"response{i} = {response.text}")
                response_array.append(response)


        # for index,i in enumerate(response_array):
        #     logger.info(f"response{index} = {i.text}")
        return True
        # return True
    except Exception as e:
        logger.error(f"registration file upload error \n{e}")
        return False