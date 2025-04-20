# run_spider.py

import os
import sys
import time
from scrapy.crawler import CrawlerProcess
from scrapy.utils.project import get_project_settings
from gitstar_ranking.spiders.github_repos import GitHubReposSpider
from sqlalchemy import create_engine
import pymysql

def ensure_directory(path):
    """Create directory if it doesn't exist and ensure it's writable"""
    if not os.path.exists(path):
        os.makedirs(path)
    elif not os.access(path, os.W_OK):
        os.chmod(path, 0o755)  # Make directory writable

def create_database_if_not_exists(db_url, db_name):
    """Tạo DB nếu chưa tồn tại (MySQL only)"""
    connection = pymysql.connect(
        host='localhost',
        user='root',
        password='abcde12345-',  # <-- sửa lại nếu cần
        port=3306
    )
    cursor = connection.cursor()
    cursor.execute(f"CREATE DATABASE IF NOT EXISTS `{db_name}` DEFAULT CHARACTER SET utf8mb4;")
    print(f"✅ Đảm bảo database `{db_name}` đã tồn tại.")
    cursor.close()
    connection.close()

def main():
    print("🚀 Starting GitStar Ranking crawler...")

    # --- PATH setup ---
    base_dir = os.path.dirname(os.path.abspath(__file__))
    output_dir = os.path.join(base_dir, 'output')
    logs_dir = os.path.join(base_dir, 'logs')

    ensure_directory(output_dir)
    ensure_directory(logs_dir)

    # --- Timestamp for log/output ---
    timestamp = time.strftime('%Y%m%d_%H%M%S')

    # --- MySQL config ---
    mysql_user = 'root'
    mysql_password = 'abcde12345-'   # 👉 Sửa lại theo máy bạn
    mysql_host = 'localhost'
    mysql_port = 3306
    mysql_db = 'github_data'
    mysql_url = f'mysql+pymysql://{mysql_user}:{mysql_password}@{mysql_host}:{mysql_port}/{mysql_db}'

    # Tạo database nếu chưa có
    create_database_if_not_exists(mysql_url, mysql_db)

    # --- Load settings ---
    settings = get_project_settings()
    settings.set('LOG_FILE', os.path.join(logs_dir, f'gitstar_crawler_{timestamp}.log'))
    settings.set('LOG_LEVEL', 'DEBUG')

    # Enable saving to DB
    settings.set('MYSQL_DATABASE_URL', mysql_url)
    settings.set('ITEM_PIPELINES', {
        'gitstar_ranking.pipelines.MySQLStorePipeline': 300,
    })

    # Optional: Also save to JSON or CSV
    # save_to_file = False
    # if save_to_file:
    #     settings.set('FEEDS', {
    #         os.path.join(output_dir, f'github_repos_{timestamp}.json'): {
    #             'format': 'json',
    #             'encoding': 'utf8',
    #             'overwrite': True
    #         }
    #     })

    try:
        # Run spider
        process = CrawlerProcess(settings)
        process.crawl(GitHubReposSpider)
        process.start()

        print("✅ Crawler finished successfully and data saved to MySQL.")

    except Exception as e:
        print(f"❌ Error running crawler: {e}")
        sys.exit(1)

    sys.exit(0)

if __name__ == "__main__":
    main()
