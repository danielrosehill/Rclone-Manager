---
name: edit-mount
description: Change a persistent rclone mount - mountpoint, remote path, cache mode, read-only or other flags - by editing its systemd user unit and restarting it. Use on "change the cache mode on my mount", "move my mount".
---

# Edit a mount

Persistent mounts are systemd user services named `rclone-mount-<name>.service`
in `~/.config/systemd/user/` (see `add-mount`). A one-off mount can't be
edited: unmount it and mount it again with the new flags.

## 1. Show the current unit

```bash
systemctl --user cat rclone-mount-<name>
```

## 2. Edit

Copy the unit file to `<file>.bak`, then change the `ExecStart` line (and
`ExecStop` if the mountpoint moves). Common changes:

| Want | Flag |
|---|---|
| Better app compatibility | `--vfs-cache-mode writes` |
| Media / random reads | `--vfs-cache-mode full --vfs-cache-max-size 10G` |
| Read-only | `--read-only` |
| Fresher directory listings | `--dir-cache-time 1m` (Drive: also `--poll-interval 1m`) |
| Mount a subfolder | change the source to `<remote>:path` |

Look up any other flag with `rclone mount --help` or the `check-docs` skill.

If the mountpoint changes, create the new directory, and stop the service
before editing so the old mount is released.

## 3. Apply and verify

```bash
systemctl --user daemon-reload
systemctl --user restart rclone-mount-<name>
findmnt -t fuse.rclone | grep "<mountpoint>"
```

If the service fails, check `journalctl --user -u rclone-mount-<name> -n 30`
and restore the `.bak` file if needed.
