import sqlite3
import os
import re
import shutil
import time

root = '素材库目录'
os.chdir(root)
db_path = r".bf\billfish.db"

def sanitize_folder_name(folder_name):
      # 替换不允许的字符
    folder_name = re.sub(r'[\\/:*?"<>| ]', "_", folder_name)
      # 处理结尾的空格和句点
    folder_name = folder_name.strip(" .")
    reserved_names = ["CON", "PRN", "AUX", "NUL", 
                    "COM1", "COM2", "COM3", "COM4", "COM5", "COM6", "COM7", "COM8", "COM9", 
                    "LPT1", "LPT2", "LPT3", "LPT4", "LPT5", "LPT6", "LPT7", "LPT8", "LPT9"]
    if folder_name.upper() in reserved_names:
       folder_name += '_'
    return folder_name

conn = sqlite3.connect(db_path)
cursor = conn.cursor()
cursor.execute(f"select id from bf_folder where name='待处理';")
pid_undeal = cursor.fetchall()[0][0]
cursor.execute(f"select id, name from bf_file where pid={pid_undeal};")
results = cursor.fetchall()
for img in results:
    cursor.execute(f"select note from bf_material_userdata where file_id={img[0]};")
    result = cursor.fetchall()
    if len(result) > 0:
        result_ = result[0][0]
        match = re.search(r"Artist:(.+)", result_)
    else:
        match = None  
    match = re.search(r"Artist:(.+)", result)
    if not match:
        print('Cant deal', img[1])
        fold_name = 'CantDeal'
    else:
        fold_name = match.group(1)
        fold_name = sanitize_folder_name(fold_name.strip())
    if os.path.exists(fold_name):
        # 获取pid
        cursor.execute(f"select id from bf_folder where name='{fold_name}'")
        pid = cursor.fetchall()[0][0]    
    else:
        os.makedirs(fold_name)
        cursor.execute(f"insert into bf_folder ('born', 'name', 'pid', 'desc', 'cover_tid', 'hide', 'seq', 'color', 'is_recycle') values ({int(time.time())}, '{fold_name}', 0, '', 0, 0, 0.9, 0, 0);")
        pid = cursor.lastrowid
        conn.commit()
        cursor = conn.cursor()
    # 移动文件
    shutil.move(rf"待处理\{img[1]}", rf"{fold_name}\{img[1]}")
    # 更新图片pid   
    cursor.execute(f'update bf_file set pid={pid} where id={img[0]}')
    conn.commit()
    cursor = conn.cursor()
conn.close()
