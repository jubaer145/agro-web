#!/bin/bash

# Акыл Жер Government Portal - Quick Start Script
# This script helps you run the backend and frontend servers

echo "======================================"
echo "Акыл Жер Government Portal Quick Start"
echo "======================================"
echo ""

# Colors for output
GREEN='\033[0;32m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

echo -e "${BLUE}BACKEND (Django REST Framework)${NC}"
echo "To run the backend server:"
echo "  cd backend"
echo "  source venv/bin/activate"
echo "  python manage.py runserver 8000"
echo ""
echo "Backend will be available at: http://localhost:8000"
echo "API Health endpoint: http://localhost:8000/api/health/"
echo ""

echo -e "${BLUE}FRONTEND (React + TypeScript + Vite)${NC}"
echo "To run the frontend dev server:"
echo "  cd frontend"
echo "  npm run dev"
echo ""
echo "Frontend will be available at: http://localhost:5173"
echo ""

echo -e "${GREEN}TESTING${NC}"
echo "Backend tests:"
echo "  cd backend && source venv/bin/activate && python manage.py test"
echo ""
echo "Frontend tests:"
echo "  cd frontend && npm test"
echo ""

echo "======================================"
echo "Choose an option:"
echo "1) Start Backend Server"
echo "2) Start Frontend Server"
echo "3) Run Backend Tests"
echo "4) Run Frontend Tests"
echo "5) Exit"
echo "======================================"

read -p "Enter your choice [1-5]: " choice

case $choice in
  1)
    echo "Starting Django backend server..."
    cd backend && source venv/bin/activate && python manage.py runserver 8000
    ;;
  2)
    echo "Starting React frontend dev server..."
    cd frontend && npm run dev
    ;;
  3)
    echo "Running Django tests..."
    cd backend && source venv/bin/activate && python manage.py test
    ;;
  4)
    echo "Running Jest tests..."
    cd frontend && npm test
    ;;
  5)
    echo "Goodbye!"
    exit 0
    ;;
  *)
    echo "Invalid option"
    exit 1
    ;;
esac
