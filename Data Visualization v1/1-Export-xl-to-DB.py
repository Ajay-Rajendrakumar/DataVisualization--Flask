import sqlite3
from sqlite3 import Error
import pandas as pd
import random
count=0

DB_FILE_PATH = 'ExcelSheet.db'
XL_FILE_PATH = 'Assignment-SampleData.xlsx'
DB_FILE_PATH1 = 'HW_Parts.db'

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
        c.execute('CREATE TABLE IF NOT EXISTS ' + table_name +
                  '(Partsid    VARCHAR,'
                  'Status     VARCHAR,'
                  'Category   VARCHAR,'
                  'PartName   VARCHAR,'
                  'CreatedBy  VARCHAR,'
                  'ApprovedBy VARCHAR)')
        df = pd.read_excel(xl_file)
        df.columns = get_column_names_from_db_table(c, table_name)
        df.to_sql(name=table_name, con=conn, if_exists='append', index=False)
        conn.close()


        print('SQL insert process finished')
    else:
        print('Connection to database failed')

def NormalizeNew(Old_tb_name ,New_tb_name,category):
    con = connect_to_db(DB_FILE_PATH)
    c = con.cursor()
    con1 = connect_to_db(DB_FILE_PATH1)
    c1 = con1.cursor()
    c1.execute('CREATE TABLE IF NOT EXISTS ' + New_tb_name +
                  '(Empid    INTEGER  Primarykey,'
                  'EmpName     VARCHAR,'
                  'Designation   VARCHAR)'
                  )
    
    sql='SELECT DISTINCT  '+ category +' from '+ Old_tb_name
    names=[]
    for row in c.execute(sql):
        names.append(row[0])

    insertEmp(names,New_tb_name)
      

def insertPart(otb,ntb):
    con = connect_to_db(DB_FILE_PATH)
    c = con.cursor()
    con1 = connect_to_db(DB_FILE_PATH1)
    c1 = con1.cursor()
    c1.execute('CREATE TABLE IF NOT EXISTS ' + ntb +
                  '(Partsid    VARCHAR,'
                  'Status     VARCHAR,'
                  'Category   VARCHAR,'
                  'PartName   VARCHAR,'
                  'CreatedEmpId  INTEGER,'
                  'ApprovedEmpId INTEGER)') 
    Values=[]
    for row in c.execute("SELECT * FROM "+ otb + ";"):
            temp=[]
            temp.append(row[0])
            temp.append(row[1])
            temp.append(row[2])
            temp.append(row[3])
            temp.append((retEmpid(row[4])))
            temp.append(retEmpid(row[5]))
            Values.append((tuple(temp[:])))
            del temp

    for i in Values:
      c1.execute('INSERT INTO '+ ntb +' VALUES (?,?,?,?,?,?)', i)
    con1.commit()


def insertEmp(names,tb):
  global count
  Values=[]
  con1 = connect_to_db(DB_FILE_PATH1)
  c1 = con1.cursor()
  for i in range(len(names)):
            temp=[]
            count+=1
            temp.append(count)
            temp.append(names[i])
            if( (random.randint(0,9) % 2) ==0):
              temp.append("Mechanical")
            else:
              temp.append("Electrical")
            Values.append((tuple(temp[:])))
            del temp
  for i in Values:
    c1.execute('INSERT INTO '+ tb +' VALUES (?,?,?)', i)
  con1.commit()
    

def printfuc(t1):
    con = sqlite3.connect(DB_FILE_PATH1)
    cur = con.cursor()      
    for row in cur.execute("SELECT * FROM " + t1 + ";"):
        print(row)

def retEmpid(name):
    con = sqlite3.connect(DB_FILE_PATH1)
    cur = con.cursor()      
    for row in cur.execute("SELECT * FROM Employee where EmpName ='"+ name +"';"):
        return(row[0])



def get_column_names_from_db_table(sql_cursor, table_name):
    table_column_names = 'PRAGMA table_info(' + table_name + ');'
    sql_cursor.execute(table_column_names)
    table_column_names = sql_cursor.fetchall()
    column_names = list()
    for name in table_column_names:
        column_names.append(name[1])
    return column_names


if __name__ == '__main__':
    

    insert_values_to_table('imdb_temp', XL_FILE_PATH)
    NormalizeNew("imdb_temp","Employee","ApprovedBy")
    NormalizeNew("imdb_temp","Employee","CreatedBy")
    insertPart("imdb_temp","PartsInfo")
    #printfuc("Employee")
    #printfuc("PartsInfo")
    
  
    