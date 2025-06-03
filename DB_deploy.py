from CSVReader import CSVReader
from DB_connection import get_connection
import os

# Ottieni la connessione e cursore
conn = get_connection()
cursor = conn.cursor()

reader = CSVReader('csv_files/cdr-wimore-2023-12-25.csv')
rows = list(reader.databaseRows())  


header = list(rows[0].keys())

# Escapa correttamente i nomi colonna per MySQL (con `backtick`)
column_string = ", ".join(f"`{col}`" for col in header)

# Prepara i placeholder per il VALUES
placeholder = ", ".join(["%s"] * len(header))

# Crea la query INSERT
insert_query = f"INSERT INTO {os.getenv("DB_NAME")} ({column_string}) VALUES ({placeholder})"

# Prepara i valori da inserire
all_values = [list(row.values()) for row in rows]

# Esegui l'inserimento
cursor.executemany(insert_query, all_values)
conn.commit()
conn.close()
