from pg_backup import ssh_connect_and_backup, gzip_backup
from aws_s3_push import upload_file


if __name__ == "__main__":
    is_backup_ok = ssh_connect_and_backup()

    if is_backup_ok:
        print ("[SUCCESS] Backup file successfully created! -> Compressing file: ")
        is_gzip_ok = gzip_backup()
        print ("[SUCCESS] Compress backup file!")
        if is_gzip_ok:
            upload_file('backup.sql.gz', 'aws-python-bucket12341234')
            print ("[SUCCESS] Successfully upload backup to the S3!")
        else:
            print ("[FAIL] Failed to upload backup to S3!")
    else:
        print("[FAIL] Backup failed! Skipping compression!")
        exit(1)