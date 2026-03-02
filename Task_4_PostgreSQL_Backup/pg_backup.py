import subprocess, time, os

DB_NAME = "devops_portfolio"
DB_USER = "backup_user"
DB_PASS = "backup123"
DB_HOST = "192.168.68.240"
DB_PORT = "5432"

def ssh_connect_and_backup():
    #sshpass apt required!
    os.environ['PGPASSWORD'] = DB_PASS
    cmd = [
        "sshpass", "-f", "pass.txt", "ssh", "-L", "5433:localhost:5432", "-N", f"looser@{DB_HOST}",
    ]
    tunnel = subprocess.Popen(cmd)
    print("[SSH] Tunnel 5433→5432 started!")
    print(f"Connection wih {DB_HOST} established!")
    time.sleep(2)
    cmd_backup = [
        "pg_dump", "-h", "localhost", "-p", "5433", "-U",f"{DB_USER}", f"{DB_NAME}", "-f", "backup.sql"
    ]
    result = subprocess.run(cmd_backup, capture_output=True, text=True)
    print(result.stdout or result.stderr)
    if os.path.exists("backup.sql"):
        print(f"[SUCCESS] backup.sql = {os.path.getsize('backup.sql')/1024/1024:.1f}MB ")
    
    tunnel.terminate()
    return result.returncode


tunnel = ssh_connect_and_backup()