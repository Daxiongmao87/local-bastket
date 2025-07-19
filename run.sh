#!/bin/bash

# Step a: Install dependencies
pip install -r requirements.txt

# Step b: Run all necessary parts of the codebase in parallel
python src/main.py &
pytest tests/ &

wait
