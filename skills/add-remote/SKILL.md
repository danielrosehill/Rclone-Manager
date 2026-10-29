---
name: add-remote
description: Add an rclone remote (Google Drive, OneDrive, Dropbox, S3, R2, B2, Wasabi, SFTP, WebDAV, crypt and more) non-interactively, then verify it can list. Use on "add a drive to rclone", "connect rclone to S3".
---

# Add a remote

## 1. Gather

- **Name:** short, lowercase, no spaces. Check `rclone listremotes` so you
  don't overwrite an existing one.
- **Backend type:** `rclone help backends` lists them all. Backend options:
  `rclone help backend <type>`, or the `check-docs` skill.
- **Credentials:** keys, host, user, or an OAuth login in a browser.

## 2. Create

Use `rclone config create <name> <type> key=value ...`. Pass secrets as
arguments; rclone obscures password fields itself. Don't echo secrets back in
your reply.

**S3-compatible** (AWS, Cloudflare R2, Wasabi, MinIO, and others):

```bash
rclone config create r2 s3 provider=Cloudflare \
  access_key_id=... secret_access_key=... \
  endpoint=https://<account-id>.r2.cloudflarestorage.com acl=private
```

Other `provider=` values include `AWS`, `Wasabi`, `Minio`, `Backblaze`,
`DigitalOcean` and `Other`. Run `rclone help backend s3` for the full list
and for the endpoint and region each one needs.

**SFTP:**

```bash
rclone config create nas sftp host=nas.local user=me key_file=~/.ssh/id_ed25519
# or password: rclone config create nas sftp host=... user=... pass=... --obscure
```

**WebDAV:** `rclone config create dav webdav url=https://... vendor=nextcloud user=... pass=... --obscure`

**OAuth backends** (`drive`, `onedrive`, `dropbox`, `box`, `pcloud`, and
others):

```bash
rclone config create gdrive drive scope=drive
```

This opens a browser for consent. A Google Drive remote can take
`root_folder_id=` to start in a folder and `team_drive=` for a shared drive.
Recommend the user's own `client_id`/`client_secret`, because rclone's shared
Google client is heavily rate-limited (see `https://rclone.org/drive/#making-your-own-client-id`).

**Headless machine** (no browser): on any machine that has a browser and
rclone, run `rclone authorize "drive"` (or `onedrive`, `dropbox`, and so on).
Paste the token JSON it prints into the headless machine:

```bash
rclone config create gdrive drive scope=drive token='<json>' config_refresh_token=false
```

**crypt** (encrypts on top of another remote):

```bash
rclone config create secret crypt remote=r2:bucket/encrypted \
  password=... password2=... --obscure
```

Tell the user to keep both passwords somewhere safe. If they are lost, the
data can't be recovered.

If a create asks something unexpected, re-run it with `--all` for the full
question set, or run plain `rclone config` interactively.

## 3. Verify

```bash
rclone lsd <name>:                 # top-level listing
rclone about <name>: 2>/dev/null   # quota, where the backend supports it
```

A listing that comes back without errors confirms the remote. An empty
listing on a new bucket or drive is normal. Say which one happened.
