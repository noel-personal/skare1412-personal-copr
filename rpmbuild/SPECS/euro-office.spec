# euro-office — repackaged from the official upstream binary rpm
# (unsigned community build of the same source as nextcloud-office).
# Same caveats as nextcloud-office-nextcloudoffice.spec: check the
# asset filename and release number when bumping the version.
# Profile data: ~/.local/share/euro-office/euro-office and
# ~/.config/euro-office (not migrated from OnlyOffice automatically).

# Upstream binaries are prebuilt/stripped: no debuginfo, and their
# embedded vendor rpaths are fixed up via QA_RPATHS in %%install.
%global debug_package %{nil}

Name:           euro-office
Version:        9.3.6
Release:        2%{?dist}
Summary:        Euro-Office Desktop Editors (community build)

License:        AGPL-3.0-only
URL:            https://github.com/Euro-Office/DesktopEditors
Source0:        https://github.com/Euro-Office/DesktopEditors/releases/download/v%{version}/euro-office-euro-office-%{version}-0.x86_64.rpm
# sha256(Source0) = 1354f91ff0c2b13b414f671d965ddab4e732bbd38860455f85f01e8681463a86

BuildArch:      x86_64
BuildRequires:  cpio

Requires:       fontconfig
Requires:       hicolor-icon-theme

%description
Euro-Office Desktop Editors: the AGPL European community fork of the
ONLYOFFICE office suite, built from the same source as Nextcloud Office
(unsigned community build). This package repackages the official
upstream rpm so it can be managed with dnf.

%prep
%setup -q -T -c -n euro-office-%{version}
rpm2cpio %{SOURCE0} | cpio -idmu --quiet

%install
rm -rf %{buildroot}
mkdir -p %{buildroot}
cp -a . %{buildroot}

# Don't let check-rpaths fail on the upstream binaries' vendor rpaths
# (bitmask: standard | invalid | $ORIGIN-position | empty).
export QA_RPATHS=$(( 0x0001 | 0x0002 | 0x0008 | 0x0010 ))

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
# rpm splits %files manifest lines on whitespace, so a filename with a
# space breaks the build. Escape spaces as "?" glob wildcards instead.
find %{buildroot} -mindepth 1 -printf '/%%P\n' \
    | grep -Fvx -f std-dirs \
    | sed 's/ /?/g' > %{name}.files

%files -f %{_builddir}/euro-office-%{version}/%{name}.files
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
* Sun Oct 25 2026 Noel Knubel - 9.3.6-2
- Escape spaces in upstream filenames ("05_green leaf.pptx" theme
  source) as "?" globs in the generated %files list.

* Sun Oct 25 2026 Noel Knubel - 9.3.6-1
- Skip debuginfo (prebuilt stripped binaries), ignore vendor rpaths.

* Sun Oct 25 2026 Noel Knubel - 9.3.6-0
- Initial repack of the official upstream rpm for COPR.