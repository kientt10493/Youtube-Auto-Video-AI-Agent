import os
import requests
from typing import Optional, Dict, Any, List

def _load_local_env():
    env_path = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), ".env")
    if os.path.exists(env_path):
        with open(env_path, "r", encoding="utf-8") as f:
            for line in f:
                line = line.strip()
                if line and not line.startswith("#") and "=" in line:
                    k, v = line.split("=", 1)
                    k, v = k.strip(), v.strip()
                    if k and k not in os.environ:
                        os.environ[k] = v

class MediaDownloader:
    """Công cụ tải ảnh, video B-Roll và âm thanh/nhạc nền từ Internet (Pexels, Pixabay, Internet Archive / Direct URLs)."""

    def __init__(
        self,
        pexels_api_key: Optional[str] = None,
        pixabay_api_key: Optional[str] = None,
        download_dir: str = "./storage/media"
    ):
        _load_local_env()
        self.pexels_api_key = pexels_api_key or os.getenv("PEXELS_API_KEY", "")
        self.pixabay_api_key = pixabay_api_key or os.getenv("PIXABAY_API_KEY", "")
        self.download_dir = download_dir
        os.makedirs(self.download_dir, exist_ok=True)

    def search_and_download_pexels_video(self, query: str, output_path: str, min_duration: int = 4) -> Optional[str]:
        """Tìm và tải stock video từ Pexels API."""
        if not self.pexels_api_key:
            return None
        
        headers = {"Authorization": self.pexels_api_key}
        url = f"https://api.pexels.com/videos/search?query={query}&per_page=5&orientation=landscape"
        try:
            res = requests.get(url, headers=headers, timeout=15)
            if res.status_code == 200:
                data = res.json()
                videos = data.get("videos", [])
                for v in videos:
                    if v.get("duration", 0) >= min_duration:
                        video_files = v.get("video_files", [])
                        # Chọn file có độ phân giải 1080p hoặc 720p
                        for vf in video_files:
                            if vf.get("width") == 1920 or vf.get("quality") == "hd":
                                download_url = vf.get("link")
                                if download_url:
                                    self._download_file(download_url, output_path)
                                    return output_path
            return None
        except Exception as e:
            print(f"[MediaDownloader] Lỗi tìm Pexels Video: {e}")
            return None

    def search_and_download_pixabay_video(self, query: str, output_path: str) -> Optional[str]:
        """Tìm và tải stock video từ Pixabay API."""
        if not self.pixabay_api_key:
            return None
        
        url = f"https://pixabay.com/api/videos/?key={self.pixabay_api_key}&q={query}&video_type=film"
        try:
            res = requests.get(url, timeout=15)
            if res.status_code == 200:
                data = res.json()
                hits = data.get("hits", [])
                if hits:
                    v_hit = hits[0]
                    video_url = v_hit.get("videos", {}).get("large", {}).get("url") or v_hit.get("videos", {}).get("medium", {}).get("url")
                    if video_url:
                        self._download_file(video_url, output_path)
                        return output_path
            return None
        except Exception as e:
            print(f"[MediaDownloader] Lỗi tìm Pixabay Video: {e}")
            return None

    def search_and_download_pexels_image(self, query: str, output_path: str) -> Optional[str]:
        """Tìm và tải ảnh chất lượng cao từ Pexels API."""
        if not self.pexels_api_key:
            return None
        
        headers = {
            "Authorization": self.pexels_api_key,
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36"
        }
        url = f"https://api.pexels.com/v1/search?query={query}&per_page=3&orientation=landscape"
        try:
            res = requests.get(url, headers=headers, timeout=15)
            if res.status_code == 200:
                photos = res.json().get("photos", [])
                if photos:
                    img_url = photos[0].get("src", {}).get("large2x") or photos[0].get("src", {}).get("large")
                    if img_url:
                        self._download_file(img_url, output_path)
                        return output_path
            return None
        except Exception as e:
            print(f"[MediaDownloader] Lỗi tải ảnh Pexels: {e}")
            return None

    def _download_file(self, url: str, target_path: str):
        headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36"}
        res = requests.get(url, headers=headers, stream=True, timeout=30)
        res.raise_for_status()
        with open(target_path, "wb") as f:
            for chunk in res.iter_content(chunk_size=8192):
                if chunk:
                    f.write(chunk)
