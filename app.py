from flask import Flask, request, redirect, session, render_template_string, url_for
import csv
import os

app = Flask(__name__)
app.secret_key = 'muchlis_secret_key'

# HTML Templates disatukan
register_html = """
<!DOCTYPE html>
<html lang="id">
<head>
    <meta charset="UTF-8">
    <title>Registrasi</title>
</head>
<body>
    <h2>Form Registrasi</h2>
    <form method="POST">
        Nama Lengkap: <input type="text" name="nama" required><br>
        Email: <input type="email" name="email" required><br>
        No. HP: <input type="text" name="hp" required><br>
        Username: <input type="text" name="username" required><br>
        Password: <input type="password" name="password" required><br>
        <input type="submit" value="Daftar">
    </form>
    <p>Sudah punya akun? <a href="/login">Login di sini</a></p>
</body>
</html>
"""

login_html = """
<!DOCTYPE html>
<html lang="id">
<head>
    <meta charset="UTF-8">
    <title>Login</title>
</head>
<body>
    <h2>Form Login</h2>
    {% if error %}<p style="color:red;">{{ error }}</p>{% endif %}
    <form method="POST">
        Username: <input type="text" name="username" required><br>
        Password: <input type="password" name="password" required><br>
        <input type="submit" value="Login">
    </form>
    <p>Belum punya akun? <a href="/register">Daftar di sini</a></p>
</body>
</html>
"""

index_html = """
<!DOCTYPE html>
<html lang="id">
<head>
    <meta charset="UTF-8">
    <title>Beranda</title>
</head>
<body>
    <h2>Selamat datang, {{ nama }}!</h2>
    <p>Email: {{ email }}</p>
    <p>No. HP: {{ hp }}</p>
    <a href="/logout">Logout</a>
</body>
</html>
"""

# Pastikan file CSV ada
if not os.path.exists('file.csv'):
    with open('file.csv', 'w', newline='') as f:
        writer = csv.writer(f)
        writer.writerow(['nama', 'email', 'hp', 'username'])

if not os.path.exists('file1.csv'):
    with open('file1.csv', 'w', newline='') as f:
        writer = csv.writer(f)
        writer.writerow(['username', 'password'])

@app.route('/')
def home():
    if 'username' not in session:
        return redirect('/login')

    username = session['username']
    with open('file.csv', newline='') as f:
        reader = csv.DictReader(f)
        for row in reader:
            if row['username'] == username:
                return render_template_string(index_html, nama=row['nama'], email=row['email'], hp=row['hp'])
    return "Data tidak ditemukan."

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        nama = request.form['nama']
        email = request.form['email']
        hp = request.form['hp']
        username = request.form['username']
        password = request.form['password']

        # Cek duplikasi username
        with open('file1.csv', newline='') as f:
            reader = csv.DictReader(f)
            for row in reader:
                if row['username'] == username:
                    return "Username sudah digunakan."

        # Simpan ke file.csv dan file1.csv
        with open('file.csv', 'a', newline='') as f1, open('file1.csv', 'a', newline='') as f2:
            writer1 = csv.writer(f1)
            writer2 = csv.writer(f2)
            writer1.writerow([nama, email, hp, username])
            writer2.writerow([username, password])

        return redirect('/login')
    return render_template_string(register_html)

@app.route('/login', methods=['GET', 'POST'])
def login():
    error = None
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        with open('file1.csv', newline='') as f:
            reader = csv.DictReader(f)
            for row in reader:
                if row['username'] == username and row['password'] == password:
                    session['username'] = username
                    return redirect('/')
        error = "Username atau password salah."
    return render_template_string(login_html, error=error)

@app.route('/logout')
def logout():
    session.clear()
    return redirect('/login')

if __name__ == '__main__':
    app.run(debug=True)
