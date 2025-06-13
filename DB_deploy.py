from CSVReader import CSVReader
from DB_connection import get_connection
import os
from logging_handler import get_logger

table_name = os.getenv("DB_NAME")
print(table_name)
LOCAL_DIR='downloaded_files/cdr2025H'
PREFIX='cdrH-wimore'


def insert_file_to_db(filepath,size):
        try:
            # Ottieni la connessione e cursore
            conn = get_connection()
            cursor = conn.cursor()

            logger=get_logger('access_logger')

            reader = CSVReader(filepath)
            rows = list(reader.databaseRows())  
            

            header = list(rows[0].keys())
            

            # Escapa correttamente i nomi colonna per MySQL (con `backtick`)
            column_string = ", ".join(f"`{col}`" for col in header)

            # Prepara i placeholder per il VALUES
            placeholder = ", ".join(["%s"] * len(header))


            # Crea la query INSERT
            insert_query = f"INSERT INTO {table_name} ({column_string}) VALUES ({placeholder})"

            # Prepara i valori da inserire
            all_values = [list(row.values()) for row in rows]


            try:
                logger.info(
                    f"File '{filepath}' - {len(rows)} righe inserite con successo | Dimensione: {size} byte "
            )
            except Exception as e :
                    logger.error(f"Errore durante il logging delle informazioni del file: {e}")
                    
            # Esegui l'inserimento
            cursor.executemany(insert_query, all_values)
            conn.commit()

        except Exception as e :
               logger.error(f"Errore durante l'inserimento del file '{filepath}': {e}")
        finally:
             conn.close()

def main():
    for filename in os.listdir(LOCAL_DIR):#listdir restituisce il nome di tutti i file nella cartella
        if filename.startswith(PREFIX) and filename.endswith(".csv"):
            filepath = os.path.join(LOCAL_DIR, filename)
            size_info =os.path.getsize(filepath)
            insert_file_to_db(filepath,size_info)

if __name__ == "__main__":
    main()


