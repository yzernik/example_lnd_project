#!/usr/bin/env bash

# exit from script if error was raised.
set -e

# Sleep for 10 seconds
sleep 5

exec python -m src.app
