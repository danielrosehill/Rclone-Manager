---
name: install-rclone
description: Install rclone if it is missing, or update an old one, using the official installer, a package manager or selfupdate, plus FUSE for mounts. Use on "install rclone", "rclone not found", "update rclone".
---

# Install or update rclone

## 1. What's there now

```bash
command -v rclone && rclone version | head -1 && rclone version --check
```

The `rclone version --check` line shows the latest release. Distro packages
often lag well behind it.

## 2. Install

Show the user the command and get a yes before running anything with sudo.

| Situation | Command |
|---|---|
| Linux/macOS, latest release (recommended) | `sudo -v && curl -fsSL https://rclone.org/install.sh \| sudo bash` |
| Debian/Ubuntu package (may be old) | `sudo apt install rclone` |
| Fedora | `sudo dnf install rclone` |
| Arch | `sudo pacman -S rclone` |
| macOS Homebrew | `brew install rclone` (Homebrew's build can't mount, so use the official binary for mounts) |
| No sudo | download the zip from `https://rclone.org/downloads/` and put `rclone` in `~/.local/bin` |

## 3. Update

- Installed with the official installer or binary: `sudo rclone selfupdate`
  (`--beta` for beta builds).
- Installed from a package manager: update with that package manager. Don't
  run selfupdate over a package-managed binary.
- If both are present (`which -a rclone`), say which one runs first on `PATH`.

## 4. FUSE (only needed for mounts)

- Debian/Ubuntu: `sudo apt install fuse3`. Fedora: `sudo dnf install fuse3`.
- macOS: macFUSE (`brew install --cask macfuse`) or FUSE-T.

## 5. Verify

`rclone version` reports the new version, and `rclone listremotes` runs
without error. If there are no remotes yet, offer `add-remote`, or
`migrate-config` to bring settings over from another machine.
