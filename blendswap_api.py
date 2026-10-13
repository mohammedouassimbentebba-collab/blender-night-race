"""BlendSwap API Client for searching and downloading 3D models."""
import json
import os
import sys
import ssl
import urllib.request
import urllib.error
import urllib.parse

CONFIG_PATH = os.path.join(os.path.dirname(os.path.abspath(__file__)), "config.json")

def load_config():
    if os.path.exists(CONFIG_PATH):
        with open(CONFIG_PATH, "r", encoding="utf-8") as f:
            return json.load(f)
    return {
        "api_key": "bsk_live_e23eb06f8360e2530d7cc9a4c58faba7",
        "api_base_url": "https://blendswap.com/api/v1"
    }

class BlendSwapClient:
    def __init__(self, api_key=None, base_url=None):
        config = load_config()
        self.api_key = api_key or config.get("api_key")
        self.base_url = base_url or config.get("api_base_url", "https://blendswap.com/api/v1")
        self.headers = {
            "Authorization": f"Bearer {self.api_key}",
            "User-Agent": "BlenderAssistant/1.0",
            "Content-Type": "application/json",
            "Accept": "application/json"
        }
        self.ssl_context = ssl._create_unverified_context()

    def _request(self, method, endpoint, data=None, params=None):
        url = f"{self.base_url}{endpoint}"
        if params:
            query = urllib.parse.urlencode({k: v for k, v in params.items() if v is not None})
            url = f"{url}?{query}"

        body = json.dumps(data).encode("utf-8") if data else None
        req = urllib.request.Request(url, data=body, headers=self.headers, method=method)

        try:
            with urllib.request.urlopen(req, context=self.ssl_context) as resp:
                return json.loads(resp.read().decode("utf-8"))
        except urllib.error.HTTPError as e:
            err_body = e.read().decode("utf-8", errors="replace")
            print(f"HTTP Error {e.code}: {err_body}", file=sys.stderr)
            raise

    def get_me(self):
        """Check current account status and download quota."""
        return self._request("GET", "/me")

    def get_categories(self):
        """Get all asset categories."""
        return self._request("GET", "/categories")

    def search_assets(self, query=None, category=None, tags=None, page=1, per_page=20):
        """Search the BlendSwap 3D asset catalog."""
        params = {
            "q": query,
            "category": category,
            "tags": tags,
            "page": page,
            "per_page": per_page
        }
        return self._request("GET", "/assets", params=params)

    def get_asset(self, asset_id):
        """Get metadata and file details for a single asset."""
        return self._request("GET", f"/assets/{asset_id}")

    def get_download_url(self, asset_id, file_id=None):
        """Generate a temporary download URL for an asset."""
        payload = {"asset_id": asset_id}
        if file_id:
            payload["file_id"] = file_id
        return self._request("POST", "/downloads", data=payload)

    def download_file(self, download_url, destination_path):
        """Download file from temporary URL to local disk."""
        req = urllib.request.Request(download_url, headers={"User-Agent": "BlenderAssistant/1.0"})
        with urllib.request.urlopen(req, context=self.ssl_context) as resp, open(destination_path, "wb") as out_file:
            while chunk := resp.read(64 * 1024):
                out_file.write(chunk)
        return destination_path

if __name__ == "__main__":
    client = BlendSwapClient()
    me = client.get_me()
    print("Logged in as:", me.get("user", {}).get("username"))
    print("Free downloads remaining today:", me.get("api_free_downloads_remaining_today"))
    print("Download credits:", me.get("download_credits"))
