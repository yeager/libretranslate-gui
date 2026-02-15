"""Main application window."""

import gi
gi.require_version("Gtk", "4.0")
gi.require_version("Adw", "1")
from gi.repository import Gtk, Adw, Gdk, Gio, GLib, Pango

from libretranslate_gui.api import LibreTranslateAPI, DEFAULT_URL
from libretranslate_gui.history import load_history, save_entry, clear_history
from libretranslate_gui.po_parser import parse_file

import gettext
import os
import json
from pathlib import Path

_ = gettext.gettext

SETTINGS_PATH = Path(os.environ.get("XDG_CONFIG_HOME", Path.home() / ".config")) / "libretranslate-gui" / "settings.json"


def _load_settings():
    if SETTINGS_PATH.exists():
        try:
            return json.loads(SETTINGS_PATH.read_text("utf-8"))
        except Exception:
            pass
    return {}


def _save_settings(data):
    SETTINGS_PATH.parent.mkdir(parents=True, exist_ok=True)
    SETTINGS_PATH.write_text(json.dumps(data, ensure_ascii=False, indent=2), "utf-8")


class LibreTranslateWindow(Adw.ApplicationWindow):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.set_title(_("LibreTranslate Assistant"))
        self.set_default_size(900, 700)

        settings = _load_settings()
        self.api = LibreTranslateAPI(
            server_url=settings.get("server_url", DEFAULT_URL),
            api_key=settings.get("api_key", ""),
        )
        self.languages = []
        self.source_lang = settings.get("source_lang", "en")
        self.target_lang = settings.get("target_lang", "sv")

        # Build UI
        self._build_ui()

        # Fetch languages
        self.api.get_languages_async(self._on_languages_loaded)

    def _build_ui(self):
        # Header bar
        header = Adw.HeaderBar()

        # Settings button
        settings_btn = Gtk.Button(icon_name="emblem-system-symbolic", tooltip_text=_("Settings"))
        settings_btn.connect("clicked", self._on_settings)
        header.pack_end(settings_btn)

        # History button
        history_btn = Gtk.Button(icon_name="document-open-recent-symbolic", tooltip_text=_("History"))
        history_btn.connect("clicked", self._on_history)
        header.pack_end(history_btn)

        # Open file button
        open_btn = Gtk.Button(icon_name="document-open-symbolic", tooltip_text=_("Open .po/.ts file"))
        open_btn.connect("clicked", self._on_open_file)
        header.pack_start(open_btn)

        # Main layout
        main_box = Gtk.Box(orientation=Gtk.Orientation.VERTICAL)
        main_box.append(header)

        content = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=12)
        content.set_margin_top(12)
        content.set_margin_bottom(12)
        content.set_margin_start(12)
        content.set_margin_end(12)

        # Language selectors row
        lang_row = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=8)
        lang_row.set_halign(Gtk.Align.CENTER)

        self.source_combo = Gtk.DropDown.new_from_strings(["en"])
        self.target_combo = Gtk.DropDown.new_from_strings(["sv"])
        self.source_combo.set_tooltip_text(_("Source language"))
        self.target_combo.set_tooltip_text(_("Target language"))

        swap_btn = Gtk.Button(icon_name="object-flip-horizontal-symbolic", tooltip_text=_("Swap languages"))
        swap_btn.connect("clicked", self._on_swap_languages)

        lang_row.append(Gtk.Label(label=_("From:")))
        lang_row.append(self.source_combo)
        lang_row.append(swap_btn)
        lang_row.append(Gtk.Label(label=_("To:")))
        lang_row.append(self.target_combo)
        content.append(lang_row)

        # Paned: source | target
        paned = Gtk.Paned(orientation=Gtk.Orientation.HORIZONTAL)
        paned.set_vexpand(True)
        paned.set_shrink_start_child(False)
        paned.set_shrink_end_child(False)

        # Source text
        source_frame = Gtk.Frame()
        source_box = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=4)
        source_box.set_margin_top(8)
        source_box.set_margin_bottom(8)
        source_box.set_margin_start(8)
        source_box.set_margin_end(8)

        source_header = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=8)
        source_label = Gtk.Label(label=_("Source Text"))
        source_label.add_css_class("heading")
        source_label.set_hexpand(True)
        source_label.set_halign(Gtk.Align.START)
        source_header.append(source_label)

        clear_btn = Gtk.Button(icon_name="edit-clear-symbolic", tooltip_text=_("Clear"))
        clear_btn.add_css_class("flat")
        clear_btn.connect("clicked", lambda b: self.source_view.get_buffer().set_text(""))
        source_header.append(clear_btn)
        source_box.append(source_header)

        source_scroll = Gtk.ScrolledWindow()
        source_scroll.set_vexpand(True)
        self.source_view = Gtk.TextView()
        self.source_view.set_wrap_mode(Gtk.WrapMode.WORD_CHAR)
        self.source_view.set_top_margin(8)
        self.source_view.set_bottom_margin(8)
        self.source_view.set_left_margin(8)
        self.source_view.set_right_margin(8)
        source_scroll.set_child(self.source_view)
        source_box.append(source_scroll)
        source_frame.set_child(source_box)
        paned.set_start_child(source_frame)

        # Target text
        target_frame = Gtk.Frame()
        target_box = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=4)
        target_box.set_margin_top(8)
        target_box.set_margin_bottom(8)
        target_box.set_margin_start(8)
        target_box.set_margin_end(8)

        target_header = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=8)
        target_label = Gtk.Label(label=_("Translation"))
        target_label.add_css_class("heading")
        target_label.set_hexpand(True)
        target_label.set_halign(Gtk.Align.START)
        target_header.append(target_label)

        copy_btn = Gtk.Button(icon_name="edit-copy-symbolic", tooltip_text=_("Copy translation"))
        copy_btn.add_css_class("flat")
        copy_btn.connect("clicked", self._on_copy)
        target_header.append(copy_btn)
        target_box.append(target_header)

        target_scroll = Gtk.ScrolledWindow()
        target_scroll.set_vexpand(True)
        self.target_view = Gtk.TextView()
        self.target_view.set_wrap_mode(Gtk.WrapMode.WORD_CHAR)
        self.target_view.set_editable(False)
        self.target_view.set_top_margin(8)
        self.target_view.set_bottom_margin(8)
        self.target_view.set_left_margin(8)
        self.target_view.set_right_margin(8)
        target_scroll.set_child(self.target_view)
        target_box.append(target_scroll)
        target_frame.set_child(target_box)
        paned.set_end_child(target_frame)

        content.append(paned)

        # Translate button + spinner
        btn_row = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=8)
        btn_row.set_halign(Gtk.Align.CENTER)
        self.translate_btn = Gtk.Button(label=_("Translate"))
        self.translate_btn.add_css_class("suggested-action")
        self.translate_btn.add_css_class("pill")
        self.translate_btn.connect("clicked", self._on_translate)
        btn_row.append(self.translate_btn)

        self.spinner = Gtk.Spinner()
        btn_row.append(self.spinner)

        content.append(btn_row)

        # Status bar
        self.status_label = Gtk.Label(label=_("Ready"))
        self.status_label.add_css_class("dim-label")
        self.status_label.set_halign(Gtk.Align.START)
        content.append(self.status_label)

        main_box.append(content)
        self.set_content(main_box)

    # --- Language handling ---

    def _on_languages_loaded(self, langs, err):
        GLib.idle_add(self._update_language_combos, langs, err)

    def _update_language_combos(self, langs, err):
        if err:
            self.status_label.set_text(_("Could not load languages: %s") % str(err))
            return
        self.languages = sorted(langs, key=lambda l: l.get("name", ""))
        names = [f"{l['name']} ({l['code']})" for l in self.languages]
        codes = [l["code"] for l in self.languages]

        model = Gtk.StringList.new(names)
        self.source_combo.set_model(model)
        self.target_combo.set_model(model.copy() if hasattr(model, 'copy') else Gtk.StringList.new(names))

        # Set defaults
        if self.source_lang in codes:
            self.source_combo.set_selected(codes.index(self.source_lang))
        if self.target_lang in codes:
            self.target_combo.set_selected(codes.index(self.target_lang))

        self.status_label.set_text(_("Loaded %d languages") % len(self.languages))

    def _get_selected_lang(self, combo):
        idx = combo.get_selected()
        if self.languages and 0 <= idx < len(self.languages):
            return self.languages[idx]["code"]
        return "en"

    # --- Actions ---

    def _on_translate(self, btn):
        buf = self.source_view.get_buffer()
        text = buf.get_text(buf.get_start_iter(), buf.get_end_iter(), False).strip()
        if not text:
            return
        src = self._get_selected_lang(self.source_combo)
        tgt = self._get_selected_lang(self.target_combo)

        self.translate_btn.set_sensitive(False)
        self.spinner.start()
        self.status_label.set_text(_("Translating…"))

        self.api.translate_async(text, src, tgt, lambda r, e: GLib.idle_add(self._on_translated, r, e, src, tgt, text))

    def _on_translated(self, result, err, src, tgt, original):
        self.translate_btn.set_sensitive(True)
        self.spinner.stop()
        if err:
            self.status_label.set_text(_("Error: %s") % str(err))
            return
        self.target_view.get_buffer().set_text(result)
        self.status_label.set_text(_("Done – %s → %s") % (src, tgt))
        save_entry(src, tgt, original, result)

    def _on_copy(self, btn):
        buf = self.target_view.get_buffer()
        text = buf.get_text(buf.get_start_iter(), buf.get_end_iter(), False)
        if text:
            clipboard = Gdk.Display.get_default().get_clipboard()
            clipboard.set(text)
            self.status_label.set_text(_("Copied to clipboard"))

    def _on_swap_languages(self, btn):
        si = self.source_combo.get_selected()
        ti = self.target_combo.get_selected()
        self.source_combo.set_selected(ti)
        self.target_combo.set_selected(si)

    # --- Settings dialog ---

    def _on_settings(self, btn):
        dialog = Adw.PreferencesWindow(transient_for=self)
        dialog.set_title(_("Settings"))

        page = Adw.PreferencesPage()
        group = Adw.PreferencesGroup(title=_("Server"))

        url_row = Adw.EntryRow(title=_("Server URL"))
        url_row.set_text(self.api.server_url)
        group.add(url_row)

        key_row = Adw.EntryRow(title=_("API Key (optional)"))
        key_row.set_text(self.api.api_key)
        group.add(key_row)

        page.add(group)
        dialog.add(page)

        dialog.connect("close-request", lambda d: self._save_server_settings(url_row.get_text(), key_row.get_text()))
        dialog.present()

    def _save_server_settings(self, url, key):
        self.api.server_url = url.rstrip("/") if url else DEFAULT_URL
        self.api.api_key = key
        settings = _load_settings()
        settings["server_url"] = self.api.server_url
        settings["api_key"] = key
        settings["source_lang"] = self._get_selected_lang(self.source_combo)
        settings["target_lang"] = self._get_selected_lang(self.target_combo)
        _save_settings(settings)
        # Reload languages from new server
        self.api.get_languages_async(self._on_languages_loaded)

    # --- History ---

    def _on_history(self, btn):
        history = load_history()
        if not history:
            self.status_label.set_text(_("No history yet"))
            return

        dialog = Adw.Window(transient_for=self)
        dialog.set_title(_("Translation History"))
        dialog.set_default_size(600, 500)
        dialog.set_modal(True)

        tb = Adw.HeaderBar()
        clear_btn = Gtk.Button(label=_("Clear"))
        clear_btn.add_css_class("destructive-action")
        clear_btn.connect("clicked", lambda b: (clear_history(), dialog.close()))
        tb.pack_end(clear_btn)

        vbox = Gtk.Box(orientation=Gtk.Orientation.VERTICAL)
        vbox.append(tb)

        scroll = Gtk.ScrolledWindow()
        scroll.set_vexpand(True)
        listbox = Gtk.ListBox()
        listbox.set_selection_mode(Gtk.SelectionMode.NONE)
        listbox.add_css_class("boxed-list")

        for entry in history[:50]:
            row = Adw.ActionRow(
                title=GLib.markup_escape_text(entry.get("source", "")[:80]),
                subtitle=GLib.markup_escape_text(entry.get("translation", "")[:80]),
            )
            row.add_suffix(Gtk.Label(label=f"{entry.get('source_lang','?')}→{entry.get('target_lang','?')}"))
            # Click to load
            row.set_activatable(True)
            row.connect("activated", self._on_history_row_activated, entry, dialog)
            listbox.append(row)

        scroll.set_child(listbox)
        vbox.append(scroll)
        dialog.set_content(vbox)
        dialog.present()

    def _on_history_row_activated(self, row, entry, dialog):
        self.source_view.get_buffer().set_text(entry.get("source", ""))
        self.target_view.get_buffer().set_text(entry.get("translation", ""))
        dialog.close()

    # --- File open (.po/.ts) ---

    def _on_open_file(self, btn):
        dialog = Gtk.FileDialog()
        f = Gtk.FileFilter()
        f.set_name(_("Translation files (*.po, *.ts)"))
        f.add_pattern("*.po")
        f.add_pattern("*.ts")
        filters = Gio.ListStore.new(Gtk.FileFilter)
        filters.append(f)
        dialog.set_filters(filters)
        dialog.open(self, None, self._on_file_opened)

    def _on_file_opened(self, dialog, result):
        try:
            file = dialog.open_finish(result)
        except Exception:
            return
        filepath = file.get_path()
        if not filepath:
            return
        try:
            entries = parse_file(filepath)
        except Exception as e:
            self.status_label.set_text(_("Error parsing file: %s") % str(e))
            return
        untranslated = [e for e in entries if e["untranslated"]]
        if not untranslated:
            self.status_label.set_text(_("No untranslated strings found"))
            return
        self._show_po_window(filepath, untranslated)

    def _show_po_window(self, filepath, entries):
        dialog = Adw.Window(transient_for=self)
        dialog.set_title(_("Untranslated strings – %s") % os.path.basename(filepath))
        dialog.set_default_size(700, 500)
        dialog.set_modal(True)

        tb = Adw.HeaderBar()
        translate_all_btn = Gtk.Button(label=_("Translate All"))
        translate_all_btn.add_css_class("suggested-action")
        tb.pack_end(translate_all_btn)

        vbox = Gtk.Box(orientation=Gtk.Orientation.VERTICAL)
        vbox.append(tb)

        scroll = Gtk.ScrolledWindow()
        scroll.set_vexpand(True)
        listbox = Gtk.ListBox()
        listbox.set_selection_mode(Gtk.SelectionMode.NONE)
        listbox.add_css_class("boxed-list")

        rows_data = []
        for entry in entries:
            row = Adw.ActionRow(
                title=GLib.markup_escape_text(entry["msgid"][:100]),
                subtitle=_("Click Translate All to get suggestions"),
            )
            rows_data.append((row, entry))
            listbox.append(row)

        scroll.set_child(listbox)
        vbox.append(scroll)
        dialog.set_content(vbox)

        src = self._get_selected_lang(self.source_combo)
        tgt = self._get_selected_lang(self.target_combo)
        translate_all_btn.connect("clicked", lambda b: self._translate_po_entries(rows_data, src, tgt, b))

        dialog.present()

    def _translate_po_entries(self, rows_data, src, tgt, btn):
        btn.set_sensitive(False)
        import threading
        def _work():
            for row, entry in rows_data:
                try:
                    result = self.api.translate(entry["msgid"], src, tgt)
                    GLib.idle_add(row.set_subtitle, GLib.markup_escape_text(result))
                except Exception as e:
                    GLib.idle_add(row.set_subtitle, f"Error: {e}")
            GLib.idle_add(btn.set_sensitive, True)
        threading.Thread(target=_work, daemon=True).start()
