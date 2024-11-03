import tkinter as tk
from tkinter import ttk
from tkinter import Menu
from tkinter import messagebox as msg

from code_pt import *

# Tạo giao diện chính
win = tk.Tk()
win.title('Giải Phương Trình')

# khóa điều chỉnh GUI
win.resizable(False, False)

# Tạo menu bar
menu_bar = Menu(win)
win.config(menu=menu_bar)

def clear_entries():
    # Reset các ô nhập hệ số a, b, c và kết quả phương trình
    a.set(0)
    b.set(0)
    c.set(0)
    kq.set("")

    # Reset ô nhập số kiểm tra nguyên tố và kết quả kiểm tra
    snt_input.set(0)
    result_output.set("")

# Tạo menu File và Help
file_menu = Menu(menu_bar, tearoff=0)
menu_bar.add_cascade(label="File", menu=file_menu)
file_menu.add_command(label="Exit", command=win.quit)
file_menu.add_command(label="New", command=clear_entries)

def _msgBox():
    msg.showinfo('Python Message Info Box', 'Chương trình tính các phương trình và kiểm tra số nguyên tố \n')

help_menu = Menu(menu_bar, tearoff=0)  
menu_bar.add_cascade(label="Help", menu=help_menu)  
help_menu.add_command(label="About", command=_msgBox)

# Tạo tab
tabControl = ttk.Notebook(win)
Pg1 = ttk.Frame(tabControl)
tabControl.add(Pg1, text="Phương trình")
tabControl.pack(expand=1, fill="both")

Pg2 = ttk.Frame(tabControl)
tabControl.add(Pg2, text="Số Nguyên Tố")
tabControl.pack(expand=2, fill="both")

# Giải Phương Trình
# Tạo Frame cho hệ số
mighty = ttk.LabelFrame(Pg1, text='Các hệ số: ')
mighty.grid(column=0, row=0, padx=8, pady=4)

# Ô nhập liệu cho hệ số a
a_label = ttk.Label(mighty, text="a:")
a_label.grid(column=0, row=0, sticky='W')

a = tk.IntVar()
a_entry = ttk.Entry(mighty, width=10, textvariable=a)
a_entry.grid(column=0, row=1, padx=5, pady=5, sticky='W')  
# Ô nhập liệu cho hệ số b
b_label = ttk.Label(mighty, text="b:")
b_label.grid(column=1, row=0, sticky='W')

b = tk.IntVar()
b_entry = ttk.Entry(mighty, width=10, textvariable=b)
b_entry.grid(column=1, row=1, padx=5, pady=5, sticky='W')  

# Ô nhập liệu cho hệ số c
c_label = ttk.Label(mighty, text="c:")
c_label.grid(column=2, row=0, sticky='W')

c = tk.IntVar()
c_entry = ttk.Entry(mighty, width=10, textvariable=c)
c_entry.grid(column=2, row=1, padx=5, pady=5, sticky='W')  

# Tạo Frame cho kết quả
Ketqua = ttk.LabelFrame(Pg1, text='Giải')
Ketqua.grid(column=0, row=1, columnspan=3, padx=8, pady=4, sticky='EW')  

# Nhãn "Kết quả:"
ketqua_lb = ttk.Label(Ketqua, text="Kết quả:")
ketqua_lb.grid(column=0, row=0, sticky='W')

# Ô nhập liệu hiển thị kết quả
kq = tk.StringVar()
kq_en = ttk.Entry(Ketqua, width=40, textvariable=kq, state='readonly')
kq_en.grid(column=1, row=0, columnspan=2, padx=10, pady=5, sticky='EW')  

# Tạo Frame cho danh sách chọn phương trình
Tinh = ttk.LabelFrame(Pg1, text='Phương Trình')
Tinh.grid(column=1, row=0, padx=8, pady=4)

# Hàm kiểm tra input
def Input():
    try:
        a_value = a.get()
        b_value = b.get()
        c_value = c.get()
        return a_value, b_value, c_value
    except tk.TclError:
        msg.showerror("Lỗi", "Vui lòng nhập vào các số hợp lệ.")
        return None, None, None

# Hàm giải phương trình bậc 1
def PTB1():
    a_value, b_value, _ = Input()  
    if a_value is not None and b_value is not None:
        pt = Giai_Phuong_Trinh(a_value, b_value)
        result = pt.giai_phuong_trinh_bac_1()
        kq.set(str(result))

# Hàm giải phương trình bậc 2
def PTB2():
    a_value, b_value, c_value = Input()
    if a_value is not None and b_value is not None and c_value is not None:
        pt = Giai_Phuong_Trinh(a_value, b_value, c_value)
        result = pt.giai_phuong_trinh_bac_2()
        kq.set(str(result))

# Hàm xử lý lựa chọn từ Listbox
def handle_selection(event):
    selected_option = listbox.get(listbox.curselection())
    if selected_option == "Bậc 1":
        PTB1()
    elif selected_option == "Bậc 2":
        PTB2()

# Tạo Listbox để chọn phương trình
listbox = tk.Listbox(Tinh, height=2)
listbox.insert(1, "Bậc 1")
listbox.insert(2, "Bậc 2")
listbox.grid(column=0, row=0, padx=5, pady=10)
listbox.bind("<<ListboxSelect>>", handle_selection)

# Kiểm tra số nguyên tố
# Tạo Frame cho kiểm tra số nguyên tố
mighty2 = ttk.LabelFrame(Pg2, text='Kiểm tra số nguyên tố: ')
mighty2.grid(column=0, row=0, padx=8, pady=4)

# Ô nhập liệu cho số nguyên tố
snt_label = ttk.Label(mighty2, text="Số:")
snt_label.grid(column=0, row=0, sticky='W')

snt_input = tk.IntVar()
snt_entry = ttk.Entry(mighty2, width=10, textvariable=snt_input)
snt_entry.grid(column=0, row=1, padx=5, pady=5, sticky='W')

# Nhãn kết quả cho kiểm tra số nguyên tố
result_label = ttk.Label(mighty2, text="Kết quả:")
result_label.grid(column=1, row=0, sticky='W')

result_output = tk.StringVar()
result_entry = ttk.Entry(mighty2, width=35, textvariable=result_output, state='readonly')
result_entry.grid(column=1, row=1, padx=10, pady=5, sticky='W')

def kiem_tra_snt():
    try:
        number = snt_input.get()
        kt_snt = KT_SNT(number)  
        if kt_snt.kiem_tra_so_nguyen_to():
            result_output.set(f"{number} là số nguyên tố.")
        else:
            result_output.set(f"{number} không phải là số nguyên tố.")
    except:
        msg.showerror("Lỗi", "Vui lòng nhập một số nguyên hợp lệ.")

# Nút kiểm tra số nguyên tố
check_prime_btn = ttk.Button(mighty2, text="Kiểm tra", command=kiem_tra_snt)
check_prime_btn.grid(column=0, row=3, padx=5, pady=10)

win.mainloop()
