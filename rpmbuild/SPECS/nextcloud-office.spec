# nextcloud-office-nextcloudoffice — repackaged from the official
# upstream binary rpm (signed production build).
# NOTE: upstream's release number is currently "0" and appears both in
# the asset filename and the Release field. When a new version comes
# out, check the asset name on the releases page and update both.
# Installs alongside euro-office without conflicts (separate dirs).

# Upstream binaries are prebuilt/stripped: no debuginfo, and their
# embedded vendor rpaths are fixed up via QA_RPATHS in %%install.
%global debug_package %{nil}

Name:           nextcloud-office-nextcloudoffice
Version:        9.3.6
Release:        2%{?dist}
Summary:        Nextcloud Office Desktop Editors (production build of the Euro-Office fork)

License:        AGPL-3.0-only
URL:            https://github.com/nextcloud-releases/Office-DesktopEditors
Source0:        https://github.com/nextcloud-releases/Office-DesktopEditors/releases/download/v%{version}/nextcloud-office-nextcloudoffice-%{version}-0.x86_64.rpm
# sha256(Source0) = b2c472f2bd36122e4a6187e2959b6d9ae209a70a502ed3438165c121a4ddddd1

BuildArch:      x86_64
BuildRequires:  cpio

Requires:       fontconfig
Requires:       hicolor-icon-theme

%description
Nextcloud Office Desktop Editors: the office suite fork derived from
ONLYOFFICE, in its signed, production-ready Nextcloud branding. This
package repackages the official upstream rpm so it can be managed with
dnf.

%prep
%setup -q -T -c -n %{name}-%{version}
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
* Sun Oct 25 2026 Noel Knubel - 9.3.6-2
- Escape spaces in upstream filenames ("05_green leaf.pptx" theme
  source) as "?" globs in the generated %files list.

* Sun Oct 25 2026 Noel Knubel - 9.3.6-1
- Skip debuginfo (prebuilt stripped binaries), ignore vendor rpaths.

* Sun Oct 25 2026 Noel Knubel - 9.3.6-0
- Initial repack of the official upstream rpm for COPR.