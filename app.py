from flask import Flask, render_template, redirect, url_for, request, session
from python.citrus_detection import detect_disease
import os
import cv2
import sqlite3

app = Flask(__name__)
app.secret_key = os.urandom(24)  # Secret key untuk session

# Database connection
def get_db_connection():
    conn = sqlite3.connect('users.db')
    conn.row_factory = sqlite3.Row
    return conn

# Rute untuk halaman utama (Home)
@app.route('/')
def home():
    if 'user_id' in session:
        return redirect(url_for('detection'))  # Redirect ke halaman deteksi jika user sudah login
    return render_template('index.html')  # Render halaman utama jika belum login

# Rute untuk login
@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        conn = get_db_connection()
        # Cek apakah username dan password cocok di database
        user = conn.execute('SELECT * FROM users WHERE username = ? AND password = ?', (username, password)).fetchone()
        conn.close()
        if user:
            session['user_id'] = user['id']  # Simpan user_id ke session
            session['is_admin'] = user['is_admin']  # Simpan status admin ke session
            return redirect(url_for('home'))  # Redirect ke halaman utama setelah login berhasil
        else:
            return "Invalid credentials"  # Pesan jika login gagal
    return render_template('login.html')  # Render halaman login jika request GET

# Rute untuk logout
@app.route('/logout')
def logout():
    session.pop('user_id', None)  # Menghapus user_id dari session
    session.pop('is_admin', None)  # Menghapus is_admin dari session
    return redirect(url_for('home'))  # Mengarahkan kembali ke halaman utama setelah logout

# Rute untuk halaman register
@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        conn = get_db_connection()
        conn.execute('INSERT INTO users (username, password) VALUES (?, ?)', (username, password))
        conn.commit()
        conn.close()
        return redirect(url_for('login'))  # Redirect ke halaman login setelah registrasi berhasil
    return render_template('register.html')  # Render halaman register jika request GET

# Rute untuk halaman deteksi (upload gambar dan proses)
@app.route('/detection', methods=['GET', 'POST'])
def detection():
    if 'user_id' not in session:
        return redirect(url_for('login'))  # Redirect ke halaman login jika user belum login
    
    if request.method == 'POST':
        # Proses upload gambar dan deteksi (panggil fungsi Python Anda di sini)
        image_file = request.files['image']
        # Simpan gambar, proses, dan ekstrak fitur
        # Simpan hasil ekstraksi fitur ke file CSV
        return "Hasil deteksi akan ditampilkan di sini"
    
    return render_template('detection.html')  # Render halaman deteksi

# Rute untuk halaman tentang kami
@app.route('/about')
def about():
    return render_template('about.html')
# Rute untuk halaman deteksi
@app.route('/detection', methods=['GET', 'POST'])
def detection():
    if 'user_id' not in session:
        return redirect(url_for('login'))  # Redirect ke login jika user belum login
    
    if request.method == 'POST':
        # Mendapatkan file gambar yang diupload
        image_file = request.files['image']
        image_path = os.path.join('uploads', image_file.filename)
        image_file.save(image_path)

        # Jalankan deteksi dan ekstraksi fitur
        thresholded_image = detect_disease(image_path)

        # Simpan gambar hasil thresholding untuk ditampilkan
        output_image_path = os.path.join('static', 'output_image.png')
        cv2.imwrite(output_image_path, thresholded_image)

        return render_template('detection.html', output_image=output_image_path)
    
    return render_template('detection.html')

if __name__ == '__main__':
    app.run(debug=True)
