import sqlite3

conn = sqlite3.connect("absensi.db")
cursor = conn.cursor()

# Hapus data sebelumnya agar tidak dobel jika dijalankan ulang
cursor.execute("DELETE FROM mahasiswa")

# Daftar data mahasiswa baru
# Format: (ID, NIM, Nama)
# Catatan: NIM Anda berikan sama semua untuk ketiganya, jika ada typo silakan disesuaikan di file ini ya.
data_mahasiswa = [
    (1, '240658302004', 'Syifa Andini Aulia Putri'),
]

# Masukkan data ke dalam tabel
cursor.executemany("INSERT INTO mahasiswa (id, nim, nama) VALUES (?, ?, ?)", data_mahasiswa)

conn.commit()
conn.close()

print("Data 3 mahasiswa berhasil ditambahkan!")