import pandas as pd
import psycopg2
from io import StringIO
import os # For managing the file path

# --- 1. Read the spreadsheet data ---
# Save your Excel file as CSV first for an easier process, or use the 'openpyxl' engine for Excel files.
# If using Excel files directly, you'd need 'pip install openpyxl'.
spreadsheet_path = 'your_data.csv' # Replace with your file path
df = pd.read_csv(spreadsheet_path) # Use pd.read_excel() if using .xlsx

# Ensure your DataFrame column names match your PostgreSQL table column names exactly
# Example: df.rename(columns={'OldName': 'new_name'}, inplace=True)

# --- 2. Database connection details ---
DB_NAME = "your_dbname"
DB_USER = "your_user"
DB_PASSWORD = "your_password"
DB_HOST = "localhost" # Or your remote host

# --- 3. Function to perform the upsert ---
def upsert_df_to_postgres(df, table_name, conn):
    # Create a temporary table name
    temp_table_name = f"temp_{table_name}"
    
    # Use pandas to_sql to efficiently create and load data into a temporary table
    # 'if_exists="replace"' drops and recreates the temp table each time
    df.to_sql(temp_table_name, conn, if_exists='replace', index=False)
    
    # Define the target table columns
    columns = ", ".join(df.columns)
    
    # Define the update statements for conflicts
    update_statements = ", ".join([f"{col} = EXCLUDED.{col}" for col in df.columns])
    
    # Construct the MERGE/UPSERT SQL command using ON CONFLICT DO UPDATE
    upsert_query = f"""
    INSERT INTO {table_name} ({columns})
    SELECT {columns} FROM {temp_table_name}
    ON CONFLICT (id_column) DO UPDATE SET
    {update_statements};
    """
    # NOTE: Replace 'id_column' with the name of your actual Primary Key/Unique constraint column.
    
    # Execute the upsert query
    with conn.cursor() as cur:
        cur.execute(upsert_query)
        conn.commit()
        print(f"Upsert complete for table {table_name}. Rows affected: {cur.rowcount}")

# --- 4. Main execution ---
if __name__ == '__main__':
    try:
        # Establish connection
        conn = psycopg2.connect(
            dbname=DB_NAME,
            user=DB_USER,
            password=DB_PASSWORD,
            host=DB_HOST
        )
        
        upsert_df_to_postgres(df, 'your_target_table_name', conn)
        
    except psycopg2.Error as e:
        print(f"Database error: {e}")
    finally:
        if conn:
            conn.close()

