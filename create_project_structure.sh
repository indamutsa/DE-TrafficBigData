#!/bin/bash

# Define project root directory
PROJECT_ROOT="./"

# Create directories
mkdir -p $PROJECT_ROOT/config
mkdir -p $PROJECT_ROOT/models
mkdir -p $PROJECT_ROOT/services
mkdir -p $PROJECT_ROOT/utilities

# Create __init__.py files for making Python packages
touch $PROJECT_ROOT/config/__init__.py
touch $PROJECT_ROOT/models/__init__.py
touch $PROJECT_ROOT/services/__init__.py
touch $PROJECT_ROOT/utilities/__init__.py

# Create specific Python files
touch $PROJECT_ROOT/config/settings.py
touch $PROJECT_ROOT/models/vehicle.py
touch $PROJECT_ROOT/services/data_generator.py
touch $PROJECT_ROOT/services/kafka_producer.py
touch $PROJECT_ROOT/utilities/coordinates.py

# Main application file
touch $PROJECT_ROOT/main.py
