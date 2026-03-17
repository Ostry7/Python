#usage: python file_backup.py .extension --path "C:/dir/path" eg. python file_backup.py .txt --path "C:/Users/Dokumenty" 
import py7zr
import datetime
from pathlib import Path
import argparse


my_parser = argparse.ArgumentParser(description='Backup files based on file extenstion')
my_parser.add_argument("--path",
                     help='Please enter the files path', required=True)
my_parser.add_argument("file_extension",
                       help='Please enter the extenstion of files (eg. .txt)')
args = my_parser.parse_args()

current_date = datetime.datetime.today().strftime('%Y-%m-%d')   #'yyyy-MM-dd' date format
file_path =  Path(args.path)
file_extension = args.file_extension
archive_name = f'backup_{current_date}.7z'

with py7zr.SevenZipFile(f'{archive_name}', 'w') as archive:
    for py_files in file_path.iterdir():
        if py_files.is_file() and py_files.suffix == file_extension:
            print (file_path/py_files.name)
            archive.write(file_path/py_files.name, arcname=py_files.name)