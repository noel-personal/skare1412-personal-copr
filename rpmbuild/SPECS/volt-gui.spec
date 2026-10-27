# volt-gui — repackaged from the official upstream release tarball
# (make release-container output: prebuilt binaries with a fixed
# glibc floor). Same repack pattern as heroic.spec.
# Update procedure: bump Version, update the sha256 comment, rebuild.
#
# The release tarball is a ready-to-install tree: the upstream
# Makefile stages it with `make install DESTDIR=... PREFIX=/usr`,
# which skips the live-system guards and ldconfig. The optional
# Flatpak runtime-extension bundles in build/bundles/ are NOT
# packaged here — install those from upstream releases if needed.
#
# The 32-bit layer (lib/i386) is included deliberately: upstream
# treats it as non-optional so 32-bit Steam games work; it pulls the
# i686 glibc/libgcc runtime deps via RPM auto-requires.

# Prebuilt stripped binaries — no debuginfo.
%global debug_package %{nil}

Name:           volt-gui
Version:        2.4.2
Release:        1%{?dist}
Summary:        Control panel for Vulkan games: settings applied by the volt implicit Vulkan layer

License:        GPL-3.0-only
URL:            https://github.com/pythonlover02/volt-gui
Source0:        https://github.com/pythonlover02/volt-gui/releases/download/v%{version}/volt-gui-%{version}.tar.gz
# sha256(Source0) = f06934f1256ed4cc84ae0306776c386d13caf1cd9c734a33537873b70d54c2d4

BuildArch:      x86_64
BuildRequires:  make >= 4.3

Requires:       vulkan-loader
Recommends:     libxcb
Recommends:     libwayland-client
# volt-probe dlopens libxcb or libwayland-client at runtime; either
# is optional, both together cover X11 and Wayland hosts.

%description
volt-gui is a control panel for Vulkan games on Linux. Settings are
applied by volt, an implicit Vulkan layer written in Rust, so they
work on every driver: RADV, ANV, NVK, AMDVLK, NVIDIA proprietary.

The layer only activates when the volt launcher sets VOLT_ENABLE on
the child process, so it is safe to install system-wide. Use it as
`volt -- %command%` in Steam launch options, or `volt -- ./game`.

This package repackages the official upstream release tarball
(64-bit and 32-bit layer, launcher, probe, and the self-contained
PySide6 GUI) so it can be managed with dnf.

%prep
%setup -q

%build
# Nothing to build: upstream release ships prebuilt binaries
# (built in rust:1.85.1-bookworm, glibc 2.36 floor).

%install
make install DESTDIR=%{buildroot} PREFIX=%{_prefix} OUT=build

%post
/bin/touch --no-create %{_datadir}/icons/hicolor 2>/dev/null || :

%postun
if [ $1 -eq 0 ]; then
    /bin/touch --no-create %{_datadir}/icons/hicolor 2>/dev/null || :
    gtk-update-icon-cache -qtf %{_datadir}/icons/hicolor 2>/dev/null || :
    update-desktop-database -q 2>/dev/null || :
fi

%files
%license LICENSE
%doc README.md
%{_bindir}/volt
%{_bindir}/volt-probe
%{_bindir}/volt-gui
%{_libdir}/libvolt.so
%{_prefix}/lib/libvolt.so
%{_datadir}/vulkan/implicit_layer.d/VkLayer_volt.json
%{_datadir}/applications/volt-gui.desktop
%{_datadir}/icons/hicolor/256x256/apps/volt-gui.png

%changelog
* Mon Oct 27 2026 Noel Knubel - 2.4.2-1
- Initial repack of the official upstream release tarball for COPR.
