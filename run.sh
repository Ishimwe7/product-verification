#!/bin/bash

echo "Starting Docker containers..."
docker-compose up -d

echo "Setting up environment..."
export PYTHONPATH=$PYTHONPATH:.

echo "Starting FastAPI server..."
python.exe -m uvicorn src.main:app --reload