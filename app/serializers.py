from rest_framework import serializers
from app.models import *

class CartSerializer(serializers.ModelSerializer):
  class Meta:
      model = Cart
      exclude = ('IS_DELETED','CREATED_DATE','UPDATED_DATE',)
      depth=1

class Registration_personal_details_Serializer(serializers.ModelSerializer):
  class Meta:
      model = Registration_personal_details
      exclude = ('IS_DELETED','CREATED_DATE','UPDATED_DATE',)
      depth=1

# class Registration_mfu_details_Serializer(serializers.ModelSerializer):
#   class Meta:
#       model = Registration_mfu_details
#       exclude = ('IS_DELETED','CREATED_DATE','UPDATED_DATE',)
#       depth=1

class Bank_details_Serializer(serializers.ModelSerializer):
  class Meta:
      model = Registration_bank_details
      exclude = ('IS_DELETED','CREATED_DATE','UPDATED_DATE',)
      depth=1

# class Registration_bank_details_Serializer(serializers.ModelSerializer):
#   class Meta:
#       model = Registration_bank_details
#       exclude = ('IS_DELETED','CREATED_DATE','UPDATED_DATE',)
#       depth=1

class Registration_communication_details_Serializer(serializers.ModelSerializer):
  class Meta:
      model = Registration_communication_details
      exclude = ('IS_DELETED','CREATED_DATE','UPDATED_DATE',)
      depth=1

class Nominee_details_Serializer(serializers.ModelSerializer):
  class Meta:
      model = Nominee_details
      exclude = ('IS_DELETED','CREATED_DATE','UPDATED_DATE',)
      depth=1

class Registration_nominee_details_Serializer(serializers.ModelSerializer):
  class Meta:
      model = Registration_nominee_details
      exclude = ('IS_DELETED','CREATED_DATE','UPDATED_DATE',)
      depth=1

class Tax_status_master_Serializer(serializers.ModelSerializer):
  class Meta:
      model = Tax_status_master
      exclude = ('IS_DELETED','CREATED_DATE','UPDATED_DATE',)
      depth=1

# class Registration_fatca_details_Serializer(serializers.ModelSerializer):
#   class Meta:
#       model = Registration_fatca_details
#       exclude = ('IS_DELETED','CREATED_DATE','UPDATED_DATE',)
#       depth=1

# "r1" : Registration_personal_details.objects.get(id=id),
#         "r2" : Registration_mfu_details.objects.get(USER__id=id),
#         "r3" : Registration_bank_details.objects.filter(USER__id=id),
#         "r4" : Registration_bank_details.objects.get(USER__id=id),
#         "r5" : Registration_communication_details.objects.get(USER__id=id),
#         "r6" : Registration_kyc_details.objects.get(USER__id=id),
#         "r7" : Nominee_details.objects.filter(USER__id=id),
#         # "r6_1" : Registration_nominee_details.objects.filter(USER__id=id),
#         # "r8" : Tax_details.objects.filter(USER__id=id),
#         "r8" : Registration_fatca_details.objects.get(USER__id=id),

class CanModificationRegSerializers(serializers.ModelSerializer):
    class Meta:
      model = Registration_personal_details
      exclude = ('IS_DELETED','CREATED_DATE','UPDATED_DATE',)
