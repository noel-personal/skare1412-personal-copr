# msttcore-fonts-installer — repackaged from the upstream installer rpm.
# The rpm contains NO fonts: the scriptlet downloads the MS font cabs
# from SourceForge at install time, under their EULA. That is why
# hosting this in a (public) copr is unproblematic, and why it must
# never be "fixed" to bundle the actual font files.
# The repack also gives the old noarch rpm fresh metadata and
# dependency generation (the stock rpm predates current dnf5 checks).

Name:           msttcore-fonts-installer
Version:        2.6
Release:        1%{?dist}
Summary:        Installer for Microsoft core TrueType fonts

License:        GPLv2
URL:            https://github.com/isboston/msttcore-fonts
Source0:        https://github.com/isboston/msttcore-fonts/releases/latest/download/msttcore-fonts-installer-%{version}-1.noarch.rpm
# sha256(Source0) = cf1ba94ce3b5e83629659a397b179f12b36c455e5312f25addd02005a9f954bd
# NOTE: /latest/download/ always serves the newest release; if upstream
# bumps to 2.7 the old filename 404s — update Version and the filename.

Obsoletes:      msttcorefonts <= 2.5-1
Provides:       msttcorefonts = 2.6-1

BuildArch:      noarch
BuildRequires:  cpio

Requires:       curl
Requires:       cabextract
Requires:       xorg-x11-font-utils
Requires(post): fontconfig
Requires(postun): fontconfig

%global fontdir         %{_datadir}/fonts/msttcore
%global download_script %{_prefix}/lib/msttcore-fonts-installer/refresh-msttcore-fonts.sh
%global license_file    %{_defaultdocdir}/msttcore-fonts-installer

%description
Installs the TrueType core fonts for the web (Arial, Times New Roman,
Verdana, ...) plus Microsoft's ClearType fonts (Calibri, Cambria,
Candara, Consolas, Constantia, Corbel). The font cab files are
downloaded and unpacked at install time; they are not part of the rpm
and are not redistributed by it.

%prep
%setup -q -T -c -n %{name}-%{version}
rpm2cpio %{SOURCE0} | cpio -idmu --quiet

%install
rm -rf %{buildroot}
mkdir -p %{buildroot}
cp -a . %{buildroot}

cat > std-dirs <<'EOF'
/bin
/etc
/usr
/usr/bin
/usr/lib
/usr/lib64
/usr/libexec
/usr/sbin
/usr/share
/usr/share/doc
/usr/share/fonts
/usr/share/licenses
/var
EOF
find %{buildroot} -mindepth 1 -printf '/%P\n' \
    | grep -Fvx -f std-dirs > %{name}.files

%files -f %{_builddir}/%{name}-%{version}/%{name}.files
%defattr(-,root,root,-)

%post
# Download and install the fonts (network required at install time).
%{download_script} -F %{fontdir} -L %{license_file} || :

%postun
# Font files are created by the scriptlet, so rpm can't remove them.
if [ "$1" = "0" ]; then
    rm -f %{fontdir}/*.ttf %{fontdir}/*.ttc 2>/dev/null || :
    if [ -x %{_bindir}/fc-cache ]; then
        %{_bindir}/fc-cache -f %{fontdir} || :
    fi
    rm -f /usr/lib/msttcore-fonts-installer/installed-list.txt 2>/dev/null || :
fi

%changelog
* Sun Oct 25 2026 Noel Knubel - 2.6-1
- Repack of the upstream installer rpm for COPR, with fresh metadata.