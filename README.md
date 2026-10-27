# skare1412-personal-copr

Spec sheets and helper scripts for my personal COPR, designed for
low-maintenance packaging: prefer sources and release artifacts
officially supported by upstream developers.

## Packages

| Package | Upstream | Source | Update procedure |
| ------- | -------- | ------ | ---------------- |
| discord-flatpak-rpc-bridge | [Arcitec/discord-flatpak-rpc-bridge](https://github.com/Arcitec/discord-flatpak-rpc-bridge) | git snapshot tarball, built from source | bump snapshot |
| euro-office | [Euro-Office/DesktopEditors](https://github.com/Euro-Office/DesktopEditors) | repack of official upstream rpm | bump version, refresh sha256 comment |
| heroic | [HeroicGamesLauncher](https://github.com/Heroic-Games-Launcher/HeroicGamesLauncher) | repack of official upstream rpm | bump version, refresh sha256 comment |
| msttcore-fonts-installer | [isboston/msttcore-fonts](https://github.com/isboston/msttcore-fonts) | repack of official upstream noarch rpm | bump version |
| nextcloud-office | [nextcloud-releases/Office-DesktopEditors](https://github.com/nextcloud-releases/Office-DesktopEditors) | repack of official upstream rpm | bump version |
| autohdr-vk | private | local tarball via `make-local-tarball.sh`, SRPM uploaded with copr-cli | re-run script, bump version |
| pyrofling | [Themaister/pyrofling](https://github.com/Themaister/pyrofling) | local tarball via `make-pyrofling-tarball.sh` (snapshot, no upstream tags) | re-run script with new date, update Version |
| volt-gui | [pythonlover02/volt-gui](https://github.com/pythonlover02/volt-gui) | repack of official release tarball (prebuilt, container-built) | bump version, refresh sha256 comment |
| vksumi | [reakjra/vkSumi](https://github.com/reakjra/vkSumi) | upstream git tag tarball, spec based on upstream's own `packaging/vksumi.spec` | bump version, refresh sha256 comment |

## Notes

- Packages whose source cannot be fetched by copr (private repos,
  git submodules, local checkouts) are built as SRPMs locally and
  uploaded with `copr-cli build <project> <srpm>`.
- Most repack specs carry a `sha256(Source0) = ...` comment near
  Source0; refresh it with `sha256sum` whenever Source0 changes.
- Vulkan layer packages (pyrofling, volt-gui, vksumi, autohdr-vk)
  install implicit-layer manifests into
  `%{_datadir}/vulkan/implicit_layer.d`; the layers stay dormant
  unless their enable environment variable is set
  (`PYROFLING=1`, `VOLT_ENABLE` via the volt launcher,
  `ENABLE_VKSUMI=1`).

## copr-packaging/scripts

- `make-local-tarball.sh <repo-path> <name> <version>` — turn a
  local/private git checkout into a Source0 tarball (git archive,
  no submodules).
- `make-pyrofling-tarball.sh [YYYYMMDD]` — vendor a pyrofling
  snapshot with the Granite submodule tree (FFmpeg submodule
  skipped: on Linux Granite links system ffmpeg-free).
