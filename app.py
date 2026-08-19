from flask import Flask, render_template_string, request, redirect, url_for, flash
import mysql.connector
from werkzeug.security import check_password_hash
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField
from wtforms.validators import DataRequired

app = Flask(__name__)
app.secret_key = 'your_secret_key'  # Replace with your actual secret key

# Database connection function
def connect_to_database():
    try:
        conn = mysql.connector.connect(
            host="localhost",
            user="root",
            password="password",
            database="mydatabase"
        )
        return conn
    except mysql.connector.Error as err:
        print(f"Error: {err}")
        return None

# Define the login form
class LoginForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])
    submit = SubmitField('Login')

@app.route('/', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        username = form.username.data
        password = form.password.data

        conn = connect_to_database()
        if conn:
            cursor = conn.cursor(dictionary=True)
            cursor.execute("SELECT * FROM users WHERE username = %s", (username,))
            user = cursor.fetchone()

            if user and check_password_hash(user['password'], password):
                return redirect(url_for('success'))
            else:
                flash('Invalid username or password.')

            conn.close()
        else:
            flash('Failed to connect to the database.')

    # Render a simple login form with a colorful background
    return render_template_string('''
        <!DOCTYPE html>
        <html lang="en">
        <head>
            <meta charset="UTF-8">
            <meta name="viewport" content="width=device-width, initial-scale=1.0">
            <title>Login Page</title>
            <style>
                body {
                    background: linear-gradient(to right, #ff7e5f, #feb47b);
                    display: flex;
                    justify-content: center;
                    align-items: center;
                    height: 100vh;
                    margin: 0;
                    font-family: Arial, sans-serif;
                }
                .login-container {
                    background: white;
                    padding: 20px;
                    border-radius: 10px;
                    box-shadow: 0 0 10px rgba(0, 0, 0, 0.1);
                }
                .login-container input {
                    width: 100%;
                    padding: 10px;
                    margin: 10px 0;
                    border: 1px solid #ddd;
                    border-radius: 5px;
                }
                .login-container button {
                    width: 100%;
                    padding: 10px;
                    background-color: #4CAF50;
                    color: white;
                    border: none;
                    border-radius: 5px;
                    cursor: pointer;
                }
                .login-container button:hover {
                    background-color: #45a049;
                }
                .alert {
                    color: red;
                    margin-top: 10px;
                }
            </style>
        </head>
        <body>
            <div class="login-container">
                <form method="post">
                    {{ form.username.label }}
                    {{ form.username() }}
                    {{ form.password.label }}
                    {{ form.password() }}
                    {{ form.submit() }}
                </form>
                {% with messages = get_flashed_messages() %}
                    {% if messages %}
                        <div class="alert">
                            {% for message in messages %}
                                <p>{{ message }}</p>
                            {% endfor %}
                        </div>
                    {% endif %}
                {% endwith %}
            </div>
        </body>
        </html>
    ''')

@app.route('/success')
def success():
    return 'Login successful!'

if __name__ == '__main__':
    app.run(debug=True)
