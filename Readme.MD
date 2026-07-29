# SculptBlender builds

Downloadable builds of **Blender with the SculptCore sculpt mode**.

Each package is a self-contained Blender — nothing is installed system-wide, and
every archive unpacks into a single folder you can delete to remove it. The
sculpt mode ships bundled and **enabled by default**, so there is no add-on to
turn on after the first launch.

> **Where are the files?**
> Binaries are published as **[GitHub Release](https://github.com/joeedh/sculptblender-builds/releases)
> assets**, not committed to this repository — cloning it stays cheap. This repo
> carries the docs plus a small JSON manifest per release under
> [`releases/`](./releases).
>
> - **[Latest build →](https://github.com/joeedh/sculptblender-builds/releases/latest)**
>   ([Linux](https://github.com/joeedh/sculptblender-builds/releases/latest/download/sculptblender-linux-x64.tar.gz)
>   · [macOS](https://github.com/joeedh/sculptblender-builds/releases/latest/download/sculptblender-macos-arm64.tar.gz)
>   · [Windows](https://github.com/joeedh/sculptblender-builds/releases/latest/download/sculptblender-windows-x64.zip))
> - **[All builds, with checksums →](./RELEASES.md)**

These are development builds of an in-progress project. They are unsigned and
unnotarized, they are not affiliated with or endorsed by the Blender Foundation,
and they can crash and lose work. Don't point one at a .blend you care about
without a backup.

---

## Installation

Pick the package for your platform. The download links always fetch the newest
build, so they are safe to bookmark or script:

| platform | file | download |
| --- | --- | --- |
| Linux x64 | `sculptblender-linux-x64.tar.gz` | [latest](https://github.com/joeedh/sculptblender-builds/releases/latest/download/sculptblender-linux-x64.tar.gz) |
| macOS (Apple silicon) | `sculptblender-macos-arm64.tar.gz` | [latest](https://github.com/joeedh/sculptblender-builds/releases/latest/download/sculptblender-macos-arm64.tar.gz) |
| Windows x64 | `sculptblender-windows-x64.zip` | [latest](https://github.com/joeedh/sculptblender-builds/releases/latest/download/sculptblender-windows-x64.zip) |

To pick a specific build instead, take it from that release's page or from
[RELEASES.md](./RELEASES.md). Older releases carry the build tag in the file
name as well (`sculptblender-<tag>-linux-x64.tar.gz`); newer ones do not, which
is what makes the always-latest links above possible.

Every package has a matching `.sha256` asset; verifying it is optional but
takes a second (commands below).

Each archive contains a single top-level folder named after the *build* —
`sculptblender-<tag>-<platform>/` — so you can extract it straight into your
Downloads folder without making a directory for it first, and two different
builds never overwrite each other.

### Windows x64

1. Download `sculptblender-windows-x64.zip`.
2. Right-click → **Properties** → tick **Unblock** → **OK**. (Windows marks
   downloaded archives, and the mark propagates to everything you extract.)
3. Extract it anywhere you like — your Desktop or `C:\` both work. It creates a
   `sculptblender-<tag>-windows-x64` folder. Avoid `C:\Program Files`; the
   folder needs to stay writable.
4. Run **`blender.exe`** from inside that folder.

SmartScreen may show *"Windows protected your PC"* the first time, because the
build is unsigned. Choose **More info → Run anyway** if you trust the source.

Verify the download (PowerShell, from the folder holding both files):

```powershell
Get-FileHash .\sculptblender-windows-x64.zip -Algorithm SHA256
# compare the hash against the contents of the matching .sha256 file
```

### Linux x64

```sh
tar -xzf sculptblender-linux-x64.tar.gz
cd sculptblender-*-linux-x64        # the folder, unlike the archive, carries the build tag
./blender
```

The tarball already carries the correct permissions, so no `chmod` is needed.
Built on Ubuntu 24.04 (glibc 2.39) — an older distro may be too old to run it.

If Blender fails to start with a message about a missing `libX*`/`libEGL`
library, install Blender's usual runtime dependencies, e.g. on Debian/Ubuntu:

```sh
sudo apt install libx11-6 libxi6 libxxf86vm1 libxcursor1 libxrandr2 \
                 libxinerama1 libxkbcommon0 libegl1 libgl1
```

Verify the download:

```sh
sha256sum -c sculptblender-linux-x64.tar.gz.sha256
```

### macOS (Apple silicon)

```sh
tar -xzf sculptblender-macos-arm64.tar.gz
cd sculptblender-*-macos-arm64      # the folder, unlike the archive, carries the build tag
xattr -dr com.apple.quarantine Blender.app     # required: the build is unsigned
open Blender.app
```

The `xattr` step is not optional. macOS quarantines anything downloaded from a
browser, and because this build carries no Developer ID signature, Gatekeeper
refuses it outright ("Blender is damaged and can't be opened") until the
quarantine flag is cleared. Only do this for downloads you trust.

These packages are **arm64 only** (M1 and later). There is no Intel build.

Verify the download:

```sh
shasum -a 256 -c sculptblender-macos-arm64.tar.gz.sha256
```

---

## Using the sculpt mode

Select a mesh object and pick **SculptCore Sculpt** from the object-mode
dropdown in the 3D viewport header — the same menu that holds Edit Mode and
Blender's own Sculpt Mode.

The mode is registered by the bundled `sculptcore_addon`, which the package
enables for you. It deliberately does not appear under
**Edit → Preferences → Add-ons** — there is nothing to switch on, and nothing
you can accidentally switch off. If the mode is missing from the dropdown, open
**Window → Toggle System Console** (Windows) or launch Blender from a terminal
to see why the native engine failed to load.

A package reads and writes the same Blender preferences as any other install on
the machine, so your themes, keymaps and paths carry over. The bundled sculpt
mode is not stored in those preferences — it is enabled by a marker file inside
the package — so deleting the folder removes the build and leaves your existing
Blender setup exactly as it was.

---

## What is in a package

- A portable build of the [Blender fork](https://github.com/joeedh/blender)
  branch `custom-object-modes`, which adds the engine-agnostic core support for
  Python-registered custom object modes.
- The [`sculptcore_addon`](https://github.com/joeedh/sculptcore-blender-addon)
  Python package, staged into `<version>/scripts/addons_core/`.
- The native **SculptCore engine** shared library, built with the addon's own
  brush kernels compiled in, vendored beside the addon.
- An `.always_enable` marker beside the add-on, which the fork reads at startup
  to turn the sculpt mode on without writing to your Blender preferences.

Packages are produced by the `Build packages` workflow in
[sculptcore-blender-addon](https://github.com/joeedh/sculptcore-blender-addon);
each release's manifest under [`releases/`](./releases) records the exact source
commit, fork branch and engine build config it came from.

## Repository layout

```
Readme.MD        this file
RELEASES.md      generated index of every release, with download links + checksums
releases/        one <tag>.json manifest per release (source commit, assets, checksums)
```

## License

Blender and this fork are [GPL-2.0-or-later](https://www.blender.org/about/license/);
the packages here are distributed under the same terms.
