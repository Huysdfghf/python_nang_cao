import tkinter as tk
from tkinter import messagebox
from database import Database
from employeeapp import EmployeeApp  # Import EmployeeApp
from customerapp import CustomerApp  # Import CustomerApp

class BookStoreApp:
    def __init__(self, master):
        self.master = master
        self.db = Database("demodb", "postgres", "200418", "127.0.0.1", "5432")
        
        # Tạo sẵn khung đăng nhập ngay từ đầu và hiển thị
        self.login_frame = self.create_login_frame()  
        self.login_frame.pack()  # Hiển thị khung đăng nhập ngay từ đầu

    def create_login_frame(self):
        frame = tk.Frame(self.master)
        self.master.title("Quản Lý Nhà Sách SKY")
        # Thiết lập menu
        self.menu_bar = tk.Menu(self.master)
        self.master.config(menu=self.menu_bar)

        self.file_menu = tk.Menu(self.menu_bar, tearoff=0)
        self.menu_bar.add_cascade(label="File", menu=self.file_menu)
        self.file_menu.add_command(label="Exit", command=self.close_app)
        tk.Label(frame, text="Đăng Nhập").pack()

        self.username_label = tk.Label(frame, text="Tên Người Dùng:")
        self.username_label.pack()
        self.username_entry = tk.Entry(frame)
        self.username_entry.pack()

        self.password_label = tk.Label(frame, text="Mật Khẩu:")
        self.password_label.pack()
        self.password_entry = tk.Entry(frame, show="*")
        self.password_entry.pack()

        tk.Button(frame, text="Đăng Nhập", command=self.login).pack()
        tk.Button(frame, text="Đăng Ký", command=self.show_registration_frame).pack()
        return frame

    def show_registration_frame(self):
        self.registration_frame = tk.Frame(self.master)
        self.login_frame.pack_forget()  # Ẩn khung đăng nhập
        tk.Label(self.registration_frame, text="Đăng Ký").pack()

        self.username_label = tk.Label(self.registration_frame, text="Tên Người Dùng:")
        self.username_label.pack()
        self.new_username_entry = tk.Entry(self.registration_frame)
        self.new_username_entry.pack()

        self.password_label = tk.Label(self.registration_frame, text="Mật Khẩu:")
        self.password_label.pack()
        self.new_password_entry = tk.Entry(self.registration_frame, show="*")
        self.new_password_entry.pack()

        tk.Button(self.registration_frame, text="Xác Nhận Đăng Ký", command=self.register).pack()
        tk.Button(self.registration_frame, text="Quay Lại Đăng Nhập", command=self.back_to_login).pack()

        self.registration_frame.pack()  # Hiển thị khung đăng ký    


    def back_to_login(self):
        self.registration_frame.pack_forget()  # Ẩn khung đăng ký
        self.login_frame.pack()  # Hiển thị lại khung đăng nhập

    def register(self):
        username = self.new_username_entry.get()
        password = self.new_password_entry.get()

        if not username or not password:
            messagebox.showerror("Lỗi", "Tên đăng nhập và mật khẩu không được để trống.")
            return

        try:
            self.db.execute_query("INSERT INTO KhachHang (TenKhachHang, SDT) VALUES (%s, %s)", (username, password))
            messagebox.showinfo("Thông Báo", "Đăng ký thành công!")
            self.back_to_login()
        except Exception as e:
            messagebox.showerror("Lỗi", f"Đã xảy ra lỗi khi đăng ký: {e}")

    def login(self):
        username = self.username_entry.get()
        password = self.password_entry.get()

        try:
            # Kiểm tra thông tin đăng nhập của khách hàng
            customer = self.db.execute_query(
                "SELECT * FROM KhachHang WHERE TenKhachHang = %s AND SDT = %s",
                (username, password)
            )
            # Kiểm tra thông tin đăng nhập của nhân viên
            employee = self.db.execute_query(
                "SELECT * FROM NhanVien WHERE TenNhanVien = %s AND SDTNhanVien = %s",
                (username, password)
            )

            if customer:
                # Nếu là khách hàng, khởi tạo CustomerApp và truyền mật khẩu cùng login_frame
                self.login_frame.pack_forget()  # Ẩn khung đăng nhập
                CustomerApp(self.master, self.login_frame, password)  # Truyền mật khẩu và login_frame
            elif employee:
                # Nếu là nhân viên, lấy ID nhân viên
                employee_id = employee[0][0]  # Giả sử ID nhân viên là trường đầu tiên trong bảng

                # Khởi tạo EmployeeApp và truyền ID nhân viên cùng login_frame
                self.login_frame.pack_forget()  # Ẩn khung đăng nhập
                EmployeeApp(self.master, self.login_frame, employee_id)  # Truyền ID nhân viên và login_frame
            else:
                # Nếu thông tin đăng nhập không hợp lệ
                messagebox.showerror("Lỗi", "Thông tin đăng nhập không hợp lệ")
        except Exception as e:
            messagebox.showerror("Lỗi", f"Đã xảy ra lỗi khi đăng nhập: {e}")


    def close_app(self):
       self.db.close()  # Đóng kết nối cơ sở dữ liệu
       self.master.destroy()  # Đóng cửa sổ chính của ứng dụng
