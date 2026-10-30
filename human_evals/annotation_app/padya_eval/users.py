# -*- coding: utf-8 -*-
"""
Per-annotator passwords: instance/users.json maps each allowed username to a password hash.

When the file exists, only the users in it can log in, each with their own password, and the shared
access code is not asked. Without the file, anyone can log in with a username (plus HE_ACCESS_CODE if set).

    .venv/bin/python -m padya_eval.users set shyam mahesh     # creates them (or resets them); prints the passwords
    .venv/bin/python -m padya_eval.users remove mahesh
    .venv/bin/python -m padya_eval.users list

The server reads the file at start-up: restart it after a change (systemctl --user restart padya-eval).
"""
from __future__ import annotations

import argparse
import json
import os
import secrets
import sys
from pathlib import Path

from werkzeug.security import check_password_hash, generate_password_hash

from .security import USERNAME_RE, normalise_username

APP_DIR = Path(__file__).resolve().parent.parent
PASSWORD_ALPHABET = "abcdefghjkmnpqrstuvwxyz23456789"     # no 0/o or 1/l/i: easy to read out and type on a phone


def users_path(instance: Path) -> Path:
    """HE_USERS_FILE, or instance/users.json."""
    return Path(os.environ.get("HE_USERS_FILE", instance / "users.json"))


def load_users(path: Path) -> dict[str, str] | None:
    """username -> password hash, or None when there is no users file (open login)."""
    if not path.is_file():
        return None
    return json.loads(path.read_text(encoding="utf-8"))


def save_users(path: Path, users: dict[str, str]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    tmp = path.with_suffix(".tmp")
    tmp.write_text(json.dumps(users, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    tmp.chmod(0o600)
    tmp.replace(path)


def new_password() -> str:
    """Twelve characters in three groups, e.g. 'k7mx-q9pt-4nar' (about 59 bits)."""
    return "-".join("".join(secrets.choice(PASSWORD_ALPHABET) for _ in range(4)) for _ in range(3))


def hash_password(password: str) -> str:
    return generate_password_hash(password)


def check_password(users: dict[str, str], username: str, password: str) -> bool:
    hashed = users.get(username)
    return hashed is not None and check_password_hash(hashed, password)


def main(argv: list[str] | None = None) -> int:
    instance = Path(os.environ.get("HE_INSTANCE_DIR", APP_DIR / "instance"))
    ap = argparse.ArgumentParser(prog="python -m padya_eval.users", description="Manage annotator passwords.")
    ap.add_argument("--file", type=Path, default=users_path(instance), help="users file (default: %(default)s)")
    sub = ap.add_subparsers(dest="command", required=True)
    p_set = sub.add_parser("set", help="create users, or give existing ones a new password; prints the passwords")
    p_set.add_argument("usernames", nargs="+")
    p_rm = sub.add_parser("remove", help="remove users (their ratings stay in the database)")
    p_rm.add_argument("usernames", nargs="+")
    sub.add_parser("list", help="list the users")
    args = ap.parse_args(argv)

    users = load_users(args.file) or {}
    if args.command == "list":
        print("\n".join(sorted(users)) if users else f"no users in {args.file}: login is open")
        return 0

    names = [normalise_username(u) for u in args.usernames]
    bad = [u for u in names if not USERNAME_RE.match(u)]
    if bad:
        print(f"not a valid username (2-40 letters, digits, '.', '-' or '_'): {', '.join(bad)}", file=sys.stderr)
        return 2
    if args.command == "remove":
        missing = [u for u in names if u not in users]
        if missing:
            print(f"no such user: {', '.join(missing)}", file=sys.stderr)
            return 1
        for u in names:
            del users[u]
        save_users(args.file, users)
        print(f"removed {', '.join(names)}; restart the server to apply")
        return 0

    width = max(len(u) for u in names)
    for u in names:
        password = new_password()
        users[u] = hash_password(password)
        print(f"{u:<{width}}  {password}")
    save_users(args.file, users)
    print(f"(saved to {args.file}; restart the server to apply)", file=sys.stderr)
    return 0


if __name__ == "__main__":
    sys.exit(main())
