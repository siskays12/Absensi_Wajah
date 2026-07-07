import sqlite3

conn = sqlite3.connect("absensi.db")
cursor = conn.cursor()

# Hapus data sebelumnya agar tidak dobel jika dijalankan ulang
cursor.execute("DELETE FROM mahasiswa")

# Daftar data mahasiswa baru
# Format: (ID, NIM, Nama)
data_mahasiswa = [
    (1, '240658302003', 'Syifa Andini Aulia Putri'),
    (2, '240658302006', 'Meishella Indihafsari'),
    (3, '240658302004', 'Siska Yama Sari'),
    (4, '240658302005', 'Nando Juliansyah'),
]

# Masukkan data ke dalam tabel
cursor.executemany("INSERT INTO mahasiswa (id, nim, nama) VALUES (?, ?, ?)", data_mahasiswa)

conn.commit()
conn.close()

print("Data 4 mahasiswa berhasil ditambahkan!")