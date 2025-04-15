from django.test import TestCase
import os
from pathlib import Path
import environ
import pandas as pd
# Create your tests here.
BASE_DIR = Path(__file__).resolve().parent.parent


class bulk_customer_upload(TestCase):
    def upload(self):
        #file_path = 'C:\Users\ADMIN\Documents\git\investology_django\client  data.xlsx'
        df1 = pd.read_excel("C:\\Users\\ADMIN\\Documents\\git\\investology_django\\client  data.xlsx")
        for index, row in df1.iterrows():
            
            print(row['Client Name'], row['Address'], int(row['Mobile']) if not pd.isna(row['Mobile']) else '', row['Email'], row['Pan No'])
            print()

bulk_customer_upload.upload