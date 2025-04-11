from rest_framework import serializers
from crm.models import *

class Branch_ManagerSerializer(serializers.ModelSerializer):
  class Meta:
      model = Branch_Manager
      exclude = ('IS_DELETED','CREATED_DATE','UPDATED_DATE',)
      depth=1


class Relationship_ManagerSerializer(serializers.ModelSerializer):
  class Meta:
      model = Relationship_Manager
      exclude = ('IS_DELETED','CREATED_DATE','UPDATED_DATE',)
      depth=1

class Easy_PartnerSerializer(serializers.ModelSerializer):
  class Meta:
      model = Easy_Partner
      exclude = ('IS_DELETED','CREATED_DATE','UPDATED_DATE',)
      depth=1

class BM_BrokerageSerializer(serializers.ModelSerializer):
  class Meta:
      model = BM_Brokerage
      exclude = ('IS_DELETED','CREATED_DATE','UPDATED_DATE',)
      depth=1

class RM_BrokerageSerializer(serializers.ModelSerializer):
  class Meta:
      model = RM_Brokerage
      exclude = ('IS_DELETED','CREATED_DATE','UPDATED_DATE',)
      depth=1

class Sub_Broker_BrokerageSerializer(serializers.ModelSerializer):
  class Meta:
      model = Easy_Partner_Brokerage
      exclude = ('IS_DELETED','CREATED_DATE','UPDATED_DATE',)
      depth=1


