#!/usr/bin/env python3
"""Merge remotes from one rclone.conf into another, optionally rewriting path prefixes.

usage: merge_config.py SOURCE TARGET [--only a,b] [--replace] [--map OLD=NEW ...] [--write]

Without --write it only prints the plan. Existing target remotes are kept unless --replace.
--map rewrites any value starting with OLD (e.g. --map /home/alice=/home/bob, --map /Users/alice=/home/alice).
"""
import argparse, configparser, shutil, sys, time

def load(path):
    c = configparser.ConfigParser(interpolation=None)
    c.optionxform = str
    c.read(path)
    return c

ap = argparse.ArgumentParser()
ap.add_argument("source"); ap.add_argument("target")
ap.add_argument("--only", default="")
ap.add_argument("--replace", action="store_true")
ap.add_argument("--map", action="append", default=[])
ap.add_argument("--write", action="store_true")
a = ap.parse_args()

src, dst = load(a.source), load(a.target)
only = {n for n in a.only.split(",") if n}
maps = [m.split("=", 1) for m in a.map]

for name in src.sections():
    if only and name not in only:
        continue
    if dst.has_section(name) and not a.replace:
        print(f"skip     {name} (exists in target; --replace to overwrite)")
        continue
    action = "replace " if dst.has_section(name) else "add     "
    if dst.has_section(name):
        dst.remove_section(name)
    dst.add_section(name)
    for k, v in src.items(name):
        for old, new in maps:
            if v.startswith(old):
                print(f"         {name}.{k}: {v} -> {new + v[len(old):]}")
                v = new + v[len(old):]
        dst.set(name, k, v)
    print(f"{action}{name} ({src.get(name, 'type', fallback='?')})")

if a.write:
    shutil.copy2(a.target, f"{a.target}.{time.strftime('%Y%m%d-%H%M%S')}.bak")
    with open(a.target, "w") as f:
        dst.write(f)
    print(f"written: {a.target}")
else:
    print("dry run: add --write to apply", file=sys.stderr)
