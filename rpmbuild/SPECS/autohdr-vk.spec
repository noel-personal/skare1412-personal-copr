# autohdr-vk — TEMPLATE. Build system assumed CMake; adjust as noted.
# Source0 is created locally (scripts/make-local-tarball.sh) because
# the repo is private: copr cannot pull it, so we build the SRPM
# locally and upload it with copr-cli.

Name:           autohdr-vk
Version:        0.1.0
Release:        1%{?dist}
Summary:        Vulkan layer: automatic HDR handling (autohdr)

License:        MIT
URL:            https://github.com/skare-sandbox/autohdr-vk
Source0:        autohdr-vk-%{version}.tar.xz

BuildRequires:  cmake
BuildRequires:  gcc-c++
BuildRequires:  ninja-build
BuildRequires:  vulkan-headers
# TODO: add whatever the layer actually links against
# (glslang-devel? libdrm-devel? check your CMakeLists).

%description
Vulkan layer for automatic HDR tone mapping, developed on skare-pc.
Private project; built and uploaded manually via copr-cli.

%prep
%setup -q

%build
%cmake -DCMAKE_BUILD_TYPE=Release -GNinja
%cmake_build

%install
%cmake_install

%files
%license LICENSE
%{_datadir}/vulkan/implicit_layer.d/autohdr*.json
%{_datadir}/vulkan/implicit_layer.d/*.so
# TODO: verify against the actual install paths in your build;
# some layers install the .so as libVkLayer_*.so next to the json.

%changelog
* Sun Oct 25 2026 Noel Knubel - 0.1.0-1
- Template for initial COPR packaging.