---
name: list-mounts
description: List active rclone mounts and persistent mount services, their state, cache mode, and any stale or failed mounts. Use on "what's mounted with rclone", "is my drive mount running", "transport endpoint is not connected".
---

# List mounts

```bash
findmnt -t fuse.rclone -o TARGET,SOURCE,OPTIONS             # active mounts
systemctl --user list-units --all 'rclone-mount-*' --no-pager   # services (any state)
ls ~/.config/systemd/user/rclone-mount-*.service 2>/dev/null
pgrep -af "rclone mount"                                    # incl. one-off --daemon mounts
```

Read each unit's `ExecStart` line for its source, mountpoint and flags:
`systemctl --user cat rclone-mount-<name>`.

Report a table: source, mountpoint, persistent or one-off, state, cache mode.

## Problems to flag

- **`Transport endpoint is not connected`** on `ls`: the rclone process died
  and left the mount behind. Clear it with `fusermount3 -uz <mountpoint>`,
  then `systemctl --user restart rclone-mount-<name>` or mount again.
- **Service `failed`:** `journalctl --user -u rclone-mount-<name> -n 50 --no-pager`.
  Common causes: an expired token (`edit-remote` reconnect), a mountpoint that
  isn't empty, or a renamed or deleted remote.
- **A service that points at a remote missing from `rclone listremotes`.**
