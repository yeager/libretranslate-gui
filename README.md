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

This app is translated via Transifex. Help translate it into your language!

**[→ Translate on Transifex](https://app.transifex.com/danielnylander/libretranslate-gui/)**

Currently supported: Swedish (sv). More languages welcome!

### For Translators
1. Create a free account at [Transifex](https://www.transifex.com)
2. Join the [danielnylander](https://app.transifex.com/danielnylander/) organization
3. Start translating!

Translations are automatically synced via GitHub Actions.
## License

GPL-3.0-or-later — Daniel Nylander <daniel@danielnylander.se>
