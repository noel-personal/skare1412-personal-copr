# vksumi — based on the spec upstream maintains in-tree at
# packaging/vksumi.spec (their Fedora CI builds RPMs with it).
# Version follows upstream git tags (v0.1.0 latest, Oct 2026).
# Update procedure: bump Version, update the sha256 comment, rebuild.

Name:           vksumi
Version:        0.1.0
Release:        1%{?dist}
Summary:        Vulkan layer for runtime color grading on Linux

License:        MIT
URL:            https://github.com/reakjra/vkSumi
Source0:        https://github.com/reakjra/vkSumi/archive/refs/tags/v%{version}/vkSumi-%{version}.tar.gz
# Update procedure: bump Version, refresh the sha256 comment below.

BuildRequires:  meson
BuildRequires:  ninja-build
BuildRequires:  glslang
BuildRequires:  gcc-c++
BuildRequires:  vulkan-loader-devel
BuildRequires:  libX11-devel
BuildRequires:  pkgconf-pkg-config

Requires:       vulkan-loader
Requires:       libX11

%description
vkSumi is an implicit Vulkan layer that exposes runtime color-grading
sliders (brightness, contrast, saturation, hue, gamma, RGB gain,
3-band lift/gain) via a hot-reloadable .conf file. Per-game configs
auto-create on first launch. The Adrenalin / NVIDIA Freestyle
equivalent that has been missing on Linux.

The layer only activates when ENABLE_VKSUMI=1 is set, so it is safe
to install system-wide. Configure it via ~/.config/vkSumi/vkSumi.conf
and toggle with the bundled vksumi-toggle.

%prep
%autosetup -n vkSumi-%{version}

%build
%meson
%meson_build

%install
%meson_install

%files
%license LICENSE
%doc README.md
%{_libdir}/libVkLayer_vksumi.so
%{_datadir}/vulkan/implicit_layer.d/vksumi.json
%{_bindir}/vksumi-toggle

%changelog
* Mon Oct 27 2026 Noel Knubel - 0.1.0-1
- Initial package, based on upstream's packaging/vksumi.spec.
