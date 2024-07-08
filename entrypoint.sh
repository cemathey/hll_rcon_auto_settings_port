#!/usr/bin/env bash

set -e
set -x 

poetry run gunicorn -t 120 -b 0.0.0.0:8080 --chdir hll_rcon_auto_settings_port app:app