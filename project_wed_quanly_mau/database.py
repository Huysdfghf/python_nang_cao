import psycopg2

class Database:
    def __init__(self, dbname, user, password, host, port):
        self.connection = psycopg2.connect(
            database=dbname,
            user=user,
            password=password,
            host=host,
            port=port
        )

    def close(self):
        if self.connection:
            self.connection.close()

    def execute_query(self, query, params=None):
        # Tạo cursor ở đây để đảm bảo luôn có sẵn
        cursor = self.connection.cursor()
        try:
            if params:
                cursor.execute(query, params)
            else:
                cursor.execute(query)

            # Nếu là truy vấn SELECT, trả về kết quả
            if query.strip().upper().startswith("SELECT"):
                return cursor.fetchall()

            # Nếu là truy vấn INSERT, UPDATE, DELETE, commit thay đổi
            self.connection.commit()
            return None
        except Exception as e:
            self.connection.rollback()  # Rollback nếu có lỗi
            print(f"Database query error: {e}")
            return None  # Hoặc ném ra lỗi để xử lý bên ngoài
        finally:
            cursor.close()  # Đóng cursor ở đây
