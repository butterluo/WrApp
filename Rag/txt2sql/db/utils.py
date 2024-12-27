import os
from dotenv import load_dotenv
import mysql.connector

#load env variables
load_dotenv('../.env')

config_mysql = {
    'host': os.getenv('MYSQL_HOST'),
    'user': os.getenv('MYSQL_USR','luogang'),
    'password': os.getenv('MYSQL_PASWRD','mysql'),
    'database': 'tst1', #os.getenv('database','tst1'),
    # 'ssl_ca': os.getenv('ssl_ca')  # Path to the SSL CA certificate (optional)
}

conn = mysql.connector.connect(**config_mysql)

cusrmysql = conn.cursor()

def execute_sql(sql):
    try:
        # Execute SQL queries
        cusrmysql.execute(sql)
        result = cusrmysql.fetchall()
    except Exception as e:
        return {
            "error": "SQL执行出错!",
            "error_msg": str(e),
        }

    return result