import pandas as pd
import sqlite3

def read_data(u):
    #Connect to Database
    conn = sqlite3.connect('./tm_db.db')
    #Use this run sql statements
    query = "select * from journal where username = ?;"
    params = (u,)  #The parameter must be a tuple
    r_df = pd.read_sql(query, conn, params=params)
    return r_df
