import csv
import json
import os

local_file = "cdr-wimore-in-2023-12-25.csv"
  
  
  # Leggi il CSV e converti in lista di dizionari
records = []
try:
    with open(local_file, newline='', encoding='utf-8') as csvfile:
        reader = csv.DictReader(csvfile)#legge ogni riga e lo converte in dizionario
        for row in reader:
            records.append(dict(row))
    print(f"Letti {len(records)} record dal CSV.")
except Exception as e:
    print(f"Errore durante la lettura del CSV: {e}")

# Salva la lista di dizionari in un file JSON
json_file = os.path.splitext(local_file)[0] + ".json"#trasformo il file csv in json
try:
    with open(json_file, 'w', encoding='utf-8') as jf:
        json.dump(records, jf, ensure_ascii=False, indent=4)#ensure_ascii=False per evitare la conversione dei caratteri speciali in entità HTML
    print(f"Salvato JSON in: {json_file}")
except Exception as e:
    print(f"Errore durante il salvataggio del JSONquest: {e}")
