---
name: migrate-config
description: Copy rclone remotes from one machine to another - whole config or picked remotes, merged without clobbering, with home/key-file paths rewritten for the new machine. Use on "copy my rclone setup to my other computer".
---

# Migrate rclone config between machines

```bash
RM="${CLAUDE_PLUGIN_ROOT:-$HOME/.local/share/rclone-manager/plugin}/scripts"
[ -f "$RM/merge_config.py" ] || git clone -q https://github.com/danielrosehill/Rclone-Manager "$HOME/.local/share/rclone-manager/plugin"
```

## 1. Get the source config onto this machine

Use any one of these:
- Over SSH: `ssh <host> 'cat "$(rclone config file | tail -1)"' > /tmp/rclone.src.conf`
- From the `auto-backup` repo: `git -C <store> pull`, then use
  `<store>/<source-host>/rclone.conf` (for `.age`, run `age -d -i <key>` first)
- From a file the user supplies

Set `chmod 600` on the copy and delete it when you are done.

## 2. Preview the merge

```bash
TARGET="$(rclone config file | tail -1)"; touch "$TARGET"
python3 -I "$RM/merge_config.py" /tmp/rclone.src.conf "$TARGET" \
  --map /home/<olduser>=/home/<newuser>     # repeat --map for each prefix to rewrite
# --only a,b      just these remotes
# --replace       overwrite remotes that already exist on the target
```

The script makes no changes until `--write` is added. Find paths to rewrite
with `grep -nE '= */|= *~|[A-Z]:\\' /tmp/rclone.src.conf`. Typical ones:
- `key_file`, `pubkey_file`, `known_hosts_file` (SFTP);
- `service_account_file` (Drive/GCS);
- `local` and `alias` remotes pointing at local folders;
- macOS `/Users/x` to Linux `/home/x`.

Check that each rewritten path exists on this machine. Key files themselves
are not copied, so tell the user which ones they need to bring across.

Show the plan, get a yes, then run it again with `--write`. The script saves
a `.bak` of the target first. It drops comments in the target file.

## 3. Check each migrated remote

```bash
for r in <migrated remotes>; do timeout 30 rclone lsd "$r:" >/dev/null && echo "OK $r" || echo "FAIL $r"; done
```

- **Shared OAuth tokens:** some providers (OneDrive, Box, and others) rotate
  refresh tokens. With the same token on two machines, one of them will
  eventually fail with `invalid_grant`. Run `rclone config reconnect <r>:`
  on the new machine so it has its own token (`edit-remote`).
- **An encrypted source config** (`rclone config encryption`) needs its
  password, set in `RCLONE_CONFIG_PASS`, to read it.

## 4. Mounts

Mounts are not part of rclone.conf. List the source machine's mounts with
`ssh <host> 'ls ~/.config/systemd/user/rclone-mount-*.service'`, then
recreate each one here with `add-mount`.
