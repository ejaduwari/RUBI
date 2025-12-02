#!/bin/bash

# Navigate to project directory
cd /home/rubipi/pixy2/src/host/libpixyusb2_examples/rubi || exit

# Activate virtual environment
source venv/bin/activate

# Run Flask app
python3 app.py
