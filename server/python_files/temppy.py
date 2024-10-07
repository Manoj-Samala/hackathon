from flask import Flask, render_template_string, request, jsonify
import pyodbc

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

app = Flask(__name__)

# Define the HTML template as a string
template = """
<!DOCTYPE html>
<html>
<head>
  <title>Registration Form</title>
  <style>
    /* Add some basic styling to our form */
    form {
      width: 50%;
      margin: 40px auto;
      background-color: #f9f9f9;
      padding: 20px;
      border: 1px solid #ccc;
      border-radius: 10px;
      box-shadow: 0 0 10px rgba(0, 0, 0, 0.1);
    }

    /* Style our form labels and inputs */
    label {
      display: block;
      margin-bottom: 10px;
    }

    label span {
      display: inline-block;
      width: 150px;
      text-align: right;
      margin-right: 10px;
    }

    input[type="text"], input[type="email"], input[type="password"] {
      width: 50%;
      height: 30px;
      margin-bottom: 20px;
      padding: 10px;
      border: 1px solid #ccc;
    }

    input[type="submit"] {
      background-color: #4CAF50;
      color: #fff;
      padding: 10px 20px;
      border: none;
      border-radius: 10px;
      cursor: pointer;
    }

    input[type="submit"]:hover {
      background-color: #3e8e41;
    }
  </style>
</head>
<body>
  <form action="/submit" method="post">
    <label>
      <span>First Name:</span>
      <input type="text" id="firstname" name="firstname" required>
    </label>

    <label>
      <span>Last Name:</span>
      <input type="text" id="lastname" name="lastname" required>
    </label>

    <label>
      <span>Email:</span>
      <input type="email" id="email" name="email" required>
    </label>

    <label>
      <span>Create Password:</span>
      <input type="password" id="password" name="password" required>
    </label>

    <label>
      <span>Confirm Password:</span>
      <input type="password" id="confirmpassword" name="confirmpassword" required>
    </label>

    <center><input type="submit" value="Sign Up"></center>
  </form>
</body>
</html>
"""

# Route to serve the existing userregistration.html file
@app.route('/')
def registration_form():
    return render_template_string(template)

# Route to handle form submission
@app.route('/submit', methods=['POST'])
def submit_form():
    # Retrieve data from the form
    fname = request.form['firstname']
    lname = request.form['lastname']
    email = request.form['email']
    password = request.form['password']
    confirm_password = request.form['confirmpassword']

    # Validate passwords
    if password != confirm_password:
        return jsonify({'error': 'Passwords do not match!'})

    # Insert data into the database
    def run_query(query, params):
        try:
            cursor.execute(query, params)
            connection.commit()
            return True
        except pyodbc.Error as e:
            print(f"Error: {e}")
            return False

    query = "insert into users (firstname,lastname,email,password) values (?, ?, ?, ?)"
    if run_query(query, (fname, lname, email, password)):
        return jsonify({
            'fname': fname,
            'lname': lname,
            'email': email,
            'password': password  # Don't store plain text passwords in real applications
        })
    else:
        return jsonify({'error': 'Failed to insert data into the database'})

if __name__ == '__main__':
    app.run(debug=True)