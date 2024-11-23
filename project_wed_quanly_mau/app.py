from flask import Flask, render_template, request, redirect, url_for, flash, session
from bookapp import BookStoreApp
from customerapp import CustomerApp
from employeeapp import EmployeeApp

app = Flask(__name__)
app.secret_key = 'your_secret_key'

bookstore_app = BookStoreApp()

@app.route('/')
def home():
    return redirect(url_for('login'))

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        
        # Kiểm tra nếu mật khẩu không rỗng
        if not password:
            flash("Mật khẩu không được để trống!", "error")
            return redirect(url_for('login'))
        
        # Kiểm tra nếu username hoặc password bị None
        if username is None or password is None:
            flash("Vui lòng nhập đầy đủ thông tin đăng nhập!", "error")
            return redirect(url_for('login'))
        
        # Xử lý đăng nhập với BookStoreApp
        result = bookstore_app.login(username, password)
        
        if "user_type" in result:
            session['user_type'] = result["user_type"]
            session['username'] = result.get("username") if result["user_type"] == "customer" else result.get("employee_id")
            
            if result["user_type"] == "customer":
                return redirect(url_for('customer_dashboard'))
            else:
                return redirect(url_for('employee_dashboard'))
        else:
            flash(result.get("error", "Đăng nhập không thành công!"), "error")
            return redirect(url_for('login'))
    
    return render_template('login.html')



@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        sdt = request.form['sdt']
        
        # Sử dụng phương thức register từ BookStoreApp
        result = bookstore_app.register(username, password,sdt)
        
        if "success" in result:
            flash(result["success"], "success")
            return redirect(url_for('login'))
        else:
            flash(result["error"], "error")
            return redirect(url_for('register'))
    return render_template('register.html')

# Routes cho customer
@app.route('/customer_dashboard')
def customer_dashboard():
    if 'user_type' in session and session['user_type'] == 'customer':
        return render_template('customer_dashboard.html')
    return redirect(url_for('login'))

@app.route('/view_purchases')
def view_purchases():
    if 'user_type' in session and session['user_type'] == 'customer':
        customer_app = CustomerApp(session['username'])
        purchases = customer_app.view_purchases()

        if "error" in purchases:  # Nếu kết quả có lỗi
            flash(purchases["error"], "error")  # Ghi lại thông báo lỗi
            return render_template('view_purchases.html', purchases=None)  # Chuyển đến template với purchases = None

        return render_template('view_purchases.html', purchases=purchases)

    return redirect(url_for('login'))





# Route cho giao diện bảng điều khiển nhân viên
@app.route('/employee_dashboard')
def employee_dashboard():
    if 'user_type' in session and session['user_type'] == 'employee':
        return render_template('employee_dashboard.html')
    return redirect(url_for('login'))

# Route để hiển thị form thêm sách
@app.route('/add_book_form')
def add_book_form():
    return render_template('add_book_form.html')

@app.route('/add_book', methods=['GET', 'POST'])
def add_book():
    if 'user_type' in session and session['user_type'] == 'employee':
        employee_app = EmployeeApp(session['username'])
        
        if request.method == 'POST':
            book_name = request.form['book_name']
            author_id = request.form['author_id']
            price = request.form['price']
            publisher_id = request.form['publisher_id']
            
            # Gọi phương thức add_book và nhận kết quả
            result = employee_app.add_book(book_name, author_id, price, publisher_id)
            
            # Kiểm tra kết quả và flash thông báo
            if "success" in result:
                flash(result["success"], "success")
            else:
                flash(result["error"], "error")
            
            return redirect(url_for('add_book_form'))  # Quay lại form thêm sách nếu có thông báo
            
        return render_template('add_book_form.html')
    return redirect(url_for('login'))

# Route hiển thị form thêm tác giả
@app.route('/add_author_form')
def add_author_form():
    return render_template('add_author_form.html')

# Route xử lý thêm tác giả
@app.route('/add_author', methods=['POST'])
def add_author():
    if session.get('user_type') == 'employee':
        employee_app = EmployeeApp(session['username'])
        
        author_name = request.form['author_name']
        
        result = employee_app.add_author(author_name)
        
        flash(result.get("success") or result.get("error"), "success" if "success" in result else "error")
        return redirect(url_for('add_author_form'))
    
    return redirect(url_for('login'))

# Route hiển thị form thêm nhà xuất bản
@app.route('/add_publisher_form')
def add_publisher_form():
    return render_template('add_publisher_form.html')

# Route xử lý thêm nhà xuất bản
@app.route('/add_publisher', methods=['POST'])
def add_publisher():
    if session.get('user_type') == 'employee':
        employee_app = EmployeeApp(session['username'])
        
        publisher_name = request.form['publisher_name']
        publisher_phone = request.form['publisher_phone']
        
        result = employee_app.add_publisher(publisher_name, publisher_phone)
        
        flash(result.get("success") or result.get("error"), "success" if "success" in result else "error")
        return redirect(url_for('add_publisher_form'))
    
    return redirect(url_for('login'))

# Route để hiển thị form nhập kho
@app.route('/add_to_inventory_form')
def add_to_inventory_form():
    return render_template('add_to_inventory_form.html')

# Route để nhập kho
@app.route('/add_to_inventory', methods=['POST'])
def add_to_inventory():
    if 'user_type' in session and session['user_type'] == 'employee':
        employee_app = EmployeeApp(session['username'])
        book_id = request.form['book_id']
        quantity = request.form['quantity']
        inventory_name = request.form['inventory_name']
        inventory_address = request.form['inventory_address']
        result = employee_app.add_to_inventory(book_id, quantity, inventory_name, inventory_address)
        flash(result.get("success") or result.get("error"), "info" if "success" in result else "error")
        return redirect(url_for('employee_dashboard'))
    return redirect(url_for('login'))

@app.route('/view_inventory')
def view_inventory():
    if 'user_type' in session and session['user_type'] == 'employee':
        employee_app = EmployeeApp(session['username'])
        
        # Lấy giá trị của book_id từ tham số GET
        book_id = request.args.get('book_id')
        
        if book_id and book_id.isdigit():
            # Nếu có book_id và là số, tìm kiếm sản phẩm theo book_id
            inventory = employee_app.view_inventory(int(book_id))
        else:
            # Nếu không có book_id, hiển thị toàn bộ kho hàng
            inventory = employee_app.view_inventory()
        
        # Kiểm tra lỗi và thông báo
        error_message = None
        if "error" in inventory:  # Nếu có lỗi
            error_message = inventory["error"]
        elif not inventory:  # Nếu không có hàng trong kho
            error_message = "Kho hàng hiện không có hàng nào."

        return render_template('view_inventory.html', inventory=inventory, error_message=error_message)
    
    return redirect(url_for('login'))


@app.route('/edit_data_form', methods=['GET'])
def edit_data_form():
    return render_template('edit_data_form.html')  # Gọi file HTML của bạn

@app.route('/edit_data', methods=['POST'])
def edit_data():
    if 'user_type' in session and session['user_type'] == 'employee':
        employee_app = EmployeeApp(session['username'])
        
        book_id = request.form['book_id']
        new_name = request.form['new_name']
        new_price = request.form['new_price']
        
        result = employee_app.edit_data(book_id, new_name, new_price)

        # Flash thông báo kết quả
        if "success" in result:
            flash(result["success"], "success")
        else:
            flash(result["error"], "error")
        
        # Chuyển hướng lại về form sửa thông tin sách
        return redirect(url_for('edit_data_form'))
    
    return redirect(url_for('login'))  # Nếu không phải nhân viên, quay về trang đăng nhập



# Route để hiển thị form xóa sách
@app.route('/delete_data_form')
def delete_data_form():
    return render_template('delete_data_form.html')

@app.route('/delete_data', methods=['POST'])
def delete_data():
    if 'user_type' in session and session['user_type'] == 'employee':
        employee_app = EmployeeApp(session['username'])
        
        book_id = request.form['book_id']
        
        result = employee_app.delete_data(book_id)

        # Flash thông báo kết quả
        if "success" in result:
            flash(result["success"], "success")
        else:
            flash(result["error"], "error")
        
        return redirect(url_for('delete_data_form'))  # Quay lại form xóa sách
    
    return redirect(url_for('login'))  # Nếu không phải nhân viên, quay về trang đăng nhập




# Route để hiển thị form ghi nhận bán hàng
@app.route('/record_sale_form')
def record_sale_form():
    return render_template('record_sale_form.html')  # Đổi tên tệp HTML nếu cần


@app.route('/record_sale', methods=['POST'])
def record_sale():
    if 'user_type' in session and session['user_type'] == 'employee':
        employee_app = EmployeeApp(session['username'])
        
        book_id = request.form.get('book_id')
        quantity = request.form.get('quantity')
        phone = request.form.get('phone')
        
        # Kiểm tra xem các trường đã được cung cấp đầy đủ chưa
        if not book_id or not quantity or not phone:
            flash("Vui lòng nhập đầy đủ thông tin.", "error")
            return redirect(url_for('record_sale_form'))  # Quay về form ghi nhận bán hàng
        
        result = employee_app.record_sale(book_id, quantity, phone)

        # Kiểm tra kết quả và flash thông báo
        if "success" in result:
            flash(result["success"], "success")
        else:
            flash(result["error"], "error")

        return redirect(url_for('record_sale_form'))  # Quay về form ghi nhận bán hàng
    
    return redirect(url_for('login'))  # Nếu không phải nhân viên, quay về trang đăng nhập



@app.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('login'))

if __name__ == '__main__':
    app.run(debug=True)
