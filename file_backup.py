import py7zr
import datetime
from pathlib import Path

current_date = datetime.datetime.today().strftime('%Y-%m-%d')   #'yyyy-MM-dd' date format
file_path = Path('C:/Users/ostro/OneDrive/Dokumenty/!GIT/DevOps_Pythonn')
file_mask = '.txt'

with py7zr.SevenZipFile(f'backup_{current_date}.7z', 'w') as archive:
    for py_files in file_path.iterdir():
        if py_files.is_file() and py_files.suffix == file_mask:
            archive.write(f'{file_path}/{py_files.name}', arcname=py_files.name)