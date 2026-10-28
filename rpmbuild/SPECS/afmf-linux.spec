# afmf-linux — repackaged from the official upstream binary rpm.
# Update procedure: bump Version, update the sha256 comment, rebuild.

# Prebuilt stripped binary — nothing to debug-extract.
%global debug_package %{nil}

Name:           afmf-linux
Version:        1.3.1
Release:        1%{?dist}
Summary:        AMD Fluid Motion Frames for Linux: Vulkan frame generation layer

License:        MIT
URL:            https://afmf-linux.digitalexperiments.dev/
Source0:        https://github.com/serialexperimentslainnnn/afmf-linux/releases/download/v%{version}/afmf-linux-%{version}-1.fc44.x86_64.rpm
# sha256(Source0) = 381697db6b28ff65cfa38b73094159efe86a98eafaa028c0fdb32e29a52b49d4

BuildArch:      x86_64
BuildRequires:  cpio

Requires:       vulkan-loader

%description
An open-source equivalent of AMD Fluid Motion Frames (AFMF) for Linux: a
Vulkan implicit layer that generates one interpolated frame between every
two frames a game presents, from the colour buffer alone, using FidelityFX
Optical Flow. Works with any 64-bit Vulkan application, including DXVK and
vkd3d-proton titles under Proton. The layer stays dormant unless
AFMF_ENABLE=1 is set for a game. This package repackages the official
upstream rpm so it can be managed with dnf.

%prep
%setup -q -T -c -n %{name}-%{version}

# Unpack the upstream binary rpm into the build directory.
rpm2cpio %{SOURCE0} | cpio -idmu --quiet

# The debuginfo split already happened upstream; drop the build-id
# symlink so it doesn't dangle in our repack.
rm -rf usr/lib/.build-id

%install
rm -rf %{buildroot}
mkdir -p %{buildroot}
cp -a . %{buildroot}

# Regenerate the %files list from the extracted tree, skipping
# directories owned by the "filesystem" package.
cat > std-dirs <<'EOF'
/usr
/usr/lib
/usr/lib64
/usr/share
/usr/share/doc
/usr/share/licenses
/usr/share/vulkan
/usr/share/vulkan/implicit_layer.d
EOF
find %{buildroot} -mindepth 1 -printf '/%%P\n' \
    | grep -Fvx -f std-dirs > %{name}.files

%files -f %{_builddir}/%{name}-%{version}/%{name}.files
%defattr(-,root,root,-)

%changelog
* Wed Sep 23 2026 Noel Knubel - 1.3.1-1
- Initial repack of the official upstream rpm for COPR.
