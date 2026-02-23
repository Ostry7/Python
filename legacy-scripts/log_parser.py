import re #regex module
from collections import Counter
import csv


ipregex = r"\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}"

def open_file(file):
    try:
        with open (file, 'r') as logfile:
            fileread = logfile.read()
            ip_list = re.findall(ipregex, fileread)
            return ip_list
    except FileNotFoundError:
         print(f'File {file} doesnt exist!')

def count_address():
        ip_count = Counter(open_file(file))
        return ip_count.items()

def write_csv():
     counter = count_address()
     with open('ip_count.csv', 'w') as file:
          writer = csv.writer(file)
          writer.writerow(['IP_Address', 'Count'])
          for item, value in counter:
            writer.writerow([item,value])


if __name__ == "__main__":
    file = 'apache_logs.log'
    write_csv()