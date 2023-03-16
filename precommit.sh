#!/bin/bash
# Cleanup repo before commit by running black and isort over all python files

# Run formatters 
python -m black .
python -m isort .

