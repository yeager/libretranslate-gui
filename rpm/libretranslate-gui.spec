Name:           libretranslate-gui
Version:        0.1.0
Release:        1%{?dist}
Summary:        GTK4/Adwaita translation assistant using LibreTranslate API
License:        GPL-3.0-or-later
URL:            https://github.com/yeager/libretranslate-gui
BuildArch:      noarch
Requires:       python3 >= 3.10
Requires:       python3-gobject
Requires:       gtk4
Requires:       libadwaita

%description
A desktop application for translating text using the LibreTranslate API.
Supports live translation, batch mode, .po/.ts file support, configurable
server URL, translation history, and clipboard integration.

%install
mkdir -p %{buildroot}/usr/lib/python3/dist-packages/libretranslate_gui
mkdir -p %{buildroot}/usr/bin
mkdir -p %{buildroot}/usr/share/applications
mkdir -p %{buildroot}/usr/share/icons/hicolor/scalable/apps
cp -r %{_sourcedir}/src/libretranslate_gui/*.py %{buildroot}/usr/lib/python3/dist-packages/libretranslate_gui/
cp %{_sourcedir}/launcher %{buildroot}/usr/bin/libretranslate-gui
chmod 755 %{buildroot}/usr/bin/libretranslate-gui
cp %{_sourcedir}/data/se.danielnylander.LibreTranslateAssistant.desktop %{buildroot}/usr/share/applications/
cp %{_sourcedir}/data/se.danielnylander.LibreTranslateAssistant.svg %{buildroot}/usr/share/icons/hicolor/scalable/apps/

%files
/usr/lib/python3/dist-packages/libretranslate_gui/
/usr/bin/libretranslate-gui
/usr/share/applications/se.danielnylander.LibreTranslateAssistant.desktop
/usr/share/icons/hicolor/scalable/apps/se.danielnylander.LibreTranslateAssistant.svg
