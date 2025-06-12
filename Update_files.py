from DB_connection import get_connection
from DB_deploy import insert_file_to_db
from datetime import datetime
from pathlib import Path
import os
from datetime import timedelta

#conn = get_connection()
#cursor = conn.cursor()

#query = "SELECT MAX(reference_file) FROM calls"
#cursor.execute(query)
#last_reference = cursor.fetchone()[0]  


LOCAL_DIR = Path('downloaded_files/Prova')
PREFIX = 'cdrH-wimore'

#if last_reference is None:(Prova)
last_reference = datetime.strptime("2025-06-12 12:00:00", "%Y-%m-%d %H:%M:%S")

new_reference = datetime.now()
hour_fifo = new_reference.strftime("%Y-%m-%d-%H")
filename = f"{PREFIX}-{hour_fifo}.csv"

filepath = LOCAL_DIR / "cdrH-wimore-2024-01-01-00.csv"  

print(f"Controllo il file: {filepath}")


file_list ={}
increment_time= last_reference 

while increment_time < new_reference:
    hour = increment_time.strftime("%Y-%m-%d-%H")
    date_key = increment_time.replace(minute=0, second=0, microsecond=0)
    key = date_key.strftime("%Y-%m-%d %H:%M:%S")
    filename = f"{PREFIX}-{hour}.csv"
    file_list[key] = filename

    increment_time += timedelta(hours=1)


print(file_list)


for key ,value in file_list.items():
    file_path = LOCAL_DIR / value   
    if os.path.exists(file_path):
        size_info =os.path.getsize(file_path)
        insert_file_to_db(file_path,size_info)
                 

#conn.commit()
#cursor.close()
#conn.close()