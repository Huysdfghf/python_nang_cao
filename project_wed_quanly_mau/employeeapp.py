from database import Database

class EmployeeApp:
    def __init__(self, employee_id):
        self.db = Database("demodb", "postgres", "200418", "127.0.0.1", "5432")
        self.employee_id = employee_id

    def add_book(self, book_name, author_id, price, publisher_id):
        if not book_name or not author_id.isdigit() or not price.isdigit() or not publisher_id.isdigit():
            return {"error": "Vui lòng nhập đầy đủ thông tin hợp lệ."}
        
        try:
            self.db.execute_query(
                "INSERT INTO SanPham (TenSanPham, GiaBan, IDTacGia, IDNXB, IDNhanVien) VALUES (%s, %s, %s, %s, %s)",
                (book_name, int(price), int(author_id), int(publisher_id), int(self.employee_id))
            )
            return {"success": "Thêm sách thành công!"}
        except Exception as e:
            return {"error": f"Đã xảy ra lỗi khi thêm sách: {e}"}

    def add_to_inventory(self, book_id, quantity, inventory_name, inventory_address):
        if not book_id.isdigit() or not quantity.isdigit():
            return {"error": "Vui lòng nhập thông tin hợp lệ."}
        
        try:
            self.db.execute_query(
                "INSERT INTO KhoHang (TenKhoHang, DiaChi, NgayNhapSP, IDSanPham, SoLuong) VALUES (%s, %s, CURRENT_DATE, %s, %s)",
                (inventory_name, inventory_address, int(book_id), int(quantity))
            )
            return {"success": "Nhập kho thành công!"}
        except Exception as e:
            return {"error": f"Đã xảy ra lỗi khi nhập kho: {e}"}

    def add_author(self, author_name):
        if not author_name:
            return {"error": "Vui lòng nhập tên tác giả hợp lệ."}

        try:
            self.db.execute_query(
                "INSERT INTO TacGia (TenTacGia) VALUES (%s)",
                (author_name,)
            )
            return {"success": "Thêm tác giả thành công!"}
        except Exception as e:
            return {"error": f"Đã xảy ra lỗi khi thêm tác giả: {e}"}

    def add_publisher(self, publisher_name, publisher_phone):
        if not publisher_name or not publisher_phone:
            return {"error": "Vui lòng nhập thông tin nhà xuất bản hợp lệ."}

        try:
            self.db.execute_query(
                "INSERT INTO NXB (Tennxb, sdtnxb) VALUES (%s, %s)",
                (publisher_name, publisher_phone)
            )
            return {"success": "Thêm nhà xuất bản thành công!"}
        except Exception as e:
            return {"error": f"Đã xảy ra lỗi khi thêm nhà xuất bản: {e}"}
        
    def view_inventory(self, book_id=None):
        """
        Xem kho hàng. Nếu cung cấp book_id, chỉ hiển thị thông tin cho sản phẩm với ID tương ứng.
        Nếu không, hiển thị tổng số lượng tất cả các sản phẩm.
        """
        try:
            if book_id :  # Nếu có ID sách và là số hợp lệ
                # Truy vấn thông tin của một sản phẩm cụ thể
                result = self.db.execute_query(
                    """
                    SELECT KhoHang.IDSanPham, SanPham.TenSanPham, SUM(KhoHang.SoLuong) AS TongSoLuong
                    FROM KhoHang 
                    JOIN SanPham ON KhoHang.IDSanPham = SanPham.IDSanPham 
                    WHERE KhoHang.IDSanPham = %s
                    GROUP BY KhoHang.IDSanPham, SanPham.TenSanPham
                    """,
                    (int(book_id),)
                )
                if result:
                    return result  # Trả về thông tin sản phẩm theo ID
                else:
                    return {"error": "Không tìm thấy sản phẩm với ID này trong kho."}
            else:
                # Truy vấn tổng số lượng tất cả sản phẩm
                result = self.db.execute_query(
                    """
                    SELECT KhoHang.IDSanPham, SanPham.TenSanPham, SUM(KhoHang.SoLuong) AS TongSoLuong
                    FROM KhoHang 
                    JOIN SanPham ON KhoHang.IDSanPham = SanPham.IDSanPham 
                    GROUP BY KhoHang.IDSanPham, SanPham.TenSanPham
                    """
                )
                if result:
                    return result  # Trả về danh sách tổng số lượng các sản phẩm
                else:
                    return {"error": "Kho hàng hiện không có hàng nào."}
        except Exception as e:
            return {"error": f"Đã xảy ra lỗi khi lấy dữ liệu kho hàng: {e}"}

    def record_sale(self, book_id, quantity, phone):
        if not book_id.isdigit() or not quantity.isdigit() or not phone.isdigit() or len(phone) < 10 or len(phone) > 11:
            return {"error": "Vui lòng nhập thông tin hợp lệ."}
        
        try:
            self.db.execute_query("BEGIN")
            
            # Truy vấn ID của khách hàng từ số điện thoại
            customer_result = self.db.execute_query("SELECT makhachhang FROM KhachHang WHERE SDT = %s", (phone,))
            
            if not customer_result:
                return {"error": "Khách hàng không tồn tại với số điện thoại này."}
            
            customer_id = customer_result[0][0]  # Lấy ID khách hàng
            
            # Kiểm tra số lượng sách có đủ để bán không
            result = self.db.execute_query("SELECT SoLuong FROM KhoHang WHERE IDSanPham = %s", (int(book_id),))

            if result and result[0][0] >= int(quantity):
                self.db.execute_query("UPDATE KhoHang SET SoLuong = SoLuong - %s WHERE IDSanPham = %s", (int(quantity), int(book_id)))
                price_result = self.db.execute_query("SELECT GiaBan FROM SanPham WHERE IDSanPham = %s", (int(book_id),))
                
                if price_result:
                    price = price_result[0][0]
                    total_price = price * int(quantity)
                    self.db.execute_query(
                        "INSERT INTO HoaDon (idSanPham, SoLuong, NgayBanSP, TongTien, makhachhang) VALUES (%s, %s, CURRENT_DATE, %s, %s)",
                        (int(book_id), int(quantity), total_price, customer_id)  # Thêm ID khách hàng vào hóa đơn
                    )
                    self.db.execute_query("COMMIT")
                    return {"success": "Ghi nhận bán hàng và thêm hóa đơn thành công!"}
                else:
                    raise Exception("Không tìm thấy giá sách trong cơ sở dữ liệu.")
            else:
                raise Exception("Số lượng trong kho không đủ.")
        except Exception as e:
            self.db.execute_query("ROLLBACK")
            return {"error": f"Đã xảy ra lỗi khi ghi nhận bán hàng: {e}"}

    def edit_data(self, book_id, new_name, new_price):
        # Kiểm tra đầu vào
        if not book_id.isdigit():
            return {"error": "Vui lòng nhập ID sách hợp lệ."}
        
        if not new_name or not new_price.isdigit():
            return {"error": "Vui lòng nhập tên sách và giá hợp lệ."}

        try:
            # Kiểm tra xem sách có tồn tại không
            existing_book = self.db.execute_query("SELECT * FROM SanPham WHERE IDSanPham = %s", (int(book_id),))
            if not existing_book:
                return {"error": "Sách không tồn tại."}

            # Thực hiện cập nhật thông tin sách
            self.db.execute_query(
                "UPDATE SanPham SET TenSanPham = %s, GiaBan = %s WHERE IDSanPham = %s",
                (new_name, int(new_price), int(book_id))
            )
            return {"success": "Sửa thông tin sách thành công!"}
        except Exception as e:
            return {"error": f"Đã xảy ra lỗi khi sửa thông tin sách: {e}"}


    def delete_data(self, book_id):
        if not book_id.isdigit():
            return {"error": "Vui lòng nhập ID hợp lệ."}
        
        try:
            # Kiểm tra sách có tồn tại không
            result = self.db.execute_query("SELECT * FROM SanPham WHERE IDSanPham = %s", (int(book_id),))
            if not result:
                return {"error": "Sách không tồn tại."}
            
            # Kiểm tra xem sách có còn tồn tại trong kho không
            stock_result = self.db.execute_query("SELECT SoLuong FROM KhoHang WHERE IDSanPham = %s", (int(book_id),))
            if stock_result and stock_result[0][0] > 0:
                return {"error": "Sách vẫn còn tồn tại trong kho, không thể xóa."}
            
            # Nếu không còn hàng trong kho, tiến hành xóa sách
            self.db.execute_query("DELETE FROM SanPham WHERE IDSanPham = %s", (int(book_id),))
            return {"success": "Xóa sách thành công!"}
        
        except Exception as e:
            return {"error": f"Đã xảy ra lỗi khi xóa sách: {e}"}

