#!/bin/bash
# (c) J~Net 2026
#
# ./setup.sh
#
#
#
python -m venv venv
source venv/bin/activate
pip install --upgrade pip
pip install pillow
pip install html5lib

echo "Pillow installed"

echo ""
echo "Now run with ./start.sh"
