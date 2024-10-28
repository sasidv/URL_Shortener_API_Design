import mysql.connector
from mysql.connector import pooling
from datetime import datetime

class Database:
    def __init__(self):
        # Set up the connection pool
        self.pool = pooling.MySQLConnectionPool(
            pool_name="mypool",
            pool_size=5,  # Set the number of connections in the pool
            host='localhost',
            user='root',
            password='shashi@123',
            database='test'  # Adjust to your actual database name
        )
        self.create_table()
    def create_table(self):
        connection = self.pool.get_connection()
        cursor = connection.cursor()
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS urls (
                short_url VARCHAR(6) PRIMARY KEY,
                long_url TEXT NOT NULL,
                expiration_time DATETIME NOT NULL
            )
        ''')
        connection.commit()
        cursor.close()
        connection.close()

    def insert_url(self, short_url, long_url, expiration_time):
        print(short_url, long_url, expiration_time)
        connection = self.pool.get_connection()
        cursor = connection.cursor()
        try:
            cursor.execute('''
                INSERT INTO urls (short_url, long_url, expiration_time) VALUES (%s, %s, %s)
            ''', (short_url, long_url, expiration_time.strftime('%Y-%m-%d %H:%M:%S')))
            connection.commit()
        except mysql.connector.Error as e:
            print("Error inserting into database:", e)
            connection.rollback()
        finally:
            cursor.close()
            connection.close()

    def get_url(self, short_url):
        connection = self.pool.get_connection()
        cursor = connection.cursor()
        cursor.execute('''
            SELECT long_url, expiration_time FROM urls WHERE short_url = %s
        ''', (short_url,))
        result = cursor.fetchone()
        cursor.close()
        connection.close()
        if result:
            long_url, expiration_time = result
            return long_url, expiration_time
        return result

    def url_exists(self, short_url: str) -> bool:
        connection = self.pool.get_connection()
        cursor = connection.cursor()
        try:
            cursor.execute('''
                SELECT 1 FROM urls WHERE short_url = %s
            ''', (short_url,))
            return cursor.fetchone() is not None  # Returns True if found, False otherwise
        except mysql.connector.Error as e:
            print("Error checking existence of URL:", e)
            return False
        finally:
            cursor.close()
            connection.close()
