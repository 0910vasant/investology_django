from django.test import TestCase
import os
from pathlib import Path
import environ
import pandas as pd
from crm.models import * 
# Create your tests here.
BASE_DIR = Path(__file__).resolve().parent.parent


class bulk_customer_upload(TestCase):
    def upload(self):
        #file_path = 'C:\Users\ADMIN\Documents\git\investology_django\client  data.xlsx'
        
        df1 = pd.read_excel("C:\\Users\\ADMIN\\Documents\\git\\investology_django\\client  data.xlsx")
        for index, row in df1.iterrows():
            print(row['Client Name'], row['Address'], int(row['Mobile']) if not pd.isna(row['Mobile']) else '', row['Email'], row['Pan No'])   

class bulk_upload_mf_master(TestCase):
    def upload(self):
        df1 = pd.read_excel("C:\\Users\\ADMIN\\Desktop\\changes.xlsx")
        for index, row in df1.iterrows():
            print(row['Fund Name'], row['Brokerage %'], row['B*18%'], row['B-C'],row['Red Diamond'], row['Blue diamond'], row['Pink Diamond'], row['Emerald'], row['Sapphire'], row['Red Ruby'])
            add = MF_master.objects.create(SCHEME=row['Fund Name'], E_C_P=row['Brokerage %'], NET_A_GST=row['B*18%'], EP_PAYOUT=row['B-C'], RED_DIAMOND=row['Red Diamond'], BLUE_DIAMOND=row['Blue diamond'], PINK_DIAMOND=row['Pink Diamond'], EMERALD=row['Emerald'], SAPPHIRE=row['Sapphire'], RED_RUBY=row['Red Ruby'])
            add.save()

bulk_customer_upload.upload