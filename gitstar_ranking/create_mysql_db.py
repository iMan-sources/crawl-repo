# create_mysql_db.py

import pymysql
from pymysql.err import OperationalError


def create_database_if_not_exists(
        host='localhost',
        port=3306,
        user='root',
        password='abcde12345-',
        database_name='github_data'
):
    try:
        # Kết nối đến MySQL server (chưa chỉ định database)
        connection = pymysql.connect(
            host=host,
            user=user,
            password=password,
            port=port
        )
        cursor = connection.cursor()

        # Tạo database nếu chưa có
        cursor.execute(f"CREATE DATABASE IF NOT EXISTS `{database_name}` DEFAULT CHARACTER SET utf8mb4;")
        print(f"✅ Database `{database_name}` is exists")

        cursor.close()
        connection.close()
    except OperationalError as e:
        print(f"❌ Lỗi kết nối MySQL: {e}")


if __name__ == "__main__":
    create_database_if_not_exists(
        host='localhost',
        port=3306,
        user='root',
        password='abcde12345-',  # 👉 đổi chỗ này
        database_name='github_data'  # 👉 và chỗ này nếu muốn
    )
