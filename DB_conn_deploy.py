import mysql.connector
import pandas as pd
import numpy as np
import os
import re
from logger import get_logger

def get_connection():
    return mysql.connector.connect(
        host=os.getenv("DB_HOST"),
        user=os.getenv("DB_USER"),
        password=os.getenv("DB_PASSWORD"),
        database=os.getenv("DB_NAME")
    )
def clean_column_name(name):
    return re.sub(r'[^a-z0-9]', '_', name.lower())


def insert_data_to_db(df, table_name):
    conn = get_connection()
    cursor = conn.cursor()

    # Pulisce i nomi delle colonne
    df.columns = [clean_column_name(col) for col in df.columns]

    # Converte NaN in None per compatibilità con MySQL
    df = df.replace({np.nan: None})

    columns = ', '.join(df.columns)
    placeholders = ', '.join(['%s'] * len(df.columns))
    insert_query = f"INSERT INTO {table_name} ({columns}) VALUES ({placeholders})"

    try:
        for _, row in df.iterrows():
            cursor.execute(insert_query, tuple(row))
        conn.commit()
        print("Dati inseriti con successo.")
    except Exception as e:
        print(f"Errore durante l'inserimento nel DB: {e}")
    finally:
        cursor.close()
        conn.close()

def main():
    logger = get_logger('access_logger')

    try:
        df = pd.read_csv('csv_files/cdr-wimore-2023-12-25.csv', sep=',', on_bad_lines='skip')
        print(df.head())
        insert_data_to_db(df, 'cdr_data')
        logger.info(f"{len(df)} righe inserite con successo.")
    except Exception as e:
        print(f"Errore generale: {e}")
        logger.error(f"Errore generale: {e}")

if __name__ == "__main__":
    main()
