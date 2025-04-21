# GitHub Repository Crawler

A production-ready Scrapy project for crawling GitHub repository data from GitStar Ranking. This crawler efficiently collects repository information including rank, name, stars, description, and programming language.

## Features

- 🚀 Efficient crawling with Scrapy
- 📊 Data export in both JSON and CSV formats
- 🔄 Automatic retry mechanism with exponential backoff
- 📝 Comprehensive logging
- ⚡ Performance optimized with concurrent requests
- 🛡️ Respects robots.txt and implements polite crawling

## Project Structure

```
github-crawler/
├── gitstar_ranking/          # Main Scrapy project directory
│   ├── spiders/             # Contains crawler spiders
│   ├── items.py            # Data structure definitions
│   ├── pipelines.py        # Data processing and storage
│   ├── middlewares.py      # Custom middleware
│   ├── settings.py         # Project configuration
│   └── run.py              # Runner script
├── output/                  # Output data directory
├── logs/                    # Log files directory
└── requirements.txt         # Project dependencies
```

## Component Details

### Spiders (`spiders/`)

- **Mục đích**: Định nghĩa logic thu thập dữ liệu từ GitStar Ranking
- **Tính năng**:
  - Tự động phân trang và thu thập dữ liệu
  - Xử lý và làm sạch dữ liệu thô
  - Tôn trọng robots.txt và rate limiting
  - Xử lý lỗi và retry tự động

### Items (`items.py`)

- **Mục đích**: Định nghĩa cấu trúc dữ liệu cho repository
- **Tính năng**:
  - Định nghĩa các trường dữ liệu cần thiết
  - Kiểm tra kiểu dữ liệu
  - Dễ dàng mở rộng thêm trường mới

### Pipelines (`pipelines.py`)

- **Mục đích**: Xử lý và lưu trữ dữ liệu đã thu thập
- **Tính năng**:
  - Lưu dữ liệu dưới dạng JSON và CSV
  - Tự động tạo thư mục output
  - Xử lý encoding UTF-8
  - Logging chi tiết quá trình xử lý

### Middlewares (`middlewares.py`)

- **Mục đích**: Xử lý các request và response
- **Tính năng**:
  - Custom retry logic với exponential backoff
  - Xử lý các HTTP error code
  - Thêm delay giữa các request
  - Logging chi tiết các lỗi

### Settings (`settings.py`)

- **Mục đích**: Cấu hình toàn bộ dự án
- **Tính năng**:
  - Cấu hình download delay và concurrent requests
  - Thiết lập retry policy
  - Cấu hình logging
  - Bật/tắt các tính năng như AutoThrottle

### Runner Script (`run.py`)

- **Mục đích**: Script chính để chạy crawler
- **Tính năng**:
  - Khởi tạo môi trường chạy
  - Xử lý các tham số dòng lệnh
  - Logging quá trình chạy
  - Xử lý các exception

## Installation

1. Clone the repository:

```bash
git clone [repository-url]
cd github-crawler
```

2. Create and activate a virtual environment:

```bash
python -m venv .venv
source .venv/bin/activate  # On Windows: .venv\Scripts\activate
```

3. Install dependencies:

```bash
pip install -r requirements.txt
```

## Usage

Run the crawler:

```bash
python run.py
```

The crawler will:

- Start collecting data from GitStar Ranking
- Save results in both JSON and CSV formats in the `output/` directory
- Generate logs in the `logs/` directory

## Output Format

### JSON Output

```json
[
  {
    "rank": 1,
    "name": "owner/repository",
    "stars": 100000,
    "description": "Repository description",
    "language": "Python"
  },
  ...
]
```

### CSV Output

```csv
rank,name,stars,description,language
1,owner/repository,100000,Repository description,Python
...
```

## Configuration

The crawler can be configured through `settings.py`:

- `DOWNLOAD_DELAY`: Delay between requests (default: 1 second)
- `CONCURRENT_REQUESTS`: Number of concurrent requests (default: 8)
- `RETRY_TIMES`: Number of retry attempts (default: 3)
- `AUTOTHROTTLE_ENABLED`: Enable/disable automatic throttling
- `LOG_LEVEL`: Logging level (default: INFO)

## Error Handling

The crawler includes robust error handling:

- Automatic retry with exponential backoff
- Detailed logging of errors and warnings
- Graceful handling of missing data
- Respect for server response codes

## Contributing

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

## License

This project is licensed under the MIT License - see the LICENSE file for details.

## Acknowledgments

- [Scrapy](https://scrapy.org/) - The web crawling framework
- [GitStar Ranking](https://gitstar-ranking.com/) - The data source



## Triển khai với docker-compose

regis + db MySQl

```bash
          docker compose -f ./.docker/docker-compose.yml up -d

          docker compose -f docker-compose.staging.yml up -d
```
