from flask import Flask, request, render_template

app = Flask(__name__, template_folder='templates')
@app.route('/', methods=['GET'])
def index():
    return render_template('login.html')

@app.route('/login', methods=['POST'])
def login():
    email = request.form['email']
    password = request.form['password']
    # Store the email and password in variables
    print(f"Email: {email}, Password: {password}")
    # You can also store the credentials in a database or a secure storage
    return "Login successful!"

if __name__ == '__main__':
    app.run(debug=True)