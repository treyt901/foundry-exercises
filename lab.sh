#!/usr/bin/env bash
# Start / restart / stop the Foundry Prompt Lab for students.
#
# Flask runs in the background and all of its technical output goes to
# .flask.log, so students only see a couple of friendly status lines.
#
#   bash lab.sh start     # start it (does nothing if already running)
#   bash lab.sh restart   # apply prompt/config edits: stop, then start
#   bash lab.sh stop      # stop it
#   bash lab.sh status    # is it running?

cd "$(dirname "$0")"

PORT="${PORT:-5000}"
PIDFILE=".flask.pid"
LOGFILE=".flask.log"
DEPSLOCK=".pip.lock"

# --- Find the Python to use (needs 3.8+ for the Azure OpenAI SDK) -----------
# Prefer an interpreter that ALREADY has the dependencies (the one the stack
# was built with), so a box with several Python versions can't pick a wrong,
# empty one. Only if none have the deps do we fall back to the newest 3.8+,
# which is where they'll be installed.
CANDIDATES="python3.12 python3.11 python3.10 python3.9 python3.8 python3"

py_ok() {
  command -v "$1" >/dev/null 2>&1 &&
    "$1" -c 'import sys; sys.exit(0 if sys.version_info[:2] >= (3, 8) else 1)' 2>/dev/null
}

pick_python() {
  for c in $CANDIDATES; do
    py_ok "$c" && "$c" -c 'import flask, openai, dotenv' >/dev/null 2>&1 && { echo "$c"; return 0; }
  done
  for c in $CANDIDATES; do
    py_ok "$c" && { echo "$c"; return 0; }
  done
  return 1
}
PY="$(pick_python || true)"

# --- Small helpers ---------------------------------------------------------
port_open() {
  "${PY:-python3}" -c "import urllib.request; urllib.request.urlopen('http://localhost:${PORT}/', timeout=2)" \
    >/dev/null 2>&1
}

is_running() {
  { [ -f "$PIDFILE" ] && kill -0 "$(cat "$PIDFILE" 2>/dev/null)" 2>/dev/null; } || port_open
}

wait_ready() {
  for _ in $(seq 1 40); do
    port_open && return 0
    sleep 1
  done
  return 1
}

stop_app() {
  [ -f "$PIDFILE" ] && kill "$(cat "$PIDFILE" 2>/dev/null)" 2>/dev/null
  rm -f "$PIDFILE"
  # Belt and suspenders: clear any stray instance so the port is free.
  pkill -f "app.py" 2>/dev/null
  # Wait (up to ~8s) for the port to actually free up before restarting.
  for _ in $(seq 1 8); do
    port_open || return 0
    sleep 1
  done
}

# --- Main actions ----------------------------------------------------------
require_python() {
  if [ -z "$PY" ]; then
    echo "❌ Python 3.8+ was not found on this box. This is an instructor setup"
    echo "   issue — see INSTRUCTOR_SETUP.md."
    return 1
  fi
}

deps_present() {
  "$PY" -c "import flask, openai, dotenv" >/dev/null 2>&1
}

ensure_deps() {
  # Install dependencies quietly, and only if they aren't already present.
  # The install is serialized with flock: the setup guide page starts it in a
  # terminal when it opens (bash lab.sh prepare), and guide BUTTONS run with a
  # short timeout Codio doesn't let us extend — so if an install is already
  # running elsewhere, a button politely says "wait" instead of colliding
  # with it or being killed mid-install.
  deps_present && return 0
  if command -v flock >/dev/null 2>&1; then
    echo "⏳ Preparing the app (first run only)…"
    flock -n -E 200 "$DEPSLOCK" "$PY" -m pip install -q -r requirements.txt >>"$LOGFILE" 2>&1
    status=$?
    if [ "$status" -eq 200 ]; then
      echo "⏳ The app's tools are still being installed (see the setup page's"
      echo "   terminal). Give it a minute, then try again."
      return 1
    fi
  else
    echo "⏳ Preparing the app (first run only)…"
    "$PY" -m pip install -q -r requirements.txt >>"$LOGFILE" 2>&1
  fi
  if ! deps_present; then
    echo "❌ Could not install dependencies. See .flask.log for details."
    return 1
  fi
}

start_app() {
  if is_running; then
    echo "ℹ️  The Prompt Lab is already running. Use Restart to apply changes."
    return 0
  fi

  require_python || return 1

  if [ ! -f .env ]; then
    echo "⚠️  The .env file is missing — it ships with the assignment. Ask your"
    echo "   instructor for help (or restore it from the original project)."
  fi

  ensure_deps || return 1

  echo "⏳ Starting the Prompt Lab…"
  # Run in the background; hide all of Flask's output in the log file.
  nohup "$PY" app.py >"$LOGFILE" 2>&1 &
  echo $! >"$PIDFILE"

  if wait_ready; then
    echo "✅ Prompt Lab is running. Open the \"Prompt Lab\" tab to use it."
    echo "   (If the tab is already open, click its refresh icon.)"
  else
    echo "❌ The app didn't start. See .flask.log for details."
    return 1
  fi
}

# Normalize the action: guide buttons and terminals can sneak in stray
# whitespace or carriage returns around the argument.
ACTION="$(printf '%s' "${1:-start}" | tr -d '[:space:]')"
[ -n "$ACTION" ] || ACTION="start"

case "$ACTION" in
  start)
    start_app
    ;;
  restart)
    echo "🔄 Restarting the Prompt Lab…"
    stop_app
    start_app
    ;;
  stop)
    stop_app
    echo "🛑 Prompt Lab stopped."
    ;;
  status)
    if is_running; then
      echo "✅ The Prompt Lab is running."
    else
      echo "⚪ The Prompt Lab is not running."
    fi
    ;;
  test)
    # One-shot check that the student's .env actually reaches their deployment.
    require_python && ensure_deps && "$PY" test_connection.py
    ;;
  prepare)
    # Install the app's tools ahead of time. The setup guide page runs this in
    # a terminal when it opens, so the slow first-time install happens while
    # the student fills in .env — not inside a guide button's timeout window.
    if require_python; then
      if deps_present; then
        echo "✅ The app's tools are already installed — you're all set."
      elif ensure_deps; then
        echo "✅ Setup finished. Fill in your .env, then press \"Test my connection\"."
      fi
    fi
    ;;
  *)
    echo "Usage: bash lab.sh [start|restart|stop|status|test|prepare]  (got: '$ACTION')"
    exit 1
    ;;
esac
