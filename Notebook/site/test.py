from werkzeug.security import generate_password_hash, check_password_hash
import sqlite3

conn = sqlite3.connect('notebook.sqlite3')
fh = conn.cursor()
pass_hash = fh.execute("select pass_hash from authentication where username='creator'")
p_hash = fh.fetchone()
print(f"Your hash is : {p_hash[0]}")
