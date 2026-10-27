# pyrofling — built from a source snapshot that vendors the Granite
# submodule (scripts/make-pyrofling-tarball.sh creates Source0; the
# ffmpeg submodule is NOT needed on Linux — Granite links system
# FFmpeg through pkg-config). Upstream has no version tags; the
# version is the snapshot date. To update: re-run the script with a
# new date, update Version.
#
# Hard configure requirements (from Granite + pyrofling CMake):
#   - pkg-config modules libavdevice/libavformat/libavcodec/libavutil
#     (Granite/video/CMakeLists.txt: pkg_check_modules(LIBAV REQUIRED ...))
#     -> ffmpeg-free-devel
#   - Python3 (Granite blobify/bin_to_text for the viewer font blob)
#   - libpipewire-0.3 is optional at configure time, but without it
#     the server loses Pipewire capture support -> pipewire-devel
#   - libpulse is optional (Granite audio backend) -> pulseaudio-libs-devel
# The vendored SDL3 (via Granite) fails gracefully when X11/Wayland
# pieces are missing, but with the BRs below it gets a full desktop
# video stack.

Name:           pyrofling
Version:        20261025
Release:        3%{?dist}
Summary:        Vulkan capture/streaming tooling from Themaister (server, viewer, layers)

License:        MIT AND GPL-3.0-or-later
# MIT for PyroFling code; the binaries link Fedora's GPL FFmpeg
# (ffmpeg-free), which applies GPL to the combined work.
URL:            https://github.com/Themaister/pyrofling
Source0:        pyrofling-%{version}.tar.xz

BuildRequires:  cmake
BuildRequires:  gcc-c++
BuildRequires:  ninja-build
BuildRequires:  pkgconf-pkg-config
BuildRequires:  python3
BuildRequires:  vulkan-headers
BuildRequires:  ffmpeg-free-devel
BuildRequires:  pipewire-devel
BuildRequires:  pulseaudio-libs-devel
BuildRequires:  libdrm-devel
BuildRequires:  libX11-devel
BuildRequires:  wayland-devel
BuildRequires:  libglvnd-devel
BuildRequires:  mesa-libEGL-devel
BuildRequires:  mesa-libGL-devel
BuildRequires:  libxkbcommon-devel
BuildRequires:  libXcursor-devel
BuildRequires:  libXrandr-devel
BuildRequires:  libXi-devel
BuildRequires:  libXfixes-devel

Requires:       vulkan-loader

%description
PyroFling captures Vulkan applications and streams video/audio with
low latency. This package builds the server (pyrofling), the client
(pyrofling-viewer), the gamepad client, the latency tester, and the
Vulkan layers (capture, cross-WSI and latency-measurement).

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
%{_bindir}/pyrofling-gamepad
%{_bindir}/pyrofling-latency-tester
%{_libdir}/libVkLayer_pyrofling*.so
%{_datadir}/vulkan/implicit_layer.d/VkLayer_pyrofling*.json

%changelog
* Mon Oct 27 2026 Noel Knubel - 20261025-3
- Add the real configure requirements: ffmpeg-free-devel (Granite
  links system libavdevice/libavformat/libavcodec/libavutil via
  pkg-config), python3 (viewer font blob), pipewire-devel,
  pulseaudio-libs-devel, pkgconf-pkg-config. Drop nasm (the ffmpeg
  submodule is never built on Linux).
- Complete the files list: layer .so files land in the libdir, and
  pyrofling-gamepad / pyrofling-latency-tester are installed too.

* Sun Oct 25 2026 Noel Knubel - 20261025-2
- Add SDL3 desktop-video build requirements (vendored Granite bundles SDL3).

* Sun Oct 25 2026 Noel Knubel - 20261025-1
- Initial package from upstream snapshot.
