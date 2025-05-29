from ftplib import FTP

# Configura questi parametri
FTP_HOST = ''
FTP_USER = 'as6service'
FTP_PASS = 'wW7T46JtT68Xz59L8p'
SEARCH_TERM = 'parte_nome_file'  # Cambia con la parte del nome che ti interessa

def main():
    ftp = FTP(FTP_HOST)
    ftp.connect(FTP_HOST, timeout=30)  # Timeout di 30 secondi
    ftp.login(FTP_USER, FTP_PASS)
    files = ftp.nlst()#fornisce una lista di file nel server ftp

    file_to_download = None
    for filename in files:
        if SEARCH_TERM in filename:# cerca il file che contiene la stringa desiderata
            file_to_download = filename
            break
            
    try:
        with open(file_to_download, 'wb') as f:
            ftp.retrbinary(f'RETR {file_to_download}', f.write)#retr è il comando per scaricare un file
        print(f"Scaricato: {file_to_download}")
    except Exception as e:
        print(f"Errore durante il download: {e}")
    

    ftp.quit()

if __name__ == "__main__":
    main()