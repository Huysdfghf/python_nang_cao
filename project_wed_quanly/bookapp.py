from database import Database

class BookStoreApp:
    def __init__(self):
        # Khởi tạo đối tượng cơ sở dữ liệu
        self.db = Database("demodb", "postgres", "200418", "127.0.0.1", "5432")

    def register(self, username, password):
        """Đăng ký người dùng mới"""
        if not username or not password:
            return {"error": "Tên đăng nhập và mật khẩu không được để trống."}
        
        try:
            # Thực hiện truy vấn thêm khách hàng
            self.db.execute_query("INSERT INTO KhachHang (TenKhachHang, SDT) VALUES (%s, %s)", (username, password))
            return {"success": "Đăng ký thành công!"}
        except Exception as e:
            return {"error": f"Đã xảy ra lỗi khi đăng ký: {e}"}

    def login(self, username, password):
                    try:
                        # Kiểm tra thông tin đăng nhập của khách hàng
                        customer = self.db.execute_query(
                            "SELECT * FROM KhachHang WHERE TenKhachHang = %s AND SDT = %s",
                            (username, password)
                        )
                        if customer:
                            customer_id = customer[0][0]
                            return {"user_type": "customer", "username": customer_id}
                        
                        # Kiểm tra thông tin đăng nhập của nhân viên
                        employee = self.db.execute_query(
                            "SELECT * FROM NhanVien WHERE TenNhanVien = %s AND SDTNhanVien = %s",
                            (username, password)
                        )
                        if employee:
                            employee_id = employee[0][0]  # Giả sử ID nhân viên là trường đầu tiên trong bảng
                            return {"user_type": "employee", "employee_id": employee_id}
                        
                        # Nếu không tìm thấy người dùng, trả về lỗi
                        return {"error": "Thông tin đăng nhập không hợp lệ"}
                    except Exception as e:
                        return {"error": f"Đã xảy ra lỗi khi đăng nhập: {e}"}
    def close_app(self):            
        """Đóng kết nối cơ sở dữ liệu"""
        self.db.close()
