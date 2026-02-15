# LibreTranslate Assistant

A GTK4/Adwaita translation assistant powered by LibreTranslate/Lingva.

![Screenshot](data/screenshots/screenshot-01.png)

## Features

- Live translation — type text and get translations instantly
- Language selector auto-populated from LibreTranslate API
- Batch translation — paste multiple sentences
- PO/TS file support — get translation suggestions for untranslated strings
- Configurable server — use public instance or self-hosted LibreTranslate
- API key support for authenticated instances
- Translation history saved locally
- One-click copy to clipboard

## Installation

### Debian/Ubuntu

```bash
# Add repository
curl -fsSL https://yeager.github.io/debian-repo/KEY.gpg | sudo gpg --dearmor -o /usr/share/keyrings/yeager-archive-keyring.gpg
echo "deb [signed-by=/usr/share/keyrings/yeager-archive-keyring.gpg] https://yeager.github.io/debian-repo stable main" | sudo tee /etc/apt/sources.list.d/yeager.list
sudo apt update
sudo apt install libretranslate-gui
```

### Fedora/RHEL

```bash
sudo dnf config-manager --add-repo https://yeager.github.io/rpm-repo/yeager.repo
sudo dnf install libretranslate-gui
```

### From source

```bash
pip install .
libretranslate-gui
```

## 🌍 Contributing Translations

Help translate this app into your language! All translations are managed via Transifex.

**→ [Translate on Transifex](https://app.transifex.com/danielnylander/libretranslate-gui/)**

### How to contribute:
1. Visit the [Transifex project page](https://app.transifex.com/danielnylander/libretranslate-gui/)
2. Create a free account (or log in)
3. Select your language and start translating

### Currently supported languages:
Arabic, Czech, Danish, German, Spanish, Finnish, French, Italian, Japanese, Korean, Norwegian Bokmål, Dutch, Polish, Brazilian Portuguese, Russian, Swedish, Ukrainian, Chinese (Simplified)

### Notes:
- Please do **not** submit pull requests with .po file changes — they are synced automatically from Transifex
- Source strings are pushed to Transifex daily via GitHub Actions
- Translations are pulled back and included in releases

New language? Open an [issue](https://github.com/yeager/libretranslate-gui/issues) and we'll add it!

## License

GPL-3.0-or-later — Daniel Nylander <daniel@danielnylander.se>
