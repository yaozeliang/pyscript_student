
import glob
import shutil
from copy import deepcopy
from datetime import datetime,timedelta,date
import pandas as pd
import numpy as np
import sqlite3


class DatabaseSqlite3:
    
    """ 
    Custom class to connect a Sqlite3 database 
    Return in format Datframe or cursor
    """
    
    def __init__(self,db_name):
        """Create a connection"""
        self.db_name =db_name
        self.status=False
        try:
            self.connection = sqlite3.connect(self.db_name)
            print(f"Connected to << {self.db_name}>>")
            self.status = True
        except(Exception,sqlite3.Error) as error:
            print("Error while trying connect",error)
    
    def close_connection(self):
        """ Close a connction """
        if self.status:
            self.connection.close()
            print(f"Connection for << {self.db_name} >> is closed")
        else:
            print(f"Connection for << {self.db_name} >> is already closed")
    
    
    def read_database_version(self):
        """ Get current database version """
        try:
            cursor = self.connection.cursor()
            cursor.execute("select sqlite_version();")
            db_version = cursor.fetchone()
            print(f"<< {self.db_name} >> 's version is {db_version}")
            
        except(Exception,sqlite3.Error) as error:
            print(f"Error while getting data",error)
    
    def get_table_names(self):
        """Return all table names in the current database"""
        try:
            cursor = self.connection.cursor()
            query = cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
            records =cursor.fetchall()
            cols = [column[0] for column in query.description]
            cursor.close()
        except sqlite3.Error as error:
            print(f"Failed to read data from sqlite table",error)
        results = pd.DataFrame.from_records(data=records,columns=cols).rename(columns={'name':'Table Name'})
        return results
    
    def read_table_with_df(self,table_name,conditions=None,limit=None):
        """
        Get a table in current database, return the table with format Dataframe
        conditions: SQL query
        limit: number of rows returns
        """
        extra_conditon = ""
        if conditions:
            extra_conditon=f" WHERE {conditions}"
            
        try:
            if limit==None:
                sqlite_query = f"""SELECT * from {table_name}"""+extra_conditon
            else:
                sqlite_query = f"""SELECT * from {table_name} LIMIT {limit}"""+extra_conditon
            df = pd.read_sql(sqlite_query,self.connection)
        except sqlite3.Error as error:
            print("Failed to retrive data from sqlite table")
        return df
    
    def get_column_names_from_table(self,table_name):
        
        """Return a list of column names from a table in database"""
        columns_names=list()
        try:
            cursor =self.connection.cursor()
            table_column_names = 'PRAGMA table_info('+table_name+');'
            cursor.execute(table_column_names)
            records = cursor.fetchall()
            for name in records:
                columns_names.append(name[1])
            
            cursor.close()
        except sqlite3.Error as error:
            print("Failed to get data",error)
            
        return columns_names
    
    def replace_table_with_df(self,table_name,df,replace=False):
        """
        Replace the selected table with Dataframe
        replace=False:append data to the table
        replace=True:replace all data with df
        """
        try:
            if table_name in list(self.get_table_names()['Table Name']):
                print(f"Found table <<{table_name}>> in Database <<{self.db_name}>>")
            else:
                print(f"Attention , creating new table <<{table_name}>> in Database <<{self.db_name}>> ")
            
            if replace:
                df.to_sql(name=table_name,con=self.connection,if_exists="replace", index=False)
            else:
                df.to_sql(name=table_name,con=self.connection,if_exists="append", index=False)
                print("Sql insert process finished.")
        
        except sqlite3.Error as error:
            print("Failed to update",error)
            print("If it's a creation, be careful with columns format and value types")
    
    def __getitem__(self,table_name):
        try:
            return self.read_table_with_df(table_name)
        except:
            raise sqlite3.KeyValueError(f"{table_name} not found in database.")
    
    def update_table(self,table_name,update_values,conditions):
        """
        Update a table with new values and conditons
        update_values:list of update values
        conditions: string / list of SQL expression
        """
        
        updated = update_values
        cond = conditions
        
        if isinstance(updated,list):
            updated = ", ".join(update_values)
        if isinstance(conditions,list):
            cond = " AND ".join(conditions)
        
        sqlite_query = f"UPDATE {table_name} SET {updated} WHERE {cond};"
        print(sqlite_query)
        try:
            cursor = self.connection.cursor()
            cursor.execute(sqlite_query)
            self.connection.commit()
            cursor.close()
            print(f"Update table << {table_name} >> success.")
        except sqlite3.Error as error:
            print(f"Failed to update table {table_name}",error)
            
            
    def delete_table(self,table_name):
        """Remove a table in the current database"""
        try:
            cursor =self.connection.cursor()
            sqlite_query = f"DROP TABLE {table_name};"
            cursor.execute(sqlite_query)
            self.connection.commit()
            cursor.close()
            print(f"Drop table << {table_name} >> success.")
            
        except sqlite3.Error as error:
            print(f"Failed to delete table <<{table_name}>>",error)
            
