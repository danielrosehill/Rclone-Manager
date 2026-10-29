---
name: check-setup
description: Check an rclone install - version and whether it is current, config file path, configured remotes, FUSE for mounts - then hand off to install-rclone if needed. Use before other rclone work or on "is rclone set up", "update rclone".
---

# Check the rclone setup

Run these and report what they show:

```bash
rclone version                 # installed version, OS, arch
rclone version --check         # online check against the latest release
rclone config file             # where rclone.conf lives
rclone listremotes --long      # configured remotes and their types
command -v fusermount3 || command -v fusermount   # needed for mounts on Linux
```

On macOS, mounts need macFUSE or FUSE-T instead of fusermount.

## If something is missing

If rclone is missing or out of date, or FUSE is missing, use the `install-rclone` skill.

## Report

Give the version, whether an update exists, the config path, the remote count
by type, and whether mounts will work. Don't print the config contents. If you
need to show them, use `rclone config redacted`, which masks secrets.
