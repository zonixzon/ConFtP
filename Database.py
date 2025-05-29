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

def main():
    logger = get_logger('access_logger')

    try:
        # Leggi il CSV
        df = pd.read_csv('cdr-wimore-in-2023-12-25.csv')  # <-- nome del tuo file

        conn = get_connection()
        cursor = conn.cursor()

        # SQL 
        sql = """
            INSERT INTO calls (
                call_start_ms, call_start, call_end_ms, call_end, duration,
                acc_account_id, acc_address_id, acc_tenant_id, acc_number, acc_tenant,
                acc_name, acc_address, acc_address_public, acc_address_combined,
                orig_number, dest_name, dest_number, dest_type, dest_tenant,
                dest_tenant_id, pricelist_id, pricelist_version, pricelist_table,
                tariff, postrating, charge_account, charge_tenant, charge_system,
                call_leg, orig_ip, dest_ip, cdr_id, call_id, alert_ms, alert_seconds,
                orig_gateway, dest_gateway, pres_preferred, pres_asserted, cause,
                flags, scope, acc_number_private, call_type, billing_info, sip_call_id,
                q850_cause, dest_acc_id, dest_acc_name, dest_addr_id, dest_addr_number,
                outbound_dest
            ) VALUES (
                %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s,
                %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s,
                %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s
            )
        """

        # Inserimento riga per riga
        for _, row in df.iterrows():
            values = tuple(row[col] for col in df.columns)
            cursor.execute(sql, values)

        conn.commit()
        logger.info(f"{len(df)} righe inserite con successo.")
        print("Dati inseriti correttamente nella tabella `calls`.")

        cursor.close()
        conn.close()

    except Exception as e:
        logger.error(f"Errore durante l'inserimento: {e}")
        print(f"Errore: {e}")

# === AVVIO SCRIPT ===
if __name__ == "__main__":
    main()