import json
import time
from pathlib import Path
from typing import Dict, Optional
import os

class CacheManager:
    def __init__(self, cache_file: Path, ttl: int = 3600):
        """Initialize cache manager
        
        Args:
            cache_file (Path): Path to cache file
            ttl (int, optional): Cache TTL in seconds. Defaults to 3600 (1 hour).
        """
        self.cache_file = cache_file
        self.ttl = ttl
        self.cache: Dict[str, dict] = {}
        self._load_cache()
    
    def _load_cache(self):
        """Load cache from file if it exists"""
        if self.cache_file.exists():
            try:
                with open(self.cache_file, 'r', encoding='utf-8') as f:
                    self.cache = json.load(f)
            except json.JSONDecodeError:
                self.cache = {}
    
    def _save_cache(self):
        """Save cache to file"""
        with open(self.cache_file, 'w', encoding='utf-8') as f:
            json.dump(self.cache, f, ensure_ascii=False, indent=2)
    
    def get(self, key: str) -> Optional[str]:
        """Get value from cache if not expired
        
        Args:
            key (str): Cache key (usually URL)
            
        Returns:
            Optional[str]: Cached HTML content if exists and not expired, None otherwise
        """
        if key in self.cache:
            entry = self.cache[key]
            if time.time() - entry['timestamp'] < self.ttl:
                return entry['content']
            else:
                del self.cache[key]
                self._save_cache()
        return None
    
    def set(self, key: str, content: str):
        """Set value in cache with current timestamp
        
        Args:
            key (str): Cache key (usually URL)
            content (str): HTML content to cache
        """
        self.cache[key] = {
            'content': content,
            'timestamp': time.time()
        }
        self._save_cache()
    
    def clear(self):
        """Clear all cache entries"""
        self.cache = {}
        self._save_cache()
    
    def remove_expired(self):
        """Remove all expired entries from cache"""
        current_time = time.time()
        expired_keys = [
            key for key, entry in self.cache.items()
            if current_time - entry['timestamp'] > self.ttl
        ]
        for key in expired_keys:
            del self.cache[key]
        if expired_keys:
            self._save_cache()
    
    @property
    def size(self) -> int:
        """Get number of entries in cache"""
        return len(self.cache)

    def cleanup(self):
        """Remove the cache file and clear the cache dictionary"""
        try:
            if self.cache_file.exists():
                os.remove(self.cache_file)
            self.cache.clear()
        except Exception as e:
            print(f"Error cleaning up cache: {e}") 