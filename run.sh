#!/bin/bash

# Exit immediately if a command fails
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

# Step 5: Install required packages
echo "📚 Installing required Python packages..."
pip install --upgrade pip
pip install google-generativeai httpx python-dotenv openai

# Step 6: Set API key
if [ -z "$GOOGLE_API_KEY" ]; then
  echo "🔐 Enter your Google API key:"
  read -r GOOGLE_API_KEY
  export GOOGLE_API_KEY=$GOOGLE_API_KEY
fi

# Step 7: Run your agent
echo "🚀 Running main.py..."
python main.py
