# Setup file for the edgar_scraper_xbrl
import pymysql
from  sqlalchemy import create_engine

conn = pymysql.connect(host = [host_name], user = [user_name], passwd = [password])
cur = conn.cursor()

cur.execute("create database [database_name]")
cur.execute("use [database_name]")

engine = create_engine("mysql+pymysql://[user_name]: [password]@[host_name]: [port]/[database_name]")

def sp500_database():
    
    df = pd.read_csv('sp500_full_hist.csv')
    df.to_sql(name = "symbol", con = engine, if_exists = "replace", index = False)
    
    return df

df = sp500_database()

###### Things to note #######
# The pupose of this .py file is to create a table that includes metadata for all S&P 500 companies 
# and export it to the database. However, MySQL needs to be setup before the export can be done.
# For the database, creating the engine object is critical for direct importation of the dataframe to database.
# create_engine module from sqlalchemy is used for this purpose, which requires specific path identification
# Format for create_engine:
    # engine = create_engine("mysql+pymysql://[user]: [passwd]@[host]: [port]/[database_name]") 
