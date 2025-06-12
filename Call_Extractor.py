from flask import Flask, request, jsonify,abort
from DB_connection import get_connection

app = Flask(__name__)

@app.route('/calls', methods=['POST'])
def get_calls():

    data =request.get_json()

    acc_number = data['acc_number']
    start = data['call_start']
    end = data['call_end']

    if not acc_number:
        return jsonify({"error": "acc_number is required"}), 400
    
    

    conn = get_connection()
    cursor = conn.cursor()

    query = "SELECT * FROM calls WHERE acc_number = %s"
    params = [acc_number]

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

    print (list(cursor.description))

    # Optional: convert to list of dicts if needed
    columns = [desc[0] for desc in cursor.description]
    result = [dict(zip(columns, row)) for row in rows]

    cursor.close()
    conn.close()

    return jsonify(result)

if __name__ == '__main__':
    app.run(port=5001)
