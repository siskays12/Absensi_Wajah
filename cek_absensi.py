import sqlite3
import pandas as pd

conn = sqlite3.connect("absensi.db")

print("--- Data Absensi ---")
try:
    df = pd.read_sql_query("SELECT * FROM absensi", conn)
    print(df)
except Exception as e:
    print("Belum ada data atau tabel belum dibuat:", e)

conn.close()
