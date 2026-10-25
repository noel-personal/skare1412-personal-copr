# discord-flatpak-rpc-bridge — native rpm of Arcitec's bridge.
# The whole thing is two systemd user units (the service runs
# systemd-socket-proxyd, part of systemd) plus the management script.
# Upstream has no versioned releases; 1.0.0 is our choice. To update:
# point Source0 at the newer commit hash, note it in the comment there,
# bump Release. (%prep strips the tarball's leading directory, so the
# commit hash never appears in any path.)

Name:           discord-flatpak-rpc-bridge
Version:        1.0.0
Release:        2%{?dist}
Summary:        Discord Rich Presence bridge for Flatpak apps (native Discord client)

License:        GPL-2.0-only
URL:            https://github.com/Arcitec/discord-flatpak-rpc-bridge
Source0:        https://github.com/Arcitec/discord-flatpak-rpc-bridge/archive/621eec8.tar.gz
# commit 621eec8 (2026-09-23): "workaround for uutil's broken mode-parser"

BuildArch:      noarch
Requires:       systemd

%description
Bridges a native (host) Discord client's Rich Presence socket to the
special RPC path expected by Flatpak applications, so flatpaked games
show Rich Presence with your native Discord client. Socket-activated
via systemd user units; enabled globally for all users at install.

%prep
%setup -q -T -c -n %{name}-%{version}
# GitHub commit tarballs extract into "<repo>-<FULL 40-char hash>/",
# NOT the abbreviated hash — so never rely on the directory name;
# strip the leading component instead.
tar --strip-components=1 -xzf %{SOURCE0}

%install
install -Dpm 0644 discord-flatpak-rpc-bridge.service \
    %{buildroot}%{_prefix}/lib/systemd/user/discord-flatpak-rpc-bridge.service
install -Dpm 0644 discord-flatpak-rpc-bridge.socket \
    %{buildroot}%{_prefix}/lib/systemd/user/discord-flatpak-rpc-bridge.socket
# Ship the management script for per-user start/stop control (-e/-d).
install -Dpm 0755 install.sh \
    %{buildroot}%{_bindir}/discord-flatpak-rpc-bridge

%files
%license LICENSE
%{_prefix}/lib/systemd/user/discord-flatpak-rpc-bridge.service
%{_prefix}/lib/systemd/user/discord-flatpak-rpc-bridge.socket
%{_bindir}/discord-flatpak-rpc-bridge

%post
# Enable the socket for all users (mirrors upstream install.sh).
# The service starts automatically when the socket is first used.
systemctl --global enable discord-flatpak-rpc-bridge.socket || :

%postun
if [ $1 -eq 0 ]; then
    systemctl --global --no-warn disable \
        discord-flatpak-rpc-bridge.socket \
        discord-flatpak-rpc-bridge.service || :
fi

%changelog
* Sun Oct 25 2026 Noel Knubel - 1.0.0-2
- Robust %prep: GitHub commit tarballs extract into full-hash dirs.

* Sun Oct 25 2026 Noel Knubel - 1.0.0-1
- Initial package from upstream commit 621eec8.