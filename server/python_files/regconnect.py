import pyodbc

# Define the connection parameters
connection_params = {
    "server": "mynewserverhtn.database.windows.net",
    "database": "mydbwork",
    "username": "manojsamala",
    "password": "Manoj@123",
    "driver": "ODBC Driver 17 for SQL Server"
}

# Create a connection string
connection_string = f"DRIVER={{{connection_params['driver']}}};SERVER={connection_params['server']};DATABASE={connection_params['database']};UID={connection_params['username']};PWD={connection_params['password']}"

# Establish a connection
connection = pyodbc.connect(connection_string)

# Create a cursor object
cursor = connection.cursor()

# Run your custom query
def run_query(query):
    try:
        cursor.execute(query)
        results = cursor.fetchall()
        return results
    except pyodbc.Error as e:
        print(f"Error: {e}")
        return None

# Example usage:
query = "SELECT * FROM users"
results = run_query(query)

# Print the results
for row in results:
    print(row)

# Close the connection
connection.close()


