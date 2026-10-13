#!/usr/bin/env bash
# Local server: http://127.0.0.1:5000  (admin: /admin, password "admin" unless HE_ADMIN_PASSWORD is set)
# HE_DEBUG=1 ./run.sh turns on auto-reload and the debugger (only on your own machine).
set -euo pipefail
cd "$(dirname "$0")"
if [ ! -x .venv/bin/python ]; then
  python3 -m venv .venv
  .venv/bin/pip install -q -r requirements.txt
fi
export HE_ADMIN_PASSWORD="${HE_ADMIN_PASSWORD:-admin}"
if [ "${HE_DEBUG:-0}" = "1" ]; then
  exec .venv/bin/flask --app wsgi run --debug "$@"
fi
exec .venv/bin/flask --app wsgi run "$@"
