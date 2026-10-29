---
name: list-remotes
description: List rclone remotes with type, settings (secrets redacted), quota, logged-in account and whether each still connects. Use on "what rclone remotes do I have", "is my drive remote still working".
---

# List and inspect remotes

```bash
rclone listremotes --long            # name and type; add --json for machine use
rclone config show <name>            # one remote's settings: shows secrets
rclone config redacted <name>        # same, with secrets masked; prefer this
```

Only show `rclone config redacted` output to the user unless they ask for the
raw values.

## Health check, per remote

```bash
timeout 30 rclone lsd <name>: --max-depth 1 >/dev/null && echo OK
rclone about <name>:          # used/free/total, if the backend supports it
rclone config userinfo <name>:   # account it is logged in as (OAuth backends)
```

Run the checks in parallel for many remotes, each with a timeout. Report a
table: name, type, connects (yes/no plus the error), quota, account.

A failure with `invalid_grant` or `token expired` means the OAuth token has
lapsed. Fix it with the `edit-remote` skill (reconnect).
