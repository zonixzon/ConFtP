import paramiko
import os

# Load configuration from environment variables
SFTP_HOST = os.getenv("SFTP_HOST")
SFTP_PORT = int(os.getenv("SFTP_PORT", 22))
SFTP_USER = os.getenv("SFTP_USER")
SFTP_PASS = os.getenv("SFTP_PASS")
REMOTE_DIR = "AS6_cdr/cdr_hourly_out/"
LOCAL_DIR = "downloaded_files/"
SPECIFIC_FILE = os.getenv("SPECIFIC_FILE")  # es: 'cdr-wimore-2023-12-25.csv'

def download_file(sftp, remote_filename, local_dir):
    local_path = os.path.join(local_dir, remote_filename)
    print(f"Scaricando: {remote_filename}")
    sftp.get(remote_filename, local_path)
    print(f"Salvato in: {local_path}")

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
        if not files:
            print("La directory remota è vuota.")
            return

        # Scarica un file specifico se specificato
        if SPECIFIC_FILE:
            if SPECIFIC_FILE in files:
                download_file(sftp, SPECIFIC_FILE, LOCAL_DIR)
            else:
                print(f"Il file specificato '{SPECIFIC_FILE}' non esiste nella directory remota.")
                return
        else:
            # Scarica tutti i file della directory remota
            for file in files:
                download_file(sftp, file, LOCAL_DIR)

        sftp.close()

    except Exception as e:
        print(f"Errore durante la connessione o il download: {e}")
    finally:
        transport.close()
        print("Connessione SFTP chiusa.")

if __name__ == "__main__":
    main()
