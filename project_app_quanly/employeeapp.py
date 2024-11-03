import tkinter as tk
from tkinter import messagebox
from tkinter import ttk
from database import Database



class EmployeeApp():
    def __init__(self, master,login_frame,employee_id):
        self.master = master
        self.db = Database("demodb", "postgres", "200418", "127.0.0.1", "5432")
        self.employee_id = employee_id
        self.login_frame = login_frame  # Tham chiếu đến login_frame
        self.employee_frame = self.create_employee_dashboard()
        

    


    def create_employee_dashboard(self):
        self.employee_frame = tk.Frame(self.master)  # Gán Frame cho self.employee_frame
        self.employee_frame.pack()

        tk.Label(self.employee_frame, text="Chào Mừng đến với Bảng Điều Khiển Nhân Viên").pack()
        tk.Button(self.employee_frame, text="Thêm Sách Mới", command=self.add_book).pack()
        tk.Button(self.employee_frame, text="Nhập Kho Hàng", command=self.add_to_inventory).pack()
        tk.Button(self.employee_frame, text="Xem Kho Hàng", command=self.view_inventory).pack()
        tk.Button(self.employee_frame, text="Ghi Nhận Bán Hàng", command=self.record_sale).pack()
        tk.Button(self.employee_frame, text="Sửa Thông Tin Sách", command=self.edit_data).pack()
        tk.Button(self.employee_frame, text="Xóa Sách", command=self.delete_data).pack()
        tk.Button(self.employee_frame, text="Đăng Xuất", command=self.logout).pack()

        return self.employee_frame  



    def add_book(self):
        add_window = tk.Toplevel(self.master)
        add_window.title("Thêm Sách Mới")

        tk.Label(add_window, text="Tên Sách:").pack()
        book_name_entry = tk.Entry(add_window)
        book_name_entry.pack()

        tk.Label(add_window, text="ID Tác Giả:").pack()
        author_id_entry = tk.Entry(add_window)
        author_id_entry.pack()

        tk.Label(add_window, text="Giá:").pack()
        price_entry = tk.Entry(add_window)
        price_entry.pack()

        tk.Label(add_window, text="ID Nhà Xuất Bản:").pack()
        publisher_id_entry = tk.Entry(add_window)
        publisher_id_entry.pack()

        def submit_add_book(event=None):
            book_name = book_name_entry.get()
            author_id = author_id_entry.get()
            price = price_entry.get()
            publisher_id = publisher_id_entry.get()
            employee_id = self.employee_id  # Lấy ID nhân viên từ thông tin đăng nhập

            # Kiểm tra tính hợp lệ của dữ liệu đầu vào
            if not book_name or not author_id.isdigit() or not price.isdigit() or not publisher_id.isdigit():
                messagebox.showerror("Lỗi", "Vui lòng nhập đầy đủ thông tin hợp lệ.")
                return

            try:
                # Chèn sản phẩm vào bảng SanPham
                self.db.execute_query(
                    "INSERT INTO SanPham (TenSanPham, GiaBan, IDTacGia, IDNXB, IDNhanVien) VALUES (%s, %s, %s, %s, %s)",
                    (book_name, int(price), int(author_id), int(publisher_id), int(employee_id))
                )

                messagebox.showinfo("Thành Công", "Thêm sách thành công!")
                add_window.destroy()
            except Exception as e:
                messagebox.showerror("Lỗi", f"Đã xảy ra lỗi khi thêm sách: {e}")

        tk.Button(add_window, text="Thêm", command=submit_add_book).pack()
        add_window.bind('<Return>', submit_add_book)


    def add_to_inventory(self):
        inventory_window = tk.Toplevel(self.master)
        inventory_window.title("Nhập Kho Hàng")

        tk.Label(inventory_window, text="ID Sách:").pack()
        book_id_entry = tk.Entry(inventory_window)
        book_id_entry.pack()

        tk.Label(inventory_window, text="Số Lượng Nhập:").pack()
        quantity_entry = tk.Entry(inventory_window)
        quantity_entry.pack()
        tk.Label(inventory_window, text="Tên Kho:").pack()
        inventory_name_entry = tk.Entry(inventory_window)
        inventory_name_entry.pack()

        tk.Label(inventory_window, text="Địa Chỉ Kho:").pack()
        
        inventory_Address_entry = tk.Entry(inventory_window)
        inventory_Address_entry.pack()

        def submit_inventory(event=None):
            book_id = book_id_entry.get()
            quantity = quantity_entry.get()
            inventory_name= inventory_name_entry.get()
            inventory_Address=inventory_Address_entry.get()

            # Kiểm tra tính hợp lệ của dữ liệu đầu vào
            if not book_id.isdigit() or not quantity.isdigit():
                messagebox.showerror("Lỗi", "Vui lòng nhập thông tin hợp lệ.")
                return

            try:
                # Chèn số lượng vào bảng KhoHang
                self.db.execute_query(
                    "INSERT INTO KhoHang (TenKhoHang, DiaChi, NgayNhapSP, IDSanPham, SoLuong) VALUES (%s, %s, CURRENT_DATE, %s, %s)",
                    (inventory_name,inventory_Address,int(book_id), int(quantity))
                )

                messagebox.showinfo("Thành Công", "Nhập kho thành công!")
                inventory_window.destroy()
            except Exception as e:
                messagebox.showerror("Lỗi", f"Đã xảy ra lỗi khi nhập kho: {e}")

        tk.Button(inventory_window, text="Nhập Kho", command=submit_inventory).pack()
        inventory_window.bind('<Return>', submit_inventory)

    

    def view_inventory(self):
        inventory_window = tk.Toplevel(self.master)
        inventory_window.title("Kho Hàng")

        # Thêm Frame chứa các nút chức năng
        frame = tk.Frame(inventory_window)
        frame.pack(pady=10)

        # Tạo một nút để tìm kiếm theo ID sản phẩm
        tk.Button(frame, text="Tìm kiếm sản phẩm trong kho", command=self.search_product_in_inventory).pack(side=tk.LEFT, padx=10)
        
        # Tạo một nút để hiển thị kho hàng với Group By
        tk.Button(frame, text="Xem kho hàng (Group By)", command=self.view_grouped_inventory).pack(side=tk.LEFT, padx=10)

        # Thêm nút Đóng
        tk.Button(inventory_window, text="Đóng", command=inventory_window.destroy).pack(pady=10)

    def search_product_in_inventory(self):
        inventory_window = tk.Toplevel(self.master)
        inventory_window.title("Tìm kiếm Sản Phẩm trong Kho")

        # Thêm label và entry để nhập ID sản phẩm
        tk.Label(inventory_window, text="Nhập ID Sản Phẩm:").pack()
        product_id_entry = tk.Entry(inventory_window)
        product_id_entry.pack()

        # Tạo Treeview để hiển thị dữ liệu kho hàng
        tree = ttk.Treeview(inventory_window, columns=("ID", "Tên Sản Phẩm", "Tên Kho Hàng", "Số Lượng"), show="headings")
        tree.heading("ID", text="ID Sản Phẩm")
        tree.heading("Tên Sản Phẩm", text="Tên Sản Phẩm")
        tree.heading("Tên Kho Hàng", text="Tên Kho Hàng")
        tree.heading("Số Lượng", text="Số Lượng")

        tree.column("ID", width=100, anchor='center')
        tree.column("Tên Sản Phẩm", width=200, anchor='center')
        tree.column("Tên Kho Hàng", width=150, anchor='center')
        tree.column("Số Lượng", width=100, anchor='center')

        tree.pack(fill=tk.BOTH, expand=True)

        def show_inventory_for_product():
            product_id = product_id_entry.get()

            if not product_id.isdigit():
                messagebox.showerror("Lỗi", "Vui lòng nhập ID sản phẩm hợp lệ.")
                return

            try:
                # Lấy dữ liệu từ bảng KhoHang cho ID sản phẩm cụ thể
                result = self.db.execute_query(
                    "SELECT KhoHang.IDSanPham, SanPham.TenSanPham, KhoHang.TenKhoHang, KhoHang.SoLuong "
                    "FROM KhoHang "
                    "JOIN SanPham ON KhoHang.IDSanPham = SanPham.IDSanPham "
                    "WHERE KhoHang.IDSanPham = %s", (int(product_id),)
                )

                # Xóa tất cả các mục cũ trong Treeview
                for item in tree.get_children():
                    tree.delete(item)

                if result:
                    # Thêm dữ liệu vào Treeview
                    for row in result:
                        tree.insert("", tk.END, values=row)
                else:
                    messagebox.showinfo("Thông Báo", "Không có sản phẩm với ID này trong kho.")
            except Exception as e:
                messagebox.showerror("Lỗi", f"Đã xảy ra lỗi khi lấy dữ liệu kho hàng: {e}")

        # Thêm nút để hiển thị kho hàng cho ID sản phẩm
        tk.Button(inventory_window, text="Hiển Thị Kho Hàng", command=show_inventory_for_product).pack()


    def view_grouped_inventory(self):
        inventory_window = tk.Toplevel(self.master)
        inventory_window.title("Kho Hàng (Group By)")

        try:
            # Lấy dữ liệu từ bảng KhoHang và gộp các sản phẩm có cùng ID
            result = self.db.execute_query(
                "SELECT KhoHang.IDSanPham, SanPham.TenSanPham, SUM(KhoHang.SoLuong) AS TongSoLuong "
                "FROM KhoHang JOIN SanPham ON KhoHang.IDSanPham = SanPham.IDSanPham "
                "GROUP BY KhoHang.IDSanPham, SanPham.TenSanPham"
            )

            if result:
                # Tạo Treeview để hiển thị dữ liệu
                tree = ttk.Treeview(inventory_window, columns=("ID", "Tên Sản Phẩm", "Số Lượng"), show="headings")
                tree.heading("ID", text="ID Sản Phẩm")
                tree.heading("Tên Sản Phẩm", text="Tên Sản Phẩm")
                tree.heading("Số Lượng", text="Tổng Số Lượng")

                tree.column("ID", width=100, anchor='center')
                tree.column("Tên Sản Phẩm", width=200, anchor='center')
                tree.column("Số Lượng", width=100, anchor='center')

                tree.pack(fill=tk.BOTH, expand=True)

                # Thêm dữ liệu vào Treeview
                for row in result:
                    tree.insert("", tk.END, values=row)
            else:
                messagebox.showinfo("Thông Báo", "Không có sản phẩm trong kho.")
        except Exception as e:
            messagebox.showerror("Lỗi", f"Đã xảy ra lỗi khi lấy dữ liệu kho hàng: {e}")





    def record_sale(self):
        record_window = tk.Toplevel(self.master)
        record_window.title("Ghi Nhận Bán Hàng")

        tk.Label(record_window, text="Nhập ID sách đã bán:").pack()
        book_id_entry = tk.Entry(record_window)
        book_id_entry.pack()

        tk.Label(record_window, text="Số Lượng:").pack()
        quantity_entry = tk.Entry(record_window)
        quantity_entry.pack()

        tk.Label(record_window, text="Số Điện Thoại Khách Hàng:").pack()
        phone_entry = tk.Entry(record_window)
        phone_entry.pack()

        def submit_record_sale():
            book_id = book_id_entry.get()
            quantity = quantity_entry.get()
            phone = phone_entry.get()

            # Kiểm tra tính hợp lệ của ID sách, số lượng và số điện thoại
            if not book_id.isdigit() or not quantity.isdigit():
                messagebox.showerror("Lỗi", "Vui lòng nhập ID và số lượng hợp lệ.")
                return

            if not phone.isdigit() or len(phone) < 10 or len(phone) > 11:
                messagebox.showerror("Lỗi", "Vui lòng nhập số điện thoại hợp lệ (10 hoặc 11 chữ số).")
                return

            try:
                # Bắt đầu giao dịch
                self.db.execute_query("BEGIN")

                # Lấy số lượng tồn kho hiện tại từ KhoHang
                result = self.db.execute_query("SELECT SoLuong FROM KhoHang WHERE IDSanPham = %s", (int(book_id),))

                if result and result[0][0] >= int(quantity):
                    # Trừ số lượng sản phẩm trong kho
                    self.db.execute_query("UPDATE KhoHang SET SoLuong = SoLuong - %s WHERE IDSanPham = %s", (int(quantity), int(book_id)))

                    # Lấy giá sách từ bảng SanPham để tính tổng tiền
                    price_result = self.db.execute_query("SELECT GiaBan FROM SanPham WHERE IDSanPham = %s", (int(book_id),))
                    if price_result:
                        price = price_result[0][0]
                        total_price = price * int(quantity)

                        # Chèn thông tin vào bảng HoaDon, bao gồm số điện thoại khách hàng
                        self.db.execute_query(
                            "INSERT INTO HoaDon (IDSanPham, SoLuong, NgayBanSP, TongTien, SDT) VALUES (%s, %s, CURRENT_DATE, %s, %s)",
                            (int(book_id), int(quantity), total_price, phone)
                        )

                        # Commit giao dịch khi tất cả các lệnh thành công
                        self.db.execute_query("COMMIT")
                        messagebox.showinfo("Thành Công", "Ghi nhận bán hàng và thêm hóa đơn thành công!")
                    else:
                        raise Exception("Không tìm thấy giá sách trong cơ sở dữ liệu.")
                else:
                    raise Exception("Số lượng trong kho không đủ.")
            
            except Exception as e:
                # Rollback giao dịch nếu có lỗi
                self.db.execute_query("ROLLBACK")
                messagebox.showerror("Lỗi", f"Đã xảy ra lỗi khi ghi nhận bán hàng: {e}")

        tk.Button(record_window, text="Ghi Nhận", command=submit_record_sale).pack()



    def edit_data(self):
        edit_window = tk.Toplevel(self.master)
        edit_window.title("Sửa Thông Tin Sách")

        tk.Label(edit_window, text="Nhập ID Sách:").pack()
        book_id_entry = tk.Entry(edit_window)
        book_id_entry.pack()

        tk.Label(edit_window, text="Tên Sách Mới:").pack()
        book_name_entry = tk.Entry(edit_window)
        book_name_entry.pack()

        tk.Label(edit_window, text="Giá Mới:").pack()
        price_entry = tk.Entry(edit_window)
        price_entry.pack()

        def submit_edit_data():
            book_id = book_id_entry.get()
            new_name = book_name_entry.get()
            new_price = price_entry.get()

            if not book_id.isdigit() or not new_price.isdigit():
                messagebox.showerror("Lỗi", "Vui lòng nhập thông tin hợp lệ.")
                return

            try:
                # Cập nhật thông tin sách dựa trên IDSanPham
                self.db.execute_query(
                    "UPDATE SanPham SET TenSanPham = %s, GiaBan = %s WHERE IDSanPham = %s",
                    (new_name, int(new_price), int(book_id))  # Điều kiện WHERE đã được thêm
                )
                messagebox.showinfo("Thành Công", "Sửa thông tin sách thành công!")
                edit_window.destroy()
            except Exception as e:
                messagebox.showerror("Lỗi", f"Đã xảy ra lỗi khi sửa thông tin sách: {e}")

        tk.Button(edit_window, text="Sửa", command=submit_edit_data).pack()


    def delete_data(self):
        delete_window = tk.Toplevel(self.master)
        delete_window.title("Xóa Sách")

        tk.Label(delete_window, text="Nhập ID Sách cần xóa:").pack()
        book_id_entry = tk.Entry(delete_window)
        book_id_entry.pack()

        def submit_delete_data():
            book_id = book_id_entry.get()

            if not book_id.isdigit():
                messagebox.showerror("Lỗi", "Vui lòng nhập ID hợp lệ.")
                return

            try:
                # Kiểm tra xem sách có tồn tại không
                result = self.db.execute_query("SELECT * FROM SanPham WHERE IDSanPham = %s", (int(book_id),))
                if result:
                    # Nếu sách tồn tại, tiến hành xóa
                    self.db.execute_query("DELETE FROM SanPham WHERE IDSanPham = %s", (int(book_id),))
                    messagebox.showinfo("Thành Công", "Xóa sách thành công!")
                    delete_window.destroy()
                else:
                    messagebox.showerror("Lỗi", "Sách không tồn tại.")
            except Exception as e:
                messagebox.showerror("Lỗi", f"Đã xảy ra lỗi khi xóa sách: {e}")

        tk.Button(delete_window, text="Xóa", command=submit_delete_data).pack()

    def logout(self):
        if self.employee_frame:  # Kiểm tra xem employee_frame có tồn tại không
            self.employee_frame.pack_forget()  # Ẩn khung điều khiển của nhanvien
        self.login_frame.pack()  # Hiển thị lại khung đăng nhập
    
