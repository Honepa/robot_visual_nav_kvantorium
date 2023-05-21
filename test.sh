#!/bin/bash
# Test services script

. ./venv/bin/activate
export FLASK_APP='web'
flask run --host '0.0.0.0' --port 5005 --no-debug

echo "Running!"
