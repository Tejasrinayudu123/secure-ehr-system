import sqlite3
import matplotlib.pyplot as plt

conn = sqlite3.connect("ehr_demo.sqlite3")
cursor = conn.cursor()

rows = cursor.execute("""
SELECT LENGTH(ciphertext), LENGTH(nonce), LENGTH(wrapped_key)
FROM medical_records
""").fetchall()

conn.close()

total_sizes = [c + n + k for c, n, k in rows]

plt.hist(total_sizes, bins=20)
plt.title("Total Encryption Storage per Record")
plt.xlabel("Bytes")
plt.ylabel("Number of Records")

plt.savefig("storage_distribution.png")
plt.show()