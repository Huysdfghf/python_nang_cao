# main.py
import tkinter as tk
from bookapp import BookStoreApp

if __name__ == "__main__":
    root = tk.Tk()
    root.geometry("800x600")
    app = BookStoreApp(root)
    root.mainloop()
