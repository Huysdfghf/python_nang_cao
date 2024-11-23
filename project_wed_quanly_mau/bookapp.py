import bcrypt
from database import Database

class BookStoreApp:
    def __init__(self):
        # Khởi tạo đối tượng cơ sở dữ liệu
        self.db = Database("demodb", "postgres", "200418", "127.0.0.1", "5432")

    def register(self, username, password, sdt):
        """Đăng ký người dùng mới"""
        if not username or not password or not sdt:
            return {"error": "Tên đăng nhập, mật khẩu và số điện thoại không được để trống."}
        
        # Mã hóa mật khẩu
        hashed_password = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())
        
        try:
            # Thực hiện truy vấn thêm khách hàng với mật khẩu đã mã hóa và số điện thoại
            self.db.execute_query(
                "INSERT INTO KhachHang (TenKhachHang, MatKhau, SDT) VALUES (%s, %s, %s)",
                (username, hashed_password.decode('utf-8'), sdt)  # Thêm số điện thoại vào truy vấn
            )
            return {"success": "Đăng ký thành công!"}
        except Exception as e:
            return {"error": f"Đã xảy ra lỗi khi đăng ký: {e}"}


    def login(self, username, password):
        """Đăng nhập người dùng"""
        try:
            # Kiểm tra nếu mật khẩu không hợp lệ (None hoặc rỗng)
            if not password:
                return {"error": "Mật khẩu không được để trống!"}
            
            # Kiểm tra thông tin đăng nhập của khách hàng
            customer = self.db.execute_query(
                "SELECT * FROM KhachHang WHERE TenKhachHang = %s",
                (username,)
            )
            if customer:
                stored_password = customer[0][3]  # Cột MatKhau nằm ở vị trí thứ 2
                # Kiểm tra mật khẩu với bcrypt
                if bcrypt.checkpw(password.encode('utf-8'), stored_password.encode('utf-8')):  # Encode mật khẩu người dùng nhập vào
                    customer_id = customer[0][0]
                    return {"user_type": "customer", "username": customer_id}
            
            # Kiểm tra thông tin đăng nhập của nhân viên
            employee = self.db.execute_query(
                "SELECT * FROM NhanVien WHERE SDTNhanVien = %s",
                (username,)
            )
            if employee:
                stored_password = employee[0][3]  # Cột MatKhau nằm ở vị trí thứ 2
                # Kiểm tra mật khẩu với bcrypt
                if bcrypt.checkpw(password.encode('utf-8'), stored_password.encode('utf-8')):  # Encode mật khẩu người dùng nhập vào
                    employee_id = employee[0][0]  # Giả sử ID nhân viên là trường đầu tiên trong bảng
                    return {"user_type": "employee", "employee_id": employee_id}
            
            # Nếu không tìm thấy người dùng, trả về lỗi
            return {"error": "Thông tin đăng nhập không hợp lệ"}
        
        except Exception as e:
            return {"error": f"Đã xảy ra lỗi khi đăng nhập: {e}"}


    def close_app(self):            
        """Đóng kết nối cơ sở dữ liệu"""
        self.db.close()
