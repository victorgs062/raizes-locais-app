import pymysql

def update_db():
    try:
        connection = pymysql.connect(
            host='localhost',
            user='root',
            password='',
            database='raizes_locais'
        )
        with connection.cursor() as cursor:
            # Check if column exists
            cursor.execute("SHOW COLUMNS FROM users LIKE 'address'")
            if not cursor.fetchone():
                cursor.execute("ALTER TABLE users ADD COLUMN address VARCHAR(255) NULL")
                connection.commit()
                print("Column 'address' added successfully.")
            else:
                print("Column 'address' already exists.")
    except Exception as e:
        print(f"Error updating database: {e}")
    finally:
        if 'connection' in locals() and connection.open:
            connection.close()

if __name__ == '__main__':
    update_db()
