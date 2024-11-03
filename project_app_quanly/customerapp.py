import tkinter as tk
from tkinter import messagebox
from tkinter import ttk
from database import Database

class CustomerApp():
    def __init__(self, master, login_frame, password):
        self.master = master
        self.db = Database("demodb", "postgres", "200418", "127.0.0.1", "5432")
        self.login_frame = login_frame  # Lưu lại login_frame được truyền từ BookStoreApp
        self.password = password  # Lưu mật khẩu được truyền vào
        self.create_customer_dashboard()

    def create_customer_dashboard(self):
        self.customer_frame = tk.Frame(self.master)  # Tạo khung khách hàng và lưu tham chiếu
        self.customer_frame.pack()

        tk.Label(self.customer_frame, text="Chào Mừng đến với Bảng Điều Khiển Khách Hàng").pack()
        tk.Button(self.customer_frame, text="Xem Sách Đã Mua", command=self.view_purchases).pack()
        tk.Button(self.customer_frame, text="Đăng Xuất", command=self.logout).pack()  # Gọi logout mà không cần tham số

    def view_purchases(self):
        # Xem sách đã mua dành cho khách hàng
        purchases_window = tk.Toplevel(self.master)
        purchases_window.title("Sách Đã Mua")

        # Sử dụng password đã được lưu
        try:
            result = self.db.execute_query(
                "SELECT SanPham.TenSanPham, HoaDon.SoLuong, HoaDon.TongTien, HoaDon.NgayBanSP "
                "FROM HoaDon "
                "JOIN SanPham ON HoaDon.IDSanPham = SanPham.IDSanPham "
                "JOIN KhachHang ON HoaDon.SDT = KhachHang.SDT "
                "WHERE KhachHang.SDT = %s", (self.password,)  # Sử dụng self.password
            )

            if result:
                tree = ttk.Treeview(purchases_window, columns=("Tên Sản Phẩm", "Số Lượng", "Tổng Tiền", "Ngày Mua"), show="headings")
                tree.heading("Tên Sản Phẩm", text="Tên Sản Phẩm")
                tree.heading("Số Lượng", text="Số Lượng")
                tree.heading("Tổng Tiền", text="Tổng Tiền")
                tree.heading("Ngày Mua", text="Ngày Mua")

                tree.pack(fill=tk.BOTH, expand=True)

                for row in result:
                    tree.insert("", tk.END, values=row)
            else:
                messagebox.showinfo("Thông Báo", "Bạn chưa mua bất kỳ sách nào.")
        except Exception as e:
            messagebox.showerror("Lỗi", f"Đã xảy ra lỗi khi lấy thông tin sách đã mua: {e}")

    def logout(self):
        if self.customer_frame:  # Kiểm tra xem customer_frame có tồn tại không
            self.customer_frame.pack_forget()  # Ẩn khung điều khiển của khách hàng
        self.login_frame.pack()  # Hiển thị lại khung đăng nhập
