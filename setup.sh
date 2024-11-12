#!/bin/bash

# Create directory structure
mkdir -p models/engine
mkdir -p tests/test_models/test_engine

# Create and set permissions for models package
touch models/__init__.py
chmod +x models/__init__.py

# Create and set permissions for engine package
touch models/engine/__init__.py
chmod +x models/engine/__init__.py

# Create and set permissions for file_storage.py
touch models/engine/file_storage.py
chmod +x models/engine/file_storage.py

# Create and set permissions for base_model.py
touch models/base_model.py
chmod +x models/base_model.py

# Create test directories
touch tests/__init__.py
touch tests/test_models/__init__.py
touch tests/test_models/test_engine/__init__.py

# Set permissions for test files
chmod +x tests/__init__.py
chmod +x tests/test_models/__init__.py
chmod +x tests/test_models/test_engine/__init__.py
