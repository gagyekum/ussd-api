#!/bin/sh

set -e

# Format all files
black ussd_api/ tests/ setup.py

# Run test with coverage info
pytest --cov=ussd_api tests/
