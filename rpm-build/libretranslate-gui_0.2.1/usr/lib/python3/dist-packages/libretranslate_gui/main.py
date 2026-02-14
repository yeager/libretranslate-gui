#!/usr/bin/env python3
"""LibreTranslate Assistant – main entry point."""

import sys
import gi
gi.require_version("Gtk", "4.0")
gi.require_version("Adw", "1")
from gi.repository import Adw, Gio

from libretranslate_gui.window import LibreTranslateWindow

class LibreTranslateApp(Adw.Application):
    def __init__(self):
        super().__init__(
            application_id="se.danielnylander.LibreTranslateAssistant",
            flags=Gio.ApplicationFlags.DEFAULT_FLAGS,
        )

    def do_activate(self):
        win = self.props.active_window
        if not win:
            win = LibreTranslateWindow(application=self)
        win.present()

def main():
    app = LibreTranslateApp()
    return app.run(sys.argv)

if __name__ == "__main__":
    sys.exit(main())
