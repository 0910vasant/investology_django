from rest_framework import serializers
from admin_panel.models import *

class Cams_kfintech_transactionSerializer(serializers.ModelSerializer):
  class Meta:
      model = Cams_kfintech_transaction
      exclude = ('IS_DELETED','CREATED_DATE','UPDATED_DATE',)
      depth=2