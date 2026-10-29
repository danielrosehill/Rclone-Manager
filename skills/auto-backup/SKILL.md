---
name: auto-backup
description: Set up automatic rclone.conf backups - a private git repo (created if missing), a local clone, and a systemd user timer, weekly by default or at the user's chosen frequency. Use on "back up my rclone config automatically".
---

# Automatic rclone config backups

The setup is:
- a private git repo, `rclone-config-backup` by default;
- a local clone at `${XDG_DATA_HOME:-~/.local/share}/rclone-manager/config-repo`;
- the `rclone-config-backup` script, copied to `~/.local/bin`;
- a systemd user timer that runs it.

Each machine writes to its own `<hostname>/` folder in the repo, so one repo
can back up several machines. A run commits only when the config has changed.

## 1. Ask

- **Frequency:** weekly by default. Others: `daily`, `monthly`, or any
  systemd `OnCalendar=` value such as `Mon *-*-* 09:00`.
- **Encryption:** the config contains live credentials. Offer to encrypt with
  `age` before it is committed (`RCLONE_BACKUP_AGE_TO=<age1 recipient>`). It
  needs `age` installed and the private key kept somewhere other than the
  repo. Without encryption the plain file is stored in a private repo. Before
  anything is pushed, tell the user in one sentence which of the two they are
  getting.
- **Repo host:** GitHub via `gh` by default. Any git remote URL works.

## 2. Repo: create if missing, then clone

```bash
RM="${CLAUDE_PLUGIN_ROOT:-$HOME/.local/share/rclone-manager/plugin}/scripts"
[ -f "$RM/merge_config.py" ] || git clone -q https://github.com/danielrosehill/Rclone-Manager "$HOME/.local/share/rclone-manager/plugin"
```

```bash
STORE="${XDG_DATA_HOME:-$HOME/.local/share}/rclone-manager/config-repo"
OWNER="$(gh api user --jq .login)"; REPO="$OWNER/rclone-config-backup"
gh repo view "$REPO" >/dev/null 2>&1 || gh repo create "$REPO" --private \
  --description "Automatic rclone.conf backups"
[ -d "$STORE/.git" ] || gh repo clone "$REPO" "$STORE"
gh repo view "$REPO" --json visibility --jq .visibility    # must say PRIVATE
```

If the repo already exists and is not private, stop and ask. Never push a
config to a public repo.

## 3. Install the script and settings

```bash
mkdir -p ~/.local/bin ~/.config/rclone-manager
install -m 755 "$RM/rclone-config-backup" ~/.local/bin/rclone-config-backup
cat > ~/.config/rclone-manager/backup.env <<ENV
RCLONE_BACKUP_REPO_DIR="$STORE"
RCLONE_CONFIG="$(rclone config file | tail -1)"
PATH="$(dirname "$(command -v rclone)"):$(dirname "$(command -v git)"):/usr/local/bin:/usr/bin:/bin"
# RCLONE_BACKUP_AGE_TO="age1..."
ENV
chmod 600 ~/.config/rclone-manager/backup.env
```

## 4. Timer

```bash
FREQ=weekly   # or what the user chose
mkdir -p ~/.config/systemd/user
cat > ~/.config/systemd/user/rclone-config-backup.service <<'UNIT'
[Unit]
Description=Back up rclone.conf to git

[Service]
Type=oneshot
ExecStart=%h/.local/bin/rclone-config-backup
UNIT
cat > ~/.config/systemd/user/rclone-config-backup.timer <<UNIT
[Unit]
Description=Back up rclone.conf ($FREQ)

[Timer]
OnCalendar=$FREQ
Persistent=true
RandomizedDelaySec=15m

[Install]
WantedBy=timers.target
UNIT
systemctl --user daemon-reload
systemctl --user enable --now rclone-config-backup.timer
```

`Persistent=true` runs a missed backup at the next login. On macOS, use a
launchd agent with `StartCalendarInterval` that runs the same script.

## 5. Verify with a real run

```bash
systemctl --user start rclone-config-backup.service
journalctl --user -u rclone-config-backup -n 20 --no-pager
git -C "$STORE" log --oneline -3
systemctl --user list-timers rclone-config-backup.timer --no-pager
```

The run must push successfully from the service, not just from your shell.
The service has no SSH agent, so use an HTTPS remote with `gh auth setup-git`
if an SSH push fails.

To change the frequency, edit `OnCalendar=` in the timer and run
`systemctl --user daemon-reload`. To stop the backups:
`systemctl --user disable --now rclone-config-backup.timer`.
