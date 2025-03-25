
import pyodbc
import pandas as pd
from datetime import datetime
import os

# Define the connection string for your SQL Server
conn_str = r'DRIVER={ODBC Driver 17 for SQL Server};SERVER=EMS-PF56Z9E8\SQLEXPRESS;DATABASE=Gwen;Trusted_Connection=yes;'

# Create a connection to the SQL Server database
conn = pyodbc.connect(conn_str)
cursor = conn.cursor()

# Define the path to your CSV file (use raw string literal to avoid escape issues)
file_path = r'C:\Users\KyleDukes\Repos\dataVailidation\Customers 20250320(Data).csv'  # Replace with your actual file path

# Extract the file name from the file path
fileName = os.path.basename(file_path)  # This extracts 'Customers 20250320(Data).csv'

# Read the CSV file into a pandas DataFrame
df = pd.read_csv(file_path)

# Strip leading/trailing spaces from the column names
df.columns = df.columns.str.strip()

# Get the current timestamp for the loadDate column
loadDate = datetime.now()

def validateValue(value):
    if pd.isna(value) or str(value).strip == '':
        return None
    return value

for index, row in df.iterrows():
    try:
        row_data = [
            validateValue(row['Selected']),
            validateValue(row['Customer ID']),
            validateValue(row['Customer Name']),
            validateValue(row['Customer Class']),
            validateValue(row['City']),
            validateValue(row['State']),
            validateValue(row['Terms']),
            validateValue(row['Customer Status']),
            validateValue(row['Restrict Visibility To']),
            validateValue(row['Time Zone']),
            validateValue(row['Tax Zone']),
            validateValue(row['Parent Account ID']),
            validateValue(row['Billing Email']),
            validateValue(row['Primary Email']),
            validateValue(row['Open Balance']),
            validateValue(row['Price Class']),
            validateValue(row['Billing Cycle']),
            validateValue(row['Send Appointment Email']),
            validateValue(row['Send Invoices by Email']),
            validateValue(row['Default Payment Method']),
            validateValue(row['Print Invoices']),
            validateValue(row['Last Modified By']),
            validateValue(row['Print Statements']),
            validateValue(row['Send Statements by Email']),
            validateValue(row['Credit Verification']),
            validateValue(row['Statement Cycle ID']),
            validateValue(row['AR Rep Name']),
            validateValue(row['AR Rep Email']),
            validateValue(row['Managed By Third Party']),
            validateValue(row['Account Name']),
            validateValue(row['Created On'])
            ]

        row_data.extend([loadDate])
        row_data.extend([fileName])

    # Iterate through the rows of the dataframe and insert them into the ValidationTable1 table
        cursor.execute("""
            INSERT INTO ValidationTable1 (
                [Selected], [Customer ID], [Customer Name], [Customer Class], [City], 
                [State], [Terms], [Customer Status], [Restrict Visibility To], [Time Zone], 
                [Tax Zone], [Parent Account ID], [Billing Email], [Primary Email], [Open Balance], 
                [Price Class], [Billing Cycle], [Send Appointment Email], [Send Invoices by Email], 
                [Default Payment Method], [Print Invoices], [Last Modified By], [Print Statements], 
                [Send Statements by Email], [Credit Verification], [Statement Cycle ID], [AR Rep Name], 
                [AR Rep Email], [Managed By Third Party], [Account Name], [Created On], [loadDate], [fileName]
            )
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        """, *row_data)
       
    except KeyError as e:
        print(f"KeyError: {e} not found in row. Skipping this row.")
        continue  # Skip this row and continue with the next one

# Commit the transaction to insert the data
conn.commit()

# Close the cursor and connection
cursor.close()
conn.close()

print(f"Data imported successfully with loadDate and file name '{fileName}'.")
