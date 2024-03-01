#!/bin/bash

# Define the root directory of the project
PROJECT_ROOT="./"

# List of directories to create, relative to the project root
DIRECTORIES=(
    "config"
    "models"
    "services"
    "utilities"
    "tests"
    "tests/config"
    "tests/models"
    "tests/services"
    "tests/utilities"
)

# Create the project root directory if it doesn't exist
mkdir -p "$PROJECT_ROOT"

# Change to the project root directory
cd "$PROJECT_ROOT"

# Create directories and __init__.py files
for dir in "${DIRECTORIES[@]}"; do
    mkdir -p "$dir"  # Create the directory
    touch "$dir/__init__.py"  # Create an empty __init__.py file in it
done

# Create additional specific files
touch "services/test_data_generator.py"
touch "utilities/test_coordinates.py"
touch "tests/test_main.py"

# Provide feedback
echo "Project structure created in $PROJECT_ROOT."
