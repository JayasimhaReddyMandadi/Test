import mysql.connector
from mysql.connector import Error

def create_database():
    try:
        # Connect to MySQL server (without specifying database)
        connection = mysql.connector.connect(
            host='localhost',
            user='root',
            password='123456'
        )
        
        if connection.is_connected():
            cursor = connection.cursor()
            
            # Create database
            cursor.execute("CREATE DATABASE IF NOT EXISTS expense_tracker")
            print("Database 'expense_tracker' created successfully!")
            
            # Grant privileges
            cursor.execute("GRANT ALL PRIVILEGES ON expense_tracker.* TO 'root'@'localhost'")
            cursor.execute("FLUSH PRIVILEGES")
            print("Privileges granted successfully!")
            
    except Error as e:
        print(f"Error while connecting to MySQL: {e}")
        return False
    
    finally:
        if connection.is_connected():
            cursor.close()
            connection.close()
            print("MySQL connection is closed")
    
    return True

if __name__ == "__main__":
    print("Creating MySQL database for Expense Tracker...")
    if create_database():
        print("\nDatabase setup completed! You can now run: python manage.py migrate")
    else:
        print("\nDatabase setup failed. Please check your MySQL installation and credentials.")