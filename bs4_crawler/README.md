# BS4 GitHub Repository Crawler

A high-performance web crawler for extracting GitHub repository data from gitstar-ranking.com using BeautifulSoup4, with support for parallel processing and caching.

## Architecture Overview

The crawler follows a multi-stage pipeline architecture with caching and parallel processing:

```ascii
                                     ┌──────────────┐
                                     │   Config     │
                                     │  (settings)  │
                                     └──────┬───────┘
                                           │
                                           ▼
┌──────────────┐    ┌──────────────┐    ┌──────────────┐
│  PageFinder  │◄───│ CacheManager │◄───│ GitHubCrawler│
│(find & cache)│    │(handle cache)│    │   (main)     │
└──────┬───────┘    └──────────────┘    └──────┬───────┘
       │                                        │
       ▼                                       ▼
┌──────────────┐                        ┌──────────────┐
│ HTML Content │                        │ Worker Pool  │
│   Cache      │                        │(process data)│
└──────────────┘                        └──────┬───────┘
                                              │
                                              ▼
                                     ┌──────────────┐
                                     │ RepoParser   │
                                     │(parse HTML)  │
                                     └──────┬───────┘
                                           │
                                           ▼
                                     ┌──────────────┐
                                     │ JSON & CSV   │
                                     │   Output     │
                                     └──────────────┘
```

## Workflow Steps

1. **Initialization & Configuration**

   ```ascii
   ┌─────────────┐
   │ Start       │
   └─────┬───────┘
         ▼
   ┌─────────────┐     ┌─────────────┐
   │ Load Config │────►│ Setup Cache │
   └─────────────┘     └─────────────┘
   ```

2. **Page Discovery & Caching**

   ```ascii
   ┌─────────────┐     ┌─────────────┐     ┌─────────────┐
   │Find Required│     │Cache HTML    │     │Verify Cache │
   │   Pages     │────►│  Content    │────►│  Content    │
   └─────────────┘     └─────────────┘     └─────────────┘
   ```

3. **Parallel Processing**

   ```ascii
   ┌─────────────┐     ┌─────────────┐
   │ Split Pages │     │Worker Pool  │
   │Among Workers│────►│(4 Workers)  │
   └─────────────┘     └──────┬──────┘
                              │
                        ┌─────┴──────┐
                        ▼     ▼      ▼
                     Worker Worker Worker
                        1     2      3
   ```

4. **Data Extraction & Storage**

   ```ascii
   ┌─────────────┐     ┌─────────────┐     ┌─────────────┐
   │Parse Repo   │     │Merge Worker │     │Save to JSON │
   │   Data      │────►│  Results    │────►│   & CSV     │
   └─────────────┘     └─────────────┘     └─────────────┘
   ```

5. **Cleanup**
   ```ascii
   ┌─────────────┐     ┌─────────────┐
   │Save Results │     │Clean Cache  │
   │to Files     │────►│& Temp Data  │
   └─────────────┘     └─────────────┘
   ```

## Components

### 1. GitHubCrawler (crawler.py)

- Main orchestrator class
- Manages the overall crawling process
- Coordinates workers and data aggregation
- Handles final cleanup

### 2. PageFinder (page_finder.py)

- Discovers repository pages
- Handles page fetching and caching
- Uses retry mechanism for reliability

### 3. CacheManager (cache_manager.py)

- Manages temporary HTML content caching
- Implements TTL-based caching
- Reduces network requests
- Auto-cleanup after crawling

### 4. RepoParser (repo_parser.py)

- Parses HTML content
- Extracts repository information
- Handles various HTML structures

### 5. Configuration (config.py)

- Centralizes crawler settings
- Configures workers and paths
- Sets cache TTL and limits

## Features

- **Parallel Processing**: Uses Python's multiprocessing for parallel page processing
- **Smart Caching**: TTL-based temporary caching of HTML content with auto-cleanup
- **Robust Parsing**: Multiple strategies for data extraction
- **Error Handling**: Comprehensive retry and error recovery
- **Progress Tracking**: Real-time progress monitoring
- **Multiple Outputs**: Both JSON and CSV output formats
- **Clean Operation**: Automatic cleanup of temporary files after completion

## Performance Optimizations

1. **Caching Strategy**

   ```ascii
   Request ──► Check Cache ──┬─► Cache Hit ──► Return Content
                            │
                            └─► Cache Miss ──► Fetch & Cache
                                                   │
                                                   ▼
                                            Auto-cleanup when done
   ```

2. **Worker Distribution**
   ```ascii
   Pages: [1..N] ──► Split ──┬─► Worker 1: [1..N/4]
                             ├─► Worker 2: [N/4+1..N/2]
                             ├─► Worker 3: [N/2+1..3N/4]
                             └─► Worker 4: [3N/4+1..N]
   ```

## Error Handling

- Retries for network failures
- Graceful degradation for parsing errors
- Comprehensive logging
- Cache invalidation for stale data
- Cleanup on both success and failure

## Output Format

```json
{
  "rank": 1,
  "name": "owner/repo",
  "stars": 50000,
  "description": "Repository description",
  "language": "Python",
  "avatar_url": "https://...",
  "repo_url": "https://..."
}
```

## Usage

```bash
# Run the crawler
python run_bs4.py

# Output files will be in:
# - bs4_crawler/output/github_repos.json
# - bs4_crawler/output/github_repos.csv

# Note: Temporary cache files are automatically cleaned up after crawling
```
