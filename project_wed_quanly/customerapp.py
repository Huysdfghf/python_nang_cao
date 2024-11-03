from database import Database

class CustomerApp:
    def __init__(self, customer_id):
        # Khởi tạo kết nối cơ sở dữ liệu
        self.db = Database("demodb", "postgres", "200418", "127.0.0.1", "5432")
        self.customer_id = customer_id  # Lưu ID của khách hàng

    def check_customer_validity(self):
    # Kiểm tra xem ID khách hàng có hợp lệ không
     return self.customer_id is not None 


    def view_purchases(self):
        """Truy vấn thông tin sách đã mua của khách hàng"""
        if not self.check_customer_validity():
            return {"error": "ID khách hàng không hợp lệ."}
        
        try:
            result = self.db.execute_query(
                "SELECT SanPham.TenSanPham, HoaDon.SoLuong, HoaDon.TongTien, HoaDon.NgayBanSP "
                "FROM HoaDon "
                "JOIN SanPham ON HoaDon.idSanPham = SanPham.idSanPham "
                "JOIN KhachHang ON HoaDon.maKhachHang = KhachHang.maKhachHang "
                "WHERE KhachHang.maKhachHang = %s", (self.customer_id,)
            )
            return result  # Đảm bảo result là danh sách
        except Exception as e:
            print(f"Error in view_purchases: {e}")  # Ghi lại lỗi cụ thể
            return {"error": f"Đã xảy ra lỗi khi lấy thông tin sách đã mua: {e}"}


    def logout(self):
        """Đóng kết nối cơ sở dữ liệu"""
        self.db.close()
