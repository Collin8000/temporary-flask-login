from flask import Flask, render_template, request, session, redirect, url_for
import sqlite3

app = Flask(__name__)
app.secret_key = 'your_secret_key'

# create database
conn = sqlite3.connect('users.db')
c = conn.cursor()
c.execute('''CREATE TABLE IF NOT EXISTS users
             (username TEXT, password TEXT, email TEXT)''')
conn.commit()
conn.close()

@app.route('/')
def home():
    return render_template('home.html')

@app.route('/signup', methods=['GET', 'POST'])
def signup():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        email = request.form['email']
        
        # validate input
        if not username or not password or not email:
            return render_template('signup.html', error='Please fill out all fields.')
        
        # add user to database
        conn = sqlite3.connect('users.db')
        c = conn.cursor()
        c.execute("INSERT INTO users VALUES (?, ?, ?)", (username, password, email))
        conn.commit()
        conn.close()
        
        return redirect(url_for('login'))
    
    return render_template('signup.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        
        # validate input
        if not username or not password:
            return render_template('login.html', error='Please fill out all fields.')
        
        # check if user exists in database
        conn = sqlite3.connect('users.db')
        c = conn.cursor()
        c.execute("SELECT * FROM users WHERE username=? AND password=?", (username, password))
        user = c.fetchone()
        conn.close()
        
        if user:
            session['username'] = username
            return redirect(url_for('protected'))
        else:
            return render_template('login.html', error='Invalid username or password.')
    
    return render_template('login.html')

@app.route('/protected')
def protected():
    if 'username' in session:
        return render_template('protected.html')
    else:
        return redirect(url_for('login'))

@app.route('/logout')
def logout():
    session.pop('username', None)
    return redirect(url_for('home'))
if __name__ == '__main__':
    app.run(debug=True)