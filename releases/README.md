# Release manifests

One `<tag>.json` per package release, written by the `Build packages` workflow
in [sculptcore-blender-addon](https://github.com/joeedh/sculptcore-blender-addon)
(`tools/record-release.mjs`). Each records what was built, from which source
commit, and the SHA-256 of every published asset. The assets themselves live on
the [releases page](https://github.com/joeedh/sculptblender-builds/releases) —
never in this repo.

`../RELEASES.md` is generated from these files; edit neither by hand.
