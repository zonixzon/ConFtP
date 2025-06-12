import csv
import re
from datetime import datetime

class CSVReader:
    def __init__(self, path, encoding='utf-8', delimiter=','):
        self.path = path
        self.encoding = encoding
        self.delimiter = delimiter


    def databaseRows(self):
        with open(self.path, newline='', encoding=self.encoding) as file:
            reader = csv.DictReader(file, delimiter=self.delimiter)
            for raw_row in reader:
                row = {}
                for key, value in raw_row.items():
                    clean_key = self.normalize_key(key)
                    if isinstance(value, str):
                        row[clean_key] = self.process_string(value.strip('"'))
                    else:
                        row[clean_key] = value
                        
                ext_call_start = row.get("call_start")

                if ext_call_start:
                    dt = datetime.strptime(ext_call_start, "%Y-%m-%d-%H-%M-%S")
                    dt = dt.replace(minute=0, second=0, microsecond=0)
                    row["reference_file"] = dt.strftime("%Y-%m-%d %H:%M:%S")
                else :
                    print("Call start is not available")

                yield row

    @staticmethod
    def normalize_key(key):
        # Sostituisce tutto tranne lettere e numeri con _
        key = re.sub(r'[^a-zA-Z0-9]', '_', key)
        # Rimuove eventuali _ consecutivi
        key = re.sub(r'_+', '_', key)
        return key.strip('_').lower()  # Rimuove _ iniziali/finali se presenti

    @staticmethod
    def is_float_string(value):
        try:
            float(value)
            return True
        except ValueError:
            return False

    @staticmethod
    def process_string(s):
        replaced = s.replace(",", ".")
        if CSVReader.is_float_string(replaced):
            return replaced
        else:
            return s
        
        
    def header(self):
        with open(self.path, newline='', encoding=self.encoding) as file:
            reader = csv.reader(file, delimiter=self.delimiter)
            return next(reader)  
        
    
