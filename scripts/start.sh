#!/bin/bash

# Script to start the EMA-AI service

# Create directory if it doesn't exist
mkdir -p scripts

# Colors for output
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
RED='\033[0;31m'
NC='\033[0m' # No Color

# Check if Python is installed
if ! command -v python3 &> /dev/null; then
    echo -e "${RED}Python 3 is not installed. Please install Python 3 and try again.${NC}"
    exit 1
fi

# Check if virtual environment exists
if [ ! -d "venv" ]; then
    echo -e "${YELLOW}Virtual environment not found. Creating one...${NC}"
    python3 -m venv venv
    echo -e "${GREEN}Virtual environment created.${NC}"
fi

# Activate virtual environment
echo -e "${YELLOW}Activating virtual environment...${NC}"
source venv/bin/activate

# Install dependencies
echo -e "${YELLOW}Installing dependencies...${NC}"
pip install -r requirements.txt

# Check if .env file exists
if [ ! -f ".env" ]; then
    echo -e "${YELLOW}.env file not found. Creating from example...${NC}"
    cp .env.example .env
    echo -e "${GREEN}.env file created. Please edit it with your API keys.${NC}"
    echo -e "${RED}WARNING: You need to add your OpenAI API key to the .env file!${NC}"
fi

# Start the service
echo -e "${GREEN}Starting EMA-AI service...${NC}"
uvicorn main:app --reload --port 8000 