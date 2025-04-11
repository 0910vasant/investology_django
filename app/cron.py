import json
from django.http import JsonResponse
import requests
from .models import *
from datetime import datetime, timedelta
import logging
logger = logging.getLogger(__name__)


def can_verify():
    try:
        logger.info(f"enter can")
            # a = 
        session = investology_login_session.objects.last()

        for index,i in enumerate(Registration_personal_details.objects.all()):
            # dob = Registration_mfu_details.objects.get(USER=i.id)
            url = "https://14.141.212.169:4091/APICANValidationService.do"
            data = {
                "sendResponseFormat": "JSON" ,
                "sessioncontext"    : session.SESSIONCONTEXT ,
                "sendersubid"       : session.SENDERSUBID ,
                # "sendersubid"       : "123" ,
                "logTp"             : "A",
                "can"               : i.CAN,
                "entityId"          : "40007K",
                "pan"               : i.PAN_NO,
                # "dob"               : dob.PRIMARY_HOLDER_DOB,
                "emailId"           : i.EMAIL,
            }
            response = requests.post(url, data=data,verify=False)
            # response = response.text
            response = json.loads(response.text)
            if response["respStatus"] == "0":
                logger.info(f"success = {response}")
                # success = text["canStatus"]
                logger.info(f'success = {response["responseList"]["canStatus"]}')

            else:
                 logger.info(f"error = {response}")
                # data_response = {
                #     "errorMessage" : response["errorMessage"]
                # }
            
        pass
    except Exception as e:
        logger.exception(e)
        return JsonResponse("Something went wrong",safe=False,status=500)




# try:
# except Exception as e:
#         logger.exception(e)
#         pass