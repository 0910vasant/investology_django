from django.urls import path
# from .views import send_login_dtl,app_login,add_buy_api,add_redeem_api
from .views import *
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('send_login_dtl', send_login_dtl),
   

    path('add_buy_api', add_buy_api),
    path('add_redeem_api', add_redeem_api),
]

# urlpatterns = []