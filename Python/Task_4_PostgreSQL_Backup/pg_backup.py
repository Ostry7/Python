import subprocess, time, os, gzip, shutil

DB_NAME = "devops_portfolio"
DB_USER = "backup_user"
DB_PASS = "backup123"
DB_HOST = "192.168.68.240"
DB_PORT = "5432"

def ssh_connect_and_backup():
    #sshpass apt required!
    os.environ['PGPASSWORD'] = DB_PASS
    cmd = [
        "sshpass", "-f", "pass.txt", "ssh", "-L", f"5433:localhost:{DB_PORT}", "-N", f"looser@{DB_HOST}",
    ]
    tunnel = subprocess.Popen(cmd)
    print("[SSH] Tunnel 5433→5432 started!")
    print(f"[SUCESS] Connection wih {DB_HOST} established!")
    time.sleep(2)
    cmd_backup = [
        "pg_dump", "-h", "localhost", "-p", "5433", "-U",f"{DB_USER}", f"{DB_NAME}", "-f", "backup.sql"
    ]
    result = subprocess.run(cmd_backup, capture_output=True, text=True)
    print(result.stdout or result.stderr)
    if os.path.exists("backup.sql"):
        print(f"[SUCCESS] backup.sql = {os.path.getsize('backup.sql')/1024/1024:.1f}MB ")
    
    is_backup_ok = (
        result.returncode == 0 and      #pg_dump ok
        os.path.exists("backup.sql")    #backup.sql exists
    )

    if is_backup_ok:
        print(f"[SUCCESS]")
    else:
        print(f"[FAIL] Backup failed!")
    tunnel.terminate()
    return is_backup_ok

def gzip_backup():
    try:
        with open('backup.sql', 'rb') as f_in:
            with gzip.open('backup.sql.gz', 'wb') as f_out:
                shutil.copyfileobj(f_in, f_out)
                print(f"[SUCCESS] Compress file = {os.path.realpath('backup.sql')}")
        
        is_gzip_ok = (
            os.path.exists("backup.sql.gz") #backup.sql.gz exists
        )
    except Exception as e:
        print(f"[FAIL] Compression error: {e}")

    if is_gzip_ok:
        print("[SUCCESS]")
    else: 
        print("[FAIL] Compressing failed!")
    return is_gzip_ok