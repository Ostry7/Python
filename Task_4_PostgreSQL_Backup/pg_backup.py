import psycopg2, subprocess, time

DB_NAME = "devops_portfolio"
DB_USER = "postgres"
DB_PASS = "devops123"
DB_HOST = "192.168.68.240"
DB_PORT = "5432"

def db_connect():
    conn = 0
    try:
        conn = psycopg2.connect(database=DB_NAME,
                                user=DB_USER,
                                password=DB_PASS,
                                host=DB_HOST,
                                port=DB_PORT)
        print("[SUCCESS]  Database connected successfully")
    except:
        print("[FAIL]  Database not connected successfully")


def ssh_connect():
    #sshpass apt required!
    cmd = [
        "sshpass", "-f", "pass.txt", "ssh", f"looser@{DB_HOST}",
    ]
    tunnel = subprocess.Popen(cmd)
    
    print(f"Connection wih {DB_HOST} established!")
    time.sleep(2)
    return tunnel

def pg_dump_create():
    cmd = [
        "pwd"

    ]
    
    subprocess.Popen(cmd)

tunnel = ssh_connect()
pg_dump_create()
tunnel.terminate()