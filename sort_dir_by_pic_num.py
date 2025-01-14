import sqlite3
import os

root = r""
os.chdir(root)
db_path = r".bf\billfish.db"

conn = sqlite3.connect(db_path)
cursor = conn.cursor()
cursor.execute("select bf_folder.id, count(bf_file.pid) from bf_folder left join bf_file on bf_folder.id=bf_file.pid group by bf_folder.id;")
results = cursor.fetchall()
all_pic_num = sum(map(lambda x:x[1], results))
for i in results:
    seq = 1 - i[1] / all_pic_num
    cursor.execute(f"update bf_folder set seq={seq} where id={i[0]};")
    conn.commit()
conn.close()
