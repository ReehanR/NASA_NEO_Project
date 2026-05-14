import sqlite3

conn = sqlite3.connect("neo.db")
cursor = conn.cursor()

print("ASTEROIDS TABLE:")

cursor.execute("PRAGMA table_info(asteroids)")
for row in cursor.fetchall():
    print(row)

print("\nCLOSE_APPROACH TABLE:")

cursor.execute("PRAGMA table_info(close_approach)")
for row in cursor.fetchall():
    print(row)

conn.close() 
