from django.http import JsonResponse
from .models import *
from datetime import datetime, timedelta
import logging
logger = logging.getLogger(__name__)


def can_verify():
    try:
        logger.info(f"enter")
        
            # a = 
        for index,i in enumerate(Registration_personal_details.objects.all()):
            logger.info(f"index = {index} , i = {i}")
        pass
    except Exception as e:
        logger.exception(e)
        return JsonResponse("Something went wrong",safe=False,status=500)




# try:
# except Exception as e:
#         logger.exception(e)
#         pass