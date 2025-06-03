from DB_connection import get_connection

conn = get_connection()
cursor = conn.cursor()


start = "2023-12-25 06:00:00"  
end = "2023-12-25 13:59:59"    
acc_number = "390532834029"  

# Query base
query = """
    SELECT * FROM calls
    WHERE acc_number = %s
"""
params = [acc_number] #aggiunta dei parametri

if start:
    query += " AND call_start >= %s"
    params.append(start)

if end:
    query += " AND call_start <= %s"
    params.append(end)

print("QUERY:", query)
print("PARAMS:", params)


cursor.execute(query, tuple(params))

for row in cursor.fetchall():#fetchall() restituisce tutte le righe della query come una lista di tuple
    print(row)

conn.close()
