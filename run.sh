#!/usr/bin/env bash
# Backwards-compatible entry point. The real logic lives in lab.sh so the app
# can be started and restarted cleanly. This just starts it.
exec bash "$(dirname "$0")/lab.sh" start
