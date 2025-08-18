#!/bin/bash

set -e

echo "🚀 Starting first-time setup..."

# Step 1: Download Miniconda installer if not already present
if [ ! -f Miniconda3-latest-MacOSX-arm64.sh ]; then
  echo "📦 Downloading Miniconda installer..."
  curl -O https://repo.anaconda.com/miniconda/Miniconda3-latest-MacOSX-arm64.sh
else
  echo "✅ Miniconda installer already downloaded."
fi

# Step 2: Install Miniconda if not already installed
if [ ! -d "$HOME/miniconda" ]; then
  echo "🔧 Installing Miniconda..."
  bash Miniconda3-latest-MacOSX-arm64.sh -b -p $HOME/miniconda
else
  echo "✅ Miniconda already installed."
fi

# Step 3: Initialize conda
echo "🔁 Initializing Conda..."
source "$HOME/miniconda/bin/activate"

# Step 4: Create and activate environment
if conda info --envs | grep -q "gemini"; then
  echo "✅ Environment 'gemini' already exists."
else
  echo "🌱 Creating 'gemini' environment..."
  conda create -y -n gemini python=3.11
fi

echo "🔀 Activating 'gemini' environment..."
conda activate gemini

# Step 5: Install required packages if missing
echo "📚 Checking and installing required Python packages..."

# Upgrade pip
pip install --upgrade pip

# Define required packages
REQUIRED_PACKAGES=(
  google-generativeai
  httpx
  python-dotenv
  openai
  psycopg2-binary
  chromadb
  sentence_transformers
)

for pkg in "${REQUIRED_PACKAGES[@]}"; do
  if pip show "$pkg" > /dev/null 2>&1; then
    echo "✅ $pkg already installed."
  else
    echo "📦 Installing $pkg..."
    pip install "$pkg"
  fi
done

# Step 6: Load environment variables from .env
if [ -f .env ]; then
  echo "🔐 Loading environment variables from .env..."
  export $(grep -v '^#' .env | xargs)
else
  echo "⚠️ .env file not found. Please create one with your GOOGLE_API_KEY."
  exit 1
fi

# Step 7: Run your main app
echo "🚀 Running app.py..."
python app.py
