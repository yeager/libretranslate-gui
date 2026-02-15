#!/usr/bin/env python3
"""LibreTranslate Assistant – main entry point."""

import gettext
import locale
import os
import sys

LOCALE_DIR = os.path.join(os.path.dirname(__file__), "..", "..", "po", "locale")
if not os.path.isdir(LOCALE_DIR):
    LOCALE_DIR = "/usr/share/locale"

try:
    locale.setlocale(locale.LC_ALL, "")
except locale.Error:
    pass

gettext.bindtextdomain("libretranslate-gui", LOCALE_DIR)
gettext.textdomain("libretranslate-gui")

import gi
gi.require_version("Gtk", "4.0")
gi.require_version("Adw", "1")
from gi.repository import Gtk, Adw, Gio

_ = gettext.gettext

from libretranslate_gui.window import LibreTranslateWindow

class LibreTranslateApp(Adw.Application):
    def __init__(self):
        super().__init__(
            application_id="se.danielnylander.LibreTranslateAssistant",
            flags=Gio.ApplicationFlags.DEFAULT_FLAGS,
        )
        about_action = Gio.SimpleAction.new("about", None)
        about_action.connect("activate", self._on_about)
        self.add_action(about_action)

    def do_activate(self):
        win = self.props.active_window
        if not win:
            win = LibreTranslateWindow(application=self)
        win.present()

    def _on_about(self, *_args):
        about = Adw.AboutWindow(
            transient_for=self.props.active_window,
            application_name=_("LibreTranslate Assistant"),
            application_icon="libretranslate-gui",
            version="0.2.2",
            developer_name="Daniel Nylander",
            developers=["Daniel Nylander <daniel@danielnylander.se>"],
            copyright="© 2026 Daniel Nylander",
            license_type=Gtk.License.GPL_3_0,
            website="https://github.com/yeager/libretranslate-gui",
            issue_url="https://github.com/yeager/libretranslate-gui/issues",
            translator_credits="Daniel Nylander <daniel@danielnylander.se>",
            comments=_("Translation assistant powered by LibreTranslate"),
        )
        about.present()

def main():
    app = LibreTranslateApp()
    return app.run(sys.argv)

if __name__ == "__main__":
    sys.exit(main())
