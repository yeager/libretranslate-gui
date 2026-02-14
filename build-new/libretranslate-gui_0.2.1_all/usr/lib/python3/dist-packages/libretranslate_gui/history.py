"""Translation history manager."""

import json
import os
from pathlib import Path

MAX_HISTORY = 100


def _history_path():
    d = Path(os.environ.get("XDG_DATA_HOME", Path.home() / ".local/share")) / "libretranslate-gui"
    d.mkdir(parents=True, exist_ok=True)
    return d / "history.json"


def load_history():
    p = _history_path()
    if p.exists():
        try:
            return json.loads(p.read_text("utf-8"))
        except Exception:
            return []
    return []


def save_entry(source_lang, target_lang, source_text, translated_text):
    history = load_history()
    history.insert(0, {
        "source_lang": source_lang,
        "target_lang": target_lang,
        "source": source_text,
        "translation": translated_text,
    })
    history = history[:MAX_HISTORY]
    _history_path().write_text(json.dumps(history, ensure_ascii=False, indent=2), "utf-8")


def clear_history():
    p = _history_path()
    if p.exists():
        p.unlink()
