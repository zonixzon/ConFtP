from flask import Flask, request, jsonify,abort
from DB_connection import get_connection
from datetime import datetime ,time
import math

app = Flask(__name__)

@app.route('/calls', methods=['POST'])
def get_calls():

    data =request.get_json()
    status = "OK"
    message = "" 

    try:
        
        acc_account_id = data['acc_account_id']
        start = data['call_start']
        end = data['call_end']
        stato = data["rows"]

        kv_param = {}
        for key , value in data.items():
         kv_param [key] = value
        

        if not acc_account_id:
            return jsonify({"error": "account id is required"}), 400

        conn = get_connection()
        cursor = conn.cursor()

        query = "SELECT * FROM calls WHERE acc_account_id = %s"
        params = [acc_account_id]

        if start:
            query += " AND call_start >= %s"
            params.append(start)

        if end:
            query += " AND call_start <= %s"
            params.append(end)

        print("QUERY:", query)
        print("PARAMS:", params)

        
        cursor.execute(query, tuple(params))
        rows = cursor.fetchall()

        #print (list(cursor.description))

        # Optional: convert to list of dicts if needed
        columns = [desc[0] for desc in cursor.description]
        result = [dict(zip(columns, row)) for row in rows]


        total_charge_account = 0.0
        total_tenant_account = 0.0
        total_system_account = 0.0

        for row in result:
            if "charge_account" in row and row["charge_account"] is not None:
                total_charge_account += row["charge_account"]

        for row in result:
            if "charge_tenant" in row and row["charge_tenant"] is not None:
                total_tenant_account += row["charge_tenant"]

        for row in result:
            if "charge_system" in row and row["charge_system"] is not None:
                total_system_account += row["charge_system"]


        total_time = 0

        for row in result:
            if "duration" in row and row["duration"] is not None:
             total_time += row["duration"]
            
        print("durata totale =",total_time)
        total_second = total_time / 1000
        hour = total_second // 3600
        extra_sec = total_second % 3600
        minuti = extra_sec // 60 
        second = extra_sec % 60
        durata = time(round(hour),round(minuti),round(second))
        durata_str = durata.strftime("%H:%M:%S")

        cursor.close()
        conn.close()

        
        if stato != True:
            result = []
        
        if status == "OK":
            return
        

    except Exception as e :
        print("Errore",e)
        status = "KO"
        message = str(e)
    
    finally:
        final_result ={
                    "status": status, # OK = success, KO = error
                    "message": message, # se si verifica errore, riempi questo campo
                    "data": {
                        "params": kv_param,
                        "stats": {
                        "price": {
                            "account":round( total_charge_account ,2), # Charge Account
                            "tenant": round(total_tenant_account ,2),  # Charge Tenant
                            "system": round(total_system_account ,2)   # Charge System
                        },
                        "time": durata_str # campo Duration che è in MILLISECONDI
                        }
                    },
                     "rows": result
                }

        return final_result

if __name__ == '__main__':
    app.run(port=5001)
