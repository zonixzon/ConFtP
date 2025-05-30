import paramiko
import os

# Load configuration from environment variables
SFTP_HOST = os.getenv("SFTP_HOST")
SFTP_PORT = int(os.getenv("SFTP_PORT", 22))
SFTP_USER = os.getenv("SFTP_USER")
SFTP_PASS = os.getenv("SFTP_PASS")
SEARCH_TERM = os.getenv("SEARCH_TERM", "cdr-wimore")
REMOTE_DIR = "AS6_cdr/cdr_hourly_out/"
LOCAL_DIR = "downloaded_files/"

def main():
    os.makedirs(LOCAL_DIR, exist_ok=True)

    transport = paramiko.Transport((SFTP_HOST, SFTP_PORT))
    try:
        print("Connecting to SFTP server...")
        transport.connect(username=SFTP_USER, password=SFTP_PASS)
        sftp = paramiko.SFTPClient.from_transport(transport)

        print(f"Changing to remote directory: {REMOTE_DIR}")
        sftp.chdir(REMOTE_DIR)
        files = sftp.listdir()

        matching_files = [f for f in files if SEARCH_TERM in f]

        if not matching_files:
            print(" Nessun file trovato con il termine di ricerca.")
            return

        for filename in matching_files:
            local_path = os.path.join(LOCAL_DIR, filename)
            print(f"Scaricando: {filename}")
            sftp.get(filename, local_path)
            print(f"Salvato in: {local_path}")

        sftp.close()
    except Exception as e:
        print(f" Errore durante la connessione o il download: {e}")
    finally:
        transport.close()
        print("Connessione SFTP chiusa.")

if __name__ == "__main__":
    main()
