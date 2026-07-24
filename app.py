import json
from unicodedata import category
from flask import Flask, request, url_for, redirect, jsonify, session
import sqlite3
from datetime import datetime, timedelta
import os
from dotenv import load_dotenv

load_dotenv()

app = Flask(__name__)
app.secret_key = os.getenv('SECRET_KEY')

db = './database/database.db'

def get_db_connection():
    conn = sqlite3.connect(db)
    conn.row_factory = sqlite3.Row
    return conn

# memeriksa username dan password
@app.route('/login', methods=['POST'])
def login():
    data = request.json
    username = data.get('username')
    password = data.get('password')

    conn = get_db_connection()
    user = conn.execute(
        'SELECT * FROM users WHERE username = ? AND password_hash = ?',
        (username, password)
    ).fetchone()
    conn.close

    if user:
        session['user_id'] = user['id']
        return jsonify({
            'status' : 'succes',
            'message' : 'Login Berhasil'
        }), 200

    return jsonify({
        'status' : 'error',
        'message' : 'Username atau password salah'
    }), 401



# Menyimpan data pengeluaran
@app.route('/api/expenses', methods=['POST'])
def add_expenses():
    # Cek apakah user sudah login
    if 'user_id' not in session:
        return jsonify({
            'status' : 'error',
            'message' : 'Belum Login'
        }), 401

    data = request.json
    title = data.get('title')
    amount = data.get('amount')
    category = data.get('category', 'lainnya')
    # jika tanggal tidak di isi dari frontend, maka otomatis menggunakan tanggal hari ini (YYYY-MM-DD)
    date = data.get('date', datetime.now().strftime('%Y-%m-%d'))

    conn = get_db_connection()
    conn.execute(
        'INSERT INTO expenses (user_id, title, amount, category, date) VALUES (?, ?, ? ,? ,?)',
        (session['user_id'], title, amount, category, date)
    )

    conn.commit()
    conn.close()

    return jsonify({
        'status' : 'succes',
        'message' : 'Pengeluaran berhasil dicatat'
    }), 201


# Mengambil data pengeluaran hari ini
@app.route('/api/expenses', methods=['GET'])
def get_expenses():
    if 'user_id' not in session:
        return jsonify({
            'status' : 'error',
            'message' : 'Belum login'
        }), 401

    report_type = request.args.get('type', 'daily')
    today = datetime.now()
    user_id = session['user_id']

    conn = get_db_connection()

    if report_type == 'daily':
        date_str =  today.strftime('%Y-%m-%d')
        query = "SELECT * FROM expenses WHERE user_id = ? AND date = ? ORDER BY date DESC"
        params = (user_id, date_str)

    elif report_type == 'weekly':
        seven_days_ago = (today - timedelta(days=7)).strftime('%Y-%m-%d')
        today_str = today.strftime('%Y-%m-%d')
        query = "SELECT * FROM expenses WHERE user_id = ? AND date BETWEEN ? AND ? ORDER BY date DESC"
        params = (user_id, seven_days_ago, today_str)

    elif report_type == 'monthly':
        # Mengambi bulan ini format (YYYY-MM)
        month_str = today.strftime('%Y-%m')
        query = "SELECT * FROM expenses WHERE user_id = ? AND date LIKE ? ORDER BY date DESC"
        params = (user_id, month_str)

    rows = conn.execute(query, params).fetchall()
    conn.close()

    # Ubah hasil SQLite row ke format JSON/List
    expenses = [dict(row) for row in rows]

    # Hitung total nominal pengeluaran
    total_amount = sum(item['amount'] for item in expenses)

    return jsonify({
        'status' : 'succes',
        'filter' : report_type,
        'total' : total_amount,
        'data' : expenses
    }), 200

if __name__ == '__main__':
    app.run(debug=True, port=5000)
