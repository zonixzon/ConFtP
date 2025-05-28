import mysql.connector
import pandas as pd
from logger import get_logger

def get_connection():
    connection = mysql.connector.connect(
        host="localhost",
        user="root",
        password="",
        database="test"
    )
    return connection

if __name__ == "__main__":
    try:
        # Leggi il CSV
        df = pd.read_csv('MOCK_DATA.csv')

        conn = get_connection()
        cursor = conn.cursor()

        # Inserisci ogni riga del DataFrame nella tabella 'cliente'
        for index, row in df.iterrows():
            sql = """
                INSERT INTO cliente (id, first_name, last_name, email, gender, ip_address)
                VALUES (%s, %s, %s, %s, %s, %s)
            """
            values = (
                row['id'],
                row['first_name'],
                row['last_name'],
                row['email'],
                row['gender'],
                row['ip_address']
            )
            cursor.execute(sql, values)

        conn.commit()

        logger = get_logger()
        total_rows = len(df)
        logger.info(f" {total_rows} rows inserted")
        print("Dati inseriti con successo!")
        
        cursor.close()
        conn.close()
    except Exception as err:
        print(f"Errore: {err}")