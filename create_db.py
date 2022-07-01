from database import DatabaseSqlite3
import pandas as pd
import wget
import requests
import os

SECRET_KEY = os.getenv("KATFILE_KEY")
BASE_URL = "https://katfile.com/api"


def fetchSqlite(tableName='student'):
    file_list_url = f"{BASE_URL}/file/list?key={SECRET_KEY}"
    allFiles = requests.get(file_list_url).json()['result']['files']

    for f in allFiles:
        if 'sqlite3' in f['link']:
            downloadUrl = f"{BASE_URL}/file/direct_link?key={SECRET_KEY}&file_code={f['file_code']}"
            db_link = requests.get(downloadUrl).json()['result']['url']
            db_name = db_link.split("/")[-1]
            wget.download(db_link,db_name )
            # local_db = requests.get(db_link)
            db = DatabaseSqlite3(db_name)

    return db.read_table_with_df(tableName)

if __name__=='__main__':
    pass