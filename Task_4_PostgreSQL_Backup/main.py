from pg_backup import ssh_connect_and_backup, gzip_backup 


if __name__ == "__main__":
    is_backup_ok = ssh_connect_and_backup()

    if is_backup_ok:
        print ("[SUCCESS] Backup file successfully created! -> Compressing file: ")
        gzip_backup()
        print ("[SUCCESS] Compress backup file!")
    else:
        print("[FAIL] Backup failed! Skipping compression!")
        exit(1)