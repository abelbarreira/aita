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

# Needed to export `pipx` path on this script run
export PATH="$PATH:/home/abr/.local/bin"

# Install or upgrade Hatch using pipx
if ! command -v hatch &> /dev/null; then
  echo "🔧 Installing Hatch via pipx..."
  pipx install hatch
else
  echo "✅ Hatch already installed. Upgrading..."
  pipx upgrade hatch
fi

echo "🔎 Ensuring Hatch environment is created/updated with dependencies from pyproject.toml..."
hatch env create

echo
echo "🚀 Generating VSCode Settings.."

hatch run set-vscode-interpreter
echo

popd > /dev/null

echo "✅ Python environment setup complete."
