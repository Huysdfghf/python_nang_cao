from math import sqrt
from tkinter import messagebox as msg

class Giai_Phuong_Trinh:
    def __init__(self, a, b, c=0):
        self.a = a
        self.b = b
        self.c = c

    # Giải phương trình bậc 1
    def giai_phuong_trinh_bac_1(self):
        if self.a == 0:
            if self.b == 0:
                return "Phương trình có vô số nghiệm"
            else:
                return "Phương trình vô nghiệm"
        else:
            nghiem = -self.b / self.a
            return f"Nghiệm x = {round(nghiem, 2)}"  


    # Giải phương trình bậc 2
    def giai_phuong_trinh_bac_2(self):
        try:
            delta = self.b**2 - 4*self.a*self.c
            if delta < 0:
                return "Phương trình vô nghiệm"
            elif delta == 0:
                x = -self.b / (2*self.a)
                return f"Nghiệm kép: x = {x:.2f}"  
            else:
                x1 = (-self.b + sqrt(delta)) / (2*self.a)
                x2 = (-self.b - sqrt(delta)) / (2*self.a)
                return f"Nghiệm x1 = {x1:.2f}, x2 = {x2:.2f}"  
        except ZeroDivisionError:
            return "Hệ số a không thể bằng 0. Vui lòng nhập lại."
        except Exception as e:
            return f"Lỗi: {str(e)}. Vui lòng nhập lại."


class KT_SNT:
    def __init__(self, n):
        self.n = n  

    # Kiểm tra số nguyên tố
    def kiem_tra_so_nguyen_to(self):
        if self.n <= 1:
            return False  
        for i in range(2, int(self.n**0.5) + 1):
            if self.n % i == 0:
                return False  
        return True 

        
    