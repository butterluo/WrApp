import pandas as pd
import mysql.connector
import os
from dotenv import load_dotenv


load_dotenv()
# Define your MySQL database connection parameters
config = {
        'host': os.getenv('azure_sql_host','127.0.0.1'),
        'user': os.getenv('user','luogang'),
        'password': os.getenv('password','mysql'),
        'database': os.getenv('database','tst1'),
        # 'ssl_ca': os.getenv('ssl_ca')  # Path to the SSL CA certificate (optional)
    }

# Define the Excel file path
excel_file = "Mobile_Stock_2.xlsx"

# Define the MySQL table name (changed to "mobile_stock")
table_name = "mobile_stock"

# Load the Excel file into a Pandas DataFrame
df = pd.read_excel(excel_file)

# Connect to the MySQL database
conn = mysql.connector.connect(**config)
cursor = conn.cursor()

# Iterate through each row in the DataFrame and insert into the MySQL table
for index, row in df.iterrows():
    sql = f"INSERT INTO {table_name} (Product_id, Product_Name, Available_Quantity, Mobile_Specs, Product_Price) VALUES (%s, %s, %s, %s, %s)"
    values = (row['Product_id'], row['Product_Name'], row['Available_Quantity'], row['Mobile_Specs'], row['Product_Price'])

    cursor.execute(sql, values)

# Commit the changes and close the database connection
conn.commit()
cursor.close()
conn.close()

print("Data has been successfully inserted into the MySQL table.")
