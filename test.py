from CSVReader import CSVReader
from DB_connection import get_connection

get_connection()

conn = get_connection()
cursor = conn.cursor()


reader = CSVReader('csv_files/cdr-wimore-2023-12-25.csv')

columns=reader.header()
table_name="calls"
placeholder = ", ".join(["%s"]) * len(columns)

insert_query = f"INSERT INTO {table_name} ({columns}) VALUES ({placeholder})"

first_row = next(reader.databaseRows())
values = list(first_row.values())
cursor.execute(insert_query,values)


