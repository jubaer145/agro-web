#!/bin/bash

# Test script for Farm Registry API endpoints

echo "======================================"
echo "Farm Registry API Test Script"
echo "======================================"
echo ""

BASE_URL="http://localhost:8000"

echo "1. Testing Health Endpoint..."
curl -s "${BASE_URL}/api/health/" | python3 -m json.tool
echo -e "\n"

echo "2. Testing Districts List..."
curl -s "${BASE_URL}/api/districts/" | python3 -m json.tool | head -20
echo -e "\n"

echo "3. Testing Farms List..."
curl -s "${BASE_URL}/api/farms/" | python3 -m json.tool | head -50
echo -e "\n"

echo "4. Testing Farms Filter by District (ALM)..."
curl -s "${BASE_URL}/api/farms/?district=ALM" | python3 -m json.tool | head -30
echo -e "\n"

echo "5. Testing Farms Search..."
curl -s "${BASE_URL}/api/farms/?search=Almas" | python3 -m json.tool | head -30
echo -e "\n"

echo "======================================"
echo "API Test Complete!"
echo "======================================"
