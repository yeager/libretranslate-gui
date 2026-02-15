"""Minimal .po / .ts file parser for translation suggestions."""

import re
import xml.etree.ElementTree as ET


def parse_po(filepath):
    """Parse a .po file, return list of dicts {msgid, msgstr, line, untranslated}."""
    entries = []
    with open(filepath, "r", encoding="utf-8") as f:
        content = f.read()

    # Split on blank lines to get entries
    blocks = re.split(r"\n\n+", content)
    for block in blocks:
        msgid_match = re.search(r'msgid\s+"((?:[^"\\]|\\.)*)"', block)
        msgstr_match = re.search(r'msgstr\s+"((?:[^"\\]|\\.)*)"', block)
        if msgid_match:
            msgid = msgid_match.group(1)
            msgstr = msgstr_match.group(1) if msgstr_match else ""
            if msgid:  # skip empty msgid (header)
                entries.append({
                    "msgid": msgid,
                    "msgstr": msgstr,
                    "untranslated": msgstr == "",
                })
    return entries


def parse_ts(filepath):
    """Parse a Qt .ts file, return list of dicts {source, translation, untranslated}."""
    entries = []
    tree = ET.parse(filepath)
    root = tree.getroot()
    for msg in root.iter("message"):
        src = msg.findtext("source", "")
        tr = msg.findtext("translation", "")
        tr_elem = msg.find("translation")
        unfinished = tr_elem is not None and tr_elem.get("type") == "unfinished"
        entries.append({
            "msgid": src,
            "msgstr": tr,
            "untranslated": tr == "" or unfinished,
        })
    return entries


def parse_file(filepath):
    """Auto-detect .po or .ts and parse."""
    if filepath.endswith(".ts"):
        return parse_ts(filepath)
    return parse_po(filepath)
