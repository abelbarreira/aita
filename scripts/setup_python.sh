#!/bin/bash

# Script to set up local Python environment using pyenv and pipx

SCRIPT_DIR=$(dirname "$0")
ROOT_DIR="$SCRIPT_DIR/.."

PYTHON_VERSION="3.13.3"

pushd "$ROOT_DIR" > /dev/null

# Check for pyenv
if ! command -v pyenv &> /dev/null; then
  echo "❌ pyenv is not installed. Please install it first: https://github.com/pyenv/pyenv"
  exit 1
fi

echo "🐍 Setting Python version to $PYTHON_VERSION"
pyenv install -s "$PYTHON_VERSION"
pyenv local "$PYTHON_VERSION"

# Install pipx if not present
if ! command -v pipx &> /dev/null; then
  echo "🔧 Installing pipx..."
  python -m pip install --user pipx
else
  echo "✅ pipx already installed. Upgrading..."
  python -m pip install --upgrade --user pipx
fi

python -m pipx ensurepath

popd > /dev/null

echo "✅ Python environment setup complete."
