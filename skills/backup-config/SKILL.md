---
name: backup-config
description: Back up rclone.conf now, as a timestamped local copy or an age-encrypted copy, or as a commit to the git backup repo if auto-backup is set up. Restore from a backup. Use on "back up my rclone config", "restore rclone config".
---

# Back up the rclone config

rclone.conf holds every remote's credentials and tokens. Anyone who gets the
file gets access to those accounts.

## One-off local backup

```bash
CONF="$(rclone config file | tail -1)"
DEST="${XDG_DATA_HOME:-$HOME/.local/share}/rclone-manager/backups"
mkdir -p "$DEST" && chmod 700 "$DEST"
cp "$CONF" "$DEST/rclone.conf.$(hostname -s).$(date +%Y%m%d-%H%M%S)"
```

Encrypted copy, if the user has `age` and a recipient key:
`age -r <age1...> -o "$DEST/rclone.conf.$(date +%Y%m%d-%H%M%S).age" "$CONF"`.

To protect the live config with a password as well:
`rclone config encryption set`. After that, every rclone run, and any mount
or timer, needs `RCLONE_CONFIG_PASS` or `--password-command`. Say so before
the user turns it on.

## Into the git backup repo

If `auto-backup` has been set up (`~/.config/rclone-manager/backup.env`
exists), run a backup now:

```bash
RM="${CLAUDE_PLUGIN_ROOT:-$HOME/.local/share/rclone-manager/plugin}/scripts"
[ -f "$RM/merge_config.py" ] || git clone -q https://github.com/danielrosehill/Rclone-Manager "$HOME/.local/share/rclone-manager/plugin"
```

```bash
"$RM/rclone-config-backup"
```

## Restore

1. Back up the current config first, using the steps above.
2. Copy the backup over `$(rclone config file | tail -1)`. For an age file,
   use `age -d -i <keyfile> -o <config> <file>.age`. To bring back only some
   remotes, use `migrate-config`'s merge instead of copying the whole file.
3. Run `rclone listremotes`, then `rclone lsd <remote>:` on one of them.
