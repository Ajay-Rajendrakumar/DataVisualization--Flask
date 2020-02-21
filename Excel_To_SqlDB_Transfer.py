import sqlite3
from sqlite3 import Error
import pandas as pd

DB_FILE_PATH = 'HW_Parts.db'
XL_FILE_PATH = 'Assignment-SampleData.xlsx'

def connect_to_db(db_file):
    sqlite3_conn = None
    try:
        sqlite3_conn = sqlite3.connect(db_file)
        return sqlite3_conn
    except Error as err:
        print(err)
        if sqlite3_conn is not None:
            sqlite3_conn.close()

def insert_values_to_table(table_name, xl_file):
    conn = connect_to_db(DB_FILE_PATH)
    if conn is not None:
        c = conn.cursor()
        # Create table if it is not exist
        c.execute('CREATE TABLE IF NOT EXISTS ' + table_name +
                  '(Partsid    VARCHAR,'
                  'Status     VARCHAR,'
                  'Category   VARCHAR,'
                  'PartName   VARCHAR,'
                  'CreatedBy  VARCHAR,'
                  'ApprovedBy VARCHAR)')
        df = pd.read_excel(xl_file)
        df.columns = get_column_names_from_db_table(c, table_name)
        df.to_sql(name=table_name, con=conn, if_exists='replace', index=False)
        conn.close()
        print('SQL insert process finished')
    else:
        print('Connection to database failed')

def get_column_names_from_db_table(sql_cursor, table_name):
    table_column_names = 'PRAGMA table_info(' + table_name + ');'
    sql_cursor.execute(table_column_names)
    table_column_names = sql_cursor.fetchall()
    column_names = list()
    for name in table_column_names:
        column_names.append(name[1])
    return column_names

def Read():
    # Read sqlite query results into a pandas DataFrame
 
    con = connect_to_db(DB_FILE_PATH)
    cur = con.cursor()
    for row in cur.execute('SELECT * FROM Parts_Info;'):
        print(row)
    con.close()


if __name__ == '__main__':
    insert_values_to_table('Parts_Info', XL_FILE_PATH)
    x = input("Need To Read DB File?[enter 1 to read]:")
    if(x=="1"):
        Read()

