# pyrofling — built from a source snapshot that vendors the
# Granite and FFmpeg git submodules (GitHub auto-tarballs don't
# include submodules, so scripts/make-pyrofling-tarball.sh creates
# Source0). Upstream has no version tags; the version is the snapshot
# date. To update: re-run the script with a new date, update Version.
#
# EXPECT THE FIRST BUILD TO FAIL once or twice: if cmake configure or
# the compiler complains about a missing package, add it to
# BuildRequires and bump Release. The copr log names it exactly.
# After the first successful build, verify the installed paths in the
# log's "install" section against the %files list below.

Name:           pyrofling
Version:        20261025
Release:        2%{?dist}
Summary:        Vulkan capture/streaming tooling from Themaister (server, viewer, layers)

License:        MIT
URL:            https://github.com/Themaister/pyrofling
Source0:        pyrofling-%{version}.tar.xz

BuildRequires:  cmake
BuildRequires:  gcc-c++
BuildRequires:  ninja-build
BuildRequires:  vulkan-headers
BuildRequires:  libdrm-devel
BuildRequires:  libX11-devel
BuildRequires:  wayland-devel
BuildRequires:  nasm
# nasm: needed by the vendored FFmpeg build.
# The vendored Granite bundles SDL3, which hard-fails at configure time
# unless it finds a desktop video stack (Wayland/X11 + EGL + xkbcommon).
BuildRequires:  libglvnd-devel
BuildRequires:  mesa-libEGL-devel
BuildRequires:  mesa-libGL-devel
BuildRequires:  libxkbcommon-devel
BuildRequires:  libXcursor-devel
BuildRequires:  libXrandr-devel
BuildRequires:  libXi-devel
BuildRequires:  libXfixes-devel

%description
PyroFling captures Vulkan applications and streams video/audio with
low latency. This package builds the server (pyrofling), the client
(pyrofling-viewer) and the Vulkan layers, including
latency-measurement-layer.

%prep
%setup -q

%build
%cmake -DCMAKE_BUILD_TYPE=Release -GNinja
%cmake_build

%install
%cmake_install

%files
%license LICENSE
%{_bindir}/pyrofling
%{_bindir}/pyrofling-viewer
%{_datadir}/vulkan/implicit_layer.d/*
# If the layer turns out to be explicit (or installs under a different
# name), adjust this line after reading the build log.

%changelog
* Sun Oct 25 2026 Noel Knubel - 20261025-2
- Add SDL3 desktop-video build requirements (vendored Granite bundles SDL3).

* Sun Oct 25 2026 Noel Knubel - 20261025-1
- Initial package from upstream snapshot.