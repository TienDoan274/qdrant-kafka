import psycopg2

# Kết nối PostgreSQL
conn = psycopg2.connect(database="file_storage", user="admin", password="password")
cur = conn.cursor()

# Thực thi câu lệnh SELECT để lấy dữ liệu từ bảng files
cur.execute("SELECT * FROM files;")
rows = cur.fetchall()  # Lấy toàn bộ dữ liệu từ kết quả truy vấn

# In dữ liệu ra console
if rows:
    print("Dữ liệu trong bảng 'files':")
    for row in rows:
        print(row)
else:
    print("Bảng 'files' hiện không có dữ liệu.")

# Đóng kết nối
cur.close()
conn.close()
