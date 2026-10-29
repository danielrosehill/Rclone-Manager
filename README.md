# Rclone Manager

Agent skills for routine [rclone](https://rclone.org) admin: installing it, managing remotes and mounts, backing up the config and moving it between machines, and looking things up in the official docs. Each skill covers one job and runs plain `rclone`, `systemd` and `git` commands, so it works in any agent that can read a SKILL.md and run a shell.

## Skills

| Skill | Does |
|---|---|
| `check-setup` | Version, update check, config path, remotes, FUSE readiness |
| `install-rclone` | Install or update rclone (official installer, package manager, selfupdate) and FUSE |
| `add-remote` | Non-interactive `rclone config create` for Drive, OneDrive, Dropbox, S3/R2/B2/Wasabi, SFTP, WebDAV, crypt; headless OAuth |
| `list-remotes` | Remotes with type, redacted settings, quota, account, connect check |
| `edit-remote` | Change options, reconnect expired OAuth, rename, change passwords |
| `delete-remote` | Back up config, clear dependent mounts, delete, flag leftover references |
| `add-mount` | One-off mount or persistent `rclone-mount-<name>.service` systemd user unit |
| `list-mounts` | Active mounts and services, stale/failed mount diagnosis |
| `edit-mount` | Change cache mode, mountpoint, flags of a persistent mount |
| `remove-mount` | Unmount, disable and delete the service |
| `backup-config` | One-off timestamped or age-encrypted backup; restore |
| `auto-backup` | Private git repo (created if missing) + local clone + systemd timer, weekly by default |
| `migrate-config` | Copy remotes to another machine, merged without clobbering, paths rewritten |
| `check-docs` | Answer from local `rclone help` and rclone.org for the installed version |

## Scripts

- `scripts/rclone-config-backup`: copies `rclone.conf` into `<repo>/<hostname>/` (optionally `age`-encrypted), then commits and pushes only if it changed. Settings are read from `~/.config/rclone-manager/backup.env`.
- `scripts/merge_config.py`: merges remotes from one `rclone.conf` into another, with `--only`, `--replace` and `--map OLD=NEW` path rewriting. It is a dry run unless you pass `--write`.

## Install

```bash
claude plugins marketplace add danielrosehill/Claude-Code-Plugins
claude plugins install rclone-manager@danielrosehill
```

Other agents: clone this repo and point the agent at `skills/`.

## Prior art (checked 2026-10-29)

Before this, the rclone agent skills were single-file transfer helpers (ratacat/claude-skills, major-ai-skills, carbonscott/rclone-skills, louiz3040-cloud/rclone-skill, EveryInc compound-engineering) and MCP servers over the rclone RC API (rclone-ui/rclone-mcp, PhateValleyman/rclone-mcp). None covered the remote, mount and config lifecycle as separate skills. Use rclone-mcp alongside this plugin if you want the RC API.

## Platform

Built and tested on Linux (Ubuntu 26.04, rclone 1.72.1). Mount and timer steps use systemd user units. macOS notes are included, but those steps are untested.

## License

MIT
