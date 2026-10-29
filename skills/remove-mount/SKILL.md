---
name: remove-mount
description: Unmount an rclone mount and, for persistent ones, stop, disable and delete its systemd user service, leaving the remote and its data alone. Use on "unmount my drive", "stop mounting this at login".
---

# Remove a mount

This only removes the local mount. The remote and the files on it are not
touched.

## 1. Unmount

```bash
systemctl --user stop rclone-mount-<name> 2>/dev/null   # persistent
fusermount3 -u <mountpoint> || fusermount3 -uz <mountpoint>   # one-off, or if still mounted
```

`-u` fails with "device busy" while a shell or app is open inside the
mountpoint. Find what is using it with `lsof +f -- <mountpoint>`, ask the
user to close it, or use `-uz` (lazy unmount).

Uploads still queued in the VFS cache are lost if you kill the process
mid-upload. Check `journalctl --user -u rclone-mount-<name> -n 20` for
pending uploads before forcing anything.

## 2. Remove the service (persistent only)

```bash
systemctl --user disable rclone-mount-<name>
rm ~/.config/systemd/user/rclone-mount-<name>.service
systemctl --user daemon-reload
```

## 3. Clean up and verify

```bash
findmnt <mountpoint> || echo "unmounted"
rmdir <mountpoint>        # only if empty; never rm -r a mountpoint
```
