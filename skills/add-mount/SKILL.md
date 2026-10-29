---
name: add-mount
description: Mount an rclone remote as a local folder, one-off or persistent via a systemd user service that starts at login, with sensible VFS cache settings. Use on "mount my Google Drive", "mount S3 at boot".
---

# Add a mount

Needs FUSE (`check-setup`) and a working remote (`rclone lsd <remote>:`).

## 1. Decide

- **Source:** `<remote>:` or `<remote>:path/inside`.
- **Mountpoint:** default `~/mnt/<remote>`. It must be an empty directory.
- **Cache mode:** `--vfs-cache-mode writes` is the default to recommend,
  because without it many apps fail to save files. Use `full` for heavy
  read/seek work (media, editing in place), and `off` only for a read-only
  browse.
- **One-off or persistent.**

## 2a. One-off

```bash
mkdir -p ~/mnt/<remote>
rclone mount <remote>: ~/mnt/<remote> --vfs-cache-mode writes --daemon
```

It lasts until unmounted or reboot.

## 2b. Persistent (systemd user service, Linux)

The unit is named `rclone-mount-<remote>.service`. Other skills look for that
name. systemd does not expand `~` or set `HOME` reliably, so use absolute
paths. Check where rclone is with `command -v rclone`.

```bash
NAME=<remote>; SRC="<remote>:"; MNT="$HOME/mnt/$NAME"; RCLONE="$(command -v rclone)"
CONF="$(rclone config file | tail -1)"
mkdir -p "$MNT" ~/.config/systemd/user
cat > ~/.config/systemd/user/rclone-mount-$NAME.service <<UNIT
[Unit]
Description=rclone mount $SRC at $MNT
Wants=network-online.target
After=network-online.target

[Service]
Type=notify
ExecStart=$RCLONE mount $SRC $MNT --config $CONF --vfs-cache-mode writes --dir-cache-time 5m --log-level INFO
ExecStop=/bin/fusermount3 -uz $MNT
Restart=on-failure
RestartSec=10

[Install]
WantedBy=default.target
UNIT
systemctl --user daemon-reload
systemctl --user enable --now rclone-mount-$NAME.service
```

If only `fusermount` exists (FUSE 2), use `/bin/fusermount -uz` instead. To
keep the mount running when the user is logged out, run
`loginctl enable-linger "$USER"`. Ask before doing this.

`--allow-other` (other users can see the mount) also needs
`user_allow_other` in `/etc/fuse.conf`. Add it only if asked.

On macOS, use a launchd agent with the same `ExecStart` arguments, or run the
one-off form.

## 3. Verify

```bash
findmnt "$MNT"
ls "$MNT" | head
systemctl --user status rclone-mount-$NAME --no-pager | head -5   # persistent only
```
