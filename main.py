from flask import Flask, render_template, redirect, url_for, request
from flask_login import LoginManager, UserMixin, login_user, logout_user, login_required
from flask_mysqldb import MySQL
from config import MYSQL_CONFIG, APP_CONFIG
import bcrypt

app = Flask(__name__)
app.secret_key = APP_CONFIG['SECRET_KEY']

# Load MySQL configurations from config file
app.config['MYSQL_HOST'] = MYSQL_CONFIG['host']
app.config['MYSQL_USER'] = MYSQL_CONFIG['user']
app.config['MYSQL_PASSWORD'] = MYSQL_CONFIG['password']
app.config['MYSQL_DB'] = MYSQL_CONFIG['db']
app.config['MYSQL_CURSORCLASS'] = MYSQL_CONFIG['cursorclass']

# Initialize Flask-Login
login_manager = LoginManager()
login_manager.init_app(app)

# Initialize MySQL
mysql = MySQL(app)

# Mock User Class
class User(UserMixin):
    def __init__(self, username, password):
        self.id = username
        self.password = password

# User Loader Function
@login_manager.user_loader
def load_user(user_id):
    cur = mysql.connection.cursor()
    cur.execute("SELECT * FROM users WHERE username = %s", (user_id,))
    user = cur.fetchone()
    cur.close()
    if user:
        return User(user['username'], user['password'])
    return None

# Routes
@app.route('/')
def index():
    return render_template('index.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        print(request.form)
        username = request.form['username']
        password = request.form['password']
        
        print(username, "and", password)
        cur = mysql.connection.cursor()
        cur.execute("SELECT * FROM users WHERE username = %s", (username,))
        user = cur.fetchone()
        cur.close()
        print(user)
        # print(user['username'], "and", user['password'])
        
        if user and bcrypt.checkpw(password.encode('utf-8'), user['password'].encode('utf-8')):
            login_user(User(user['username'], user['password']))
            
            print("I am verified!")
            return redirect(url_for('protected', username=username))
    return render_template('login.html')

@app.route('/protected')
@login_required
def protected():
    return f"Hello, {load_user(request.args.get('username')).id}! This is a protected page."

@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('index'))

if __name__ == '__main__':
    app.run(debug=True)