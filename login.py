import sqlite3
import hashlib
import getpass

# 1. Inisialisasi Database SQLite
def init_db():
    conn = sqlite3.connect("database_user.db")
    cursor = conn.cursor()
    # Membuat tabel users jika belum ada
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT UNIQUE NOT NULL,
            password TEXT NOT NULL
        )
    """)
    conn.commit()
    conn.close()

# Fungsi untuk mengenkripsi password menggunakan SHA-256
def hash_password(password):
    return hashlib.sha256(password.encode()).hexdigest()

# 2. Fungsi Registrasi
def register():
    print("\n=== MENU REGISTRASI ===")
    username = input("Masukkan username baru : ").strip()
    
    # Menggunakan getpass agar password tidak terlihat saat diketik (opsional, aman di terminal)
    password = getpass.getpass("Masukkan password       : ")
    confirm_password = getpass.getpass("Konfirmasi password     : ")

    if password != confirm_password:
        print("[!] Error: Password tidak cocok. Silakan coba lagi.")
        return

    if not username or not password:
        print("[!] Error: Username dan password tidak boleh kosong.")
        return

    hashed_pw = hash_password(password)

    try:
        conn = sqlite3.connect("database_user.db")
        cursor = conn.cursor()
        
        # Masukkan data ke database
        cursor.execute("INSERT INTO users (username, password) VALUES (?, ?)", (username, hashed_pw))
        conn.commit()
        print(f"[Sukses] Akun dengan username '{username}' berhasil didaftarkan!")
        
    except sqlite3.IntegrityError:
        print(f"[!] Error: Username '{username}' sudah digunakan. Pilih username lain.")
    finally:
        conn.close()

# 3. Fungsi Login
def login():
    print("\n=== MENU LOGIN ===")
    username = input("Masukkan username : ").strip()
    password = getpass.getpass("Masukkan password : ")

    hashed_pw = hash_password(password)

    conn = sqlite3.connect("database_user.db")
    cursor = conn.cursor()

    # Periksa apakah username dan password cocok di database
    cursor.execute("SELECT * FROM users WHERE username = ? AND password = ?", (username, hashed_pw))
    user = cursor.fetchone()
    conn.close()

    if user:
        print(f"\n[Sukses] Login berhasil! Selamat datang, {username}.")
        dashboard(username)
    else:
        print("[!] Error: Username atau password salah.")

# 4. Menu Utama Setelah Login
def dashboard(username):
    while True:
        print(f"\n--- DASHBOARD [Login sebagai: {username}] ---")
        print("1. Lihat Profil")
        print("2. Logout")
        
        pilihan = input("Pilih menu (1/2): ").strip()
        
        if pilihan == "1":
            print(f"\n[Info Profil] Username Anda terdaftar di sistem: {username}")
        elif pilihan == "2":
            print("[Info] Anda telah logout.")
            break
        else:
            print("[!] Pilihan tidak valid, silakan coba lagi.")

# 5. Program Utama (Main Menu)
def main():
    init_db()
    
    while True:
        print("\n===============================")
        print("   APLIKASI LOGIN & REGISTER   ")
        print("===============================")
        print("1. Login")
        print("2. Registrasi Akun Baru")
        print("3. Keluar")
        
        pilihan = input("Silakan pilih menu (1-3): ").strip()
        
        if pilihan == "1":
            login()
        elif pilihan == "2":
            register()
        elif pilihan == "3":
            print("\nTerima kasih telah menggunakan aplikasi ini. Sampai jumpa!")
            break
        else:
            print("[!] Pilihan tidak valid. Masukkan angka 1, 2, atau 3.")

if __name__ == "__main__":
    main()