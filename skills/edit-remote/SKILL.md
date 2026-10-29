---
name: edit-remote
description: Edit an existing rclone remote - change options, reconnect an expired OAuth token, rename it, or change a password. Use on "update my rclone remote", "rclone token expired", "rename the remote".
---

# Edit a remote

Before any edit, back up the config:

```bash
CONF="$(rclone config file | tail -1)"; cp "$CONF" "$CONF.$(date +%Y%m%d-%H%M%S).bak"
```

## Change options

```bash
rclone config update <name> key=value [key=value ...]
# passwords: add --obscure
```

To remove an option, set it to an empty value (`key=`).

## Re-authorise (expired or revoked OAuth token)

```bash
rclone config reconnect <name>:
```

This opens the browser login again. On a headless machine, run
`rclone authorize "<type>"` where a browser is available, then
`rclone config update <name> token='<json>'`.

## Rename

rclone has no rename command. Recreate the remote under the new name, then
delete the old one:

1. `rclone config show <old>` and copy its key/value lines.
2. `rclone config create <new> <type> key=value ... --no-obscure`. The values
   are already obscured, so don't let rclone obscure them again.
3. Verify with `rclone lsd <new>:`, then `rclone config delete <old>`.
4. Update anything that referenced `<old>:`: mounts (see `list-mounts`), cron,
   scripts.

Or run `rclone config` interactively and use `r) Rename remote`.

## Verify

`rclone lsd <name>:` after every edit.
