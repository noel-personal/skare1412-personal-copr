# heroic — repackaged from the official upstream binary rpm.
# Update procedure: bump Version, update the sha256 comment, rebuild.

Name:           heroic
Version:        2.22.4
Release:        1%{?dist}
Summary:        Games launcher for GOG, Epic and Amazon Games

License:        GPL-3.0-only AND MIT AND BSD-3-Clause
URL:            https://heroicgameslauncher.com
Source0:        https://github.com/Heroic-Games-Launcher/HeroicGamesLauncher/releases/download/v%{version}/Heroic-%{version}-linux-x86_64.rpm
# sha256(Source0) = c346ce64b5f29a53367c8fd701d061b9a3a83a7b5d53135a31a81147a36951e4

BuildArch:      x86_64
BuildRequires:  cpio

# ELF auto-dependencies cover the libraries; these are the
# non-library bits Electron apps need.
Requires:       xdg-utils
Requires:       hicolor-icon-theme

%description
Heroic is an Open Source Game Launcher for Linux. It supports launching
games from the Epic Games Store, GOG and Amazon Games. This package
repackages the official upstream rpm so it can be managed with dnf.

%prep
%setup -q -T -c -n %{name}-%{version}

# Unpack the upstream binary rpm into the build directory.
rpm2cpio %{SOURCE0} | cpio -idmu --quiet

%install
rm -rf %{buildroot}
mkdir -p %{buildroot}
cp -a . %{buildroot}

# Regenerate the %files list from the extracted tree, skipping
# directories owned by the "filesystem" package.
cat > std-dirs <<'EOF'
/bin
/etc
/etc/opt
/opt
/usr
/usr/bin
/usr/lib
/usr/lib64
/usr/libexec
/usr/local
/usr/sbin
/usr/share
/usr/share/applications
/usr/share/appdata
/usr/share/doc
/usr/share/icons
/usr/share/icons/hicolor
/usr/share/licenses
/usr/share/metainfo
/usr/share/mime
/usr/share/mime-info
/usr/share/pixmaps
/var
EOF
find %{buildroot} -mindepth 1 -printf '/%%P\n' \
    | grep -Fvx -f std-dirs > %{name}.files

%files -f %{_builddir}/%{name}-%{version}/%{name}.files
%defattr(-,root,root,-)

%post
/bin/touch --no-create %{_datadir}/icons/hicolor 2>/dev/null || :

%postun
if [ $1 -eq 0 ]; then
    /bin/touch --no-create %{_datadir}/icons/hicolor 2>/dev/null || :
    gtk-update-icon-cache -qtf %{_datadir}/icons/hicolor 2>/dev/null || :
    update-desktop-database -q 2>/dev/null || :
fi

%changelog
* Sun Oct 25 2026 Noel Knubel - 2.22.4-1
- Initial repack of the official upstream rpm for COPR.