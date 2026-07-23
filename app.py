from flask import Flask, render_template, request, redirect, url_for, flash
from dotenv import load_dotenv
import os


load_dotenv()

app = Flask(__name__)
app.secret_key = os.environ.get('SECRET_KEY')

DATABASE = {
    'ivan' : 'adit'
}

@app.route('/home')
def home():
    return 'home'

@app.route('/', methods=['GET'])
def index():

    return render_template('index.html')


@app.route('/login', methods=['POST'])
def login():
    username = request.form.get('username')
    password = request.form.get('password')

    if username in DATABASE and DATABASE[username] == password:
        return redirect(url_for('home'))

    else:
        flash('Username atau password salah!!')
        return redirect(url_for('index'))

if __name__ == '__main__':
    app.run(debug=True)