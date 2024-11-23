import psycopg2
import random
import bcrypt
import sys

# Cấu hình in Unicode
sys.stdout.reconfigure(encoding='utf-8')

def hash_password(password):
    """
    Hash mật khẩu sử dụng bcrypt
    """
    salt = bcrypt.gensalt()
    hashed = bcrypt.hashpw(password.encode('utf-8'), salt)
    return hashed.decode('utf-8')

def create_table_if_not_exists(cur, create_table_query):
    """
    Kiểm tra và tạo bảng nếu chưa tồn tại
    """
    table_name = create_table_query.split()[2]  # Lấy tên bảng từ câu lệnh
    cur.execute(f'''
        SELECT EXISTS (
            SELECT 1 
            FROM information_schema.tables 
            WHERE table_name = '{table_name}'
        );
    ''')
    exists = cur.fetchone()[0]
    
    if not exists:
        cur.execute(create_table_query)
        print(f"Table {table_name} created successfully")
    else:
        print(f"Table {table_name} already exists")

def insert_data(cur):
    """
    Chèn dữ liệu vào các bảng
    """
    # Hash mật khẩu khách hàng
    password1 = hash_password("b12345")  # Mật khẩu khách hàng 1
    password2 = hash_password("c09876")  # Mật khẩu khách hàng 2
    
    password3 = hash_password("a01020304")
    # Chèn một tài khoản nhân viên
    cur.execute('''
    INSERT INTO NhanVien (TenNhanVien, SDTNhanVien, MatKhau) 
    VALUES ('nguyenvana','0123456789', %s);
''', (password3,))


    # Chèn 2 tài khoản khách hàng với mật khẩu
    cur.execute('''
        INSERT INTO KhachHang (TenKhachHang, SDT, MatKhau) 
        VALUES 
        ('tranthib', '0987654321', %s),
        ('Levanc', '0123456780', %s);
    ''', (password1, password2))

    # Chèn 4 tác giả
    cur.execute('''
        INSERT INTO TacGia (TenTacGia) 
        VALUES 
        ('Nguyễn Văn X'),
        ('Nguyễn Văn B'),
        ('Nguyễn Văn C'),
        ('Nguyễn Văn D');
    ''')

    # Chèn 3 nhà xuất bản
    cur.execute('''
        INSERT INTO NXB (TenNXB, SDTNXB) 
        VALUES 
        ('NXB ABC', '0123456789'),
        ('NXB AAB', '0223456789'),
        ('NXB AAA', '0323456789');
    ''')

    # Chèn 10 sản phẩm với IDTacGia, IDNXB ngẫu nhiên
    for i in range(1, 11):
        id_tacgia = random.randint(1, 4)  # Giả sử có 4 tác giả
        id_nxb = random.randint(1, 3)     # Giả sử có 3 nhà xuất bản
        cur.execute(f'''
            INSERT INTO SanPham (TenSanPham, GiaBan, IDTacGia, IDNXB, IDNhanVien) 
            VALUES ('Sản phẩm {i}', {i * 100}, {id_tacgia}, {id_nxb}, 1);
        ''')

    # Chèn 5 kho hàng với sản phẩm ngẫu nhiên
    for i in range(1, 6):
        id_sanpham = random.randint(1, 10)  # Giả sử có 10 sản phẩm
        soluong = random.randint(50, 200)   # Số lượng ngẫu nhiên từ 50 đến 200
        cur.execute(f'''
            INSERT INTO KhoHang (TenKhoHang, DiaChi, NgayNhapSP, IDSanPham, SoLuong) 
            VALUES ('Kho {i}', 'Địa chỉ {i}', CURRENT_DATE, {id_sanpham}, {soluong});
        ''')

try:
    # Kết nối với cơ sở dữ liệu
    conn = psycopg2.connect(
        database="demodb", 
        user="postgres", 
        password="200418", 
        host="127.0.0.1", 
        port="5432"
    )
    print("Opened database successfully")

    # Tạo con trỏ
    cur = conn.cursor()

    # Câu lệnh tạo bảng
    create_queries = [
        '''CREATE TABLE NhanVien
        (
            IDNhanVien SERIAL PRIMARY KEY NOT NULL,
            TenNhanVien TEXT,
            SDTNhanVien CHAR(15) UNIQUE,
            MatKhau TEXT NOT NULL 
        );''',

        '''CREATE TABLE TacGia
        (
            IDTacGia SERIAL PRIMARY KEY NOT NULL,
            TenTacGia TEXT NOT NULL
        );''',

        '''CREATE TABLE NXB
        (
            IDNXB SERIAL PRIMARY KEY NOT NULL,
            TenNXB TEXT NOT NULL,
            SDTNXB CHAR(15)
        );''',

        '''CREATE TABLE KhachHang
        (
            MaKhachHang SERIAL PRIMARY KEY NOT NULL,
            TenKhachHang TEXT,
            SDT CHAR(15) UNIQUE,
            MatKhau TEXT NOT NULL -- Thêm cột MatKhau
        );''',

        '''CREATE TABLE SanPham
        (
            IDSanPham SERIAL PRIMARY KEY NOT NULL,
            TenSanPham TEXT NOT NULL,
            GiaBan REAL,
            IDNhanVien INT REFERENCES NhanVien(IDNhanVien) ON DELETE SET NULL ON UPDATE CASCADE,
            IDTacGia INT REFERENCES TacGia(IDTacGia) ON DELETE SET NULL ON UPDATE CASCADE,
            IDNXB INT REFERENCES NXB(IDNXB) ON DELETE SET NULL ON UPDATE CASCADE
        );''',

        '''CREATE TABLE HoaDon
        (
            MaHoaDon SERIAL PRIMARY KEY NOT NULL,
            SoLuong INT,
            NgayBanSP DATE,
            TongTien NUMERIC,  -- Thêm cột TongTien để lưu tổng tiền
            IDSanPham INT REFERENCES SanPham(IDSanPham) ON DELETE CASCADE ON UPDATE CASCADE,
            MaKhachHang INT,  -- Chỉ định kiểu dữ liệu cho cột
            FOREIGN KEY (MaKhachHang) REFERENCES KhachHang(MaKhachHang) ON DELETE CASCADE ON UPDATE CASCADE
        );''',

        '''CREATE TABLE KhoHang (
            IDKho SERIAL PRIMARY KEY,
            TenKhoHang TEXT,
            DiaChi TEXT,
            NgayNhapSP DATE,
            IDSanPham INT REFERENCES SanPham(IDSanPham) ON DELETE SET NULL ON UPDATE CASCADE,
            SoLuong INT NOT NULL
        );'''
    ]

    # Tạo các bảng nếu chưa tồn tại
    for query in create_queries:
        create_table_if_not_exists(cur, query)

    # Chèn dữ liệu vào các bảng
    insert_data(cur)

    # Commit thay đổi và đóng kết nối
    conn.commit()
    cur.close()
    conn.close()
    print("Data inserted successfully")

except Exception as e:
    print(f"An error occurred: {e}")
