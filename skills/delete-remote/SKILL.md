---
name: delete-remote
description: Delete an rclone remote safely - back up rclone.conf, stop any mounts using it, remove it, and flag scripts that still reference it. Remote data is untouched. Use on "remove this rclone remote".
---

# Delete a remote

Deleting a remote removes its entry from `rclone.conf`. It does not delete
any files on the storage. Say that to the user, and get a yes naming the
remote before step 3.

## 1. Back up the config

```bash
CONF="$(rclone config file | tail -1)"; cp "$CONF" "$CONF.$(date +%Y%m%d-%H%M%S).bak"
```

## 2. Find what still uses it

```bash
findmnt -t fuse.rclone -o TARGET,SOURCE | grep "<name>:"
grep -l "<name>:" ~/.config/systemd/user/*.service 2>/dev/null
crontab -l 2>/dev/null | grep "<name>:"
grep -E "remote *= *<name>:" "$CONF"     # crypt/alias/union remotes layered on it
```

If any mount uses the remote, remove it first with the `remove-mount` skill.
For remotes layered on top of it, ask whether to delete them too.

## 3. Delete

```bash
rclone config delete <name>
rclone listremotes | grep -x "<name>:" || echo "removed"
```

For OAuth remotes, you can also revoke the app's access in the provider's
account settings. Mention this to the user; only they can do it.
