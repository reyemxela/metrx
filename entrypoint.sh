#!/bin/sh

set -eu

if [ -f '/app/modules/custom/requirements.txt' ]; then
  pip install --no-cache --disable-pip-version-check -q -r /app/modules/custom/requirements.txt
fi

exec python3 /app/metrx.py "$@"