"""LibreTranslate API client."""

import json
import threading
from urllib import request, error, parse

DEFAULT_URL = "https://libretranslate.com"


class LibreTranslateAPI:
    def __init__(self, server_url=None, api_key=None):
        self.server_url = (server_url or DEFAULT_URL).rstrip("/")
        self.api_key = api_key or ""

    def _post(self, endpoint, data):
        url = f"{self.server_url}{endpoint}"
        payload = json.dumps(data).encode("utf-8")
        req = request.Request(url, data=payload, headers={"Content-Type": "application/json"})
        with request.urlopen(req, timeout=30) as resp:
            return json.loads(resp.read().decode("utf-8"))

    def _get(self, endpoint):
        url = f"{self.server_url}{endpoint}"
        req = request.Request(url)
        with request.urlopen(req, timeout=15) as resp:
            return json.loads(resp.read().decode("utf-8"))

    def get_languages(self):
        """Return list of dicts with code/name."""
        return self._get("/languages")

    def translate(self, text, source="en", target="sv"):
        data = {"q": text, "source": source, "target": target, "format": "text"}
        if self.api_key:
            data["api_key"] = self.api_key
        result = self._post("/translate", data)
        return result.get("translatedText", "")

    def translate_async(self, text, source, target, callback):
        """Run translation in background thread, call callback(result, error) on finish."""
        def _worker():
            try:
                result = self.translate(text, source, target)
                callback(result, None)
            except Exception as e:
                callback(None, e)
        t = threading.Thread(target=_worker, daemon=True)
        t.start()

    def get_languages_async(self, callback):
        def _worker():
            try:
                langs = self.get_languages()
                callback(langs, None)
            except Exception as e:
                callback(None, e)
        t = threading.Thread(target=_worker, daemon=True)
        t.start()
