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
        GLib.set_application_name(_("LibreTranslate Assistant"))
            flags=Gio.ApplicationFlags.DEFAULT_FLAGS,
        )
        about_action = Gio.SimpleAction.new("about", None)
        about_action.connect("activate", self._on_about)
        self.add_action(about_action)

    def do_startup(self):
        Adw.Application.do_startup(self)
        self.set_accels_for_action("app.quit", ["<Control>q"])
        self.set_accels_for_action("app.refresh", ["F5"])
        self.set_accels_for_action("app.shortcuts", ["<Control>slash"])
        for n, cb in [("quit", lambda *_: self.quit()),
                      ("refresh", lambda *_: self._do_refresh()),
                      ("shortcuts", self._show_shortcuts_window)]:
            a = Gio.SimpleAction.new(n, None); a.connect("activate", cb); self.add_action(a)

    def _do_refresh(self):
        w = self.get_active_window()
        if w and hasattr(w, '_load_data'): w._load_data(force=True)
        elif w and hasattr(w, '_on_refresh'): w._on_refresh(None)

    def _show_shortcuts_window(self, *_args):
        win = Gtk.ShortcutsWindow(transient_for=self.get_active_window(), modal=True)
        section = Gtk.ShortcutsSection(visible=True, max_height=10)
        group = Gtk.ShortcutsGroup(visible=True, title="General")
        for accel, title in [("<Control>q", "Quit"), ("F5", "Refresh"), ("<Control>slash", "Keyboard shortcuts")]:
            s = Gtk.ShortcutsShortcut(visible=True, accelerator=accel, title=title)
            group.append(s)
        section.append(group)
        win.add_child(section)
        win.present()

    def do_activate(self):
        win = self.props.active_window
        if not win:
            win = LibreTranslateWindow(application=self)
        win.present()

    def _on_about(self, *_args):
        about = Adw.AboutDialog(
            application_name=_("LibreTranslate Assistant"),
            application_icon="libretranslate-gui",
            version="0.2.2",
            developer_name="Daniel Nylander",
            developers=["Daniel Nylander <daniel@danielnylander.se>"],
            copyright="© 2026 Daniel Nylander",
            license_type=Gtk.License.GPL_3_0,
            website="https://github.com/yeager/libretranslate-gui",
            issue_url="https://github.com/yeager/libretranslate-gui/issues",
            translator_credits=_("Translate this app: https://www.transifex.com/danielnylander/libretranslate-gui/"),
            comments=_("Translation assistant powered by LibreTranslate"),
        )
        about.add_link(_("Help translate"), "https://app.transifex.com/danielnylander/libretranslate-gui/")
        about.present(self.props.active_window)

def main():
    app = LibreTranslateApp()
    return app.run(sys.argv)

if __name__ == "__main__":
    sys.exit(main())
