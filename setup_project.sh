#!/bin/bash

# 🚫 Step 0: Remove existing virtual environment
echo "Removing existing virtual environment..."
rm -rf venv

# 🧪 Step 1: Create new virtual environment
echo "Creating new virtual environment..."
python3 -m venv venv

# ✅ Step 2: Activate virtual environment
echo "Activating virtual environment..."
source venv/bin/activate

# 📦 Step 3: Install required packages
echo "Installing OpenAI and python-dotenv..."
pip install --upgrade pip
pip install openai python-dotenv

# 🚀 Step 4: Run your main script
echo "Running main.py..."
python main.py
