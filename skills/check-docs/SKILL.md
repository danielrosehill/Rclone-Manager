---
name: check-docs
description: Look up the official rclone documentation for a backend, command or flag, matched to the installed version, before guessing. Use on "how do I configure X in rclone", "what does this rclone flag do".
---

# Check the rclone docs

Answer from the docs, not from memory. rclone flags and backend options change
between releases.

## 1. Local help (matches the installed version, works offline)

```bash
rclone version | head -1
rclone help backends                  # all backend types
rclone help backend <type>            # every option for one backend, e.g. drive, s3, sftp
rclone <command> --help               # e.g. rclone mount --help, rclone sync --help
rclone help flags <filter>            # global flags matching a word, e.g. vfs, transfers
rclone config providers | jq '.[] | select(.Name=="<type>")'   # options as JSON
```

## 2. Website (latest release; may be newer than the install)

| Topic | URL |
|---|---|
| Backend page | `https://rclone.org/<type>/` (e.g. `/drive/`, `/s3/`, `/sftp/`) |
| Command page | `https://rclone.org/commands/rclone_<cmd>/` (e.g. `rclone_mount`) |
| Global flags | `https://rclone.org/flags/` |
| Filtering | `https://rclone.org/filtering/` |
| Changelog | `https://rclone.org/changelog/` |
| Forum (known issues) | `https://forum.rclone.org/` |

Fetch the page and quote the relevant part. If the website describes a flag
that local help doesn't show, the install is older than the docs. Check the
changelog and suggest updating (`check-setup`).

## 3. Answer

Cite the source (local help for version X, or a rclone.org URL) and give the
exact command.
