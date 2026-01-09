#!/bin/bash

# CORS Configuration Test Script
# This script tests the CORS configuration for the Nexus Agent API
# Run this script after starting the backend server to verify CORS is working correctly

set -e  # Exit on error

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

# API base URL
API_BASE_URL="http://localhost:8001/v1"
FRONTEND_ORIGIN="http://localhost:5173"

echo "=========================================="
echo "CORS Configuration Test Script"
echo "=========================================="
echo ""

# Function to print test result
print_result() {
    if [ $1 -eq 0 ]; then
        echo -e "${GREEN}✓ PASS${NC}: $2"
    else
        echo -e "${RED}✗ FAIL${NC}: $2"
    fi
}

# Function to check if server is running
check_server() {
    echo -e "${YELLOW}Checking if backend server is running...${NC}"
    if curl -s -f "${API_BASE_URL}/health" > /dev/null 2>&1; then
        echo -e "${GREEN}✓ Server is running${NC}"
        return 0
    else
        echo -e "${RED}✗ Server is not running${NC}"
        echo "Please start the server with: python run_server.py"
        return 1
    fi
}

# Test 1: Health Check (GET request)
test_health_check() {
    echo ""
    echo -e "${YELLOW}Test 1: Health Check (GET request)${NC}"
    echo "----------------------------------------"
    
    response=$(curl -s -w "\n%{http_code}" "${API_BASE_URL}/health")
    http_code=$(echo "$response" | tail -n1)
    body=$(echo "$response" | sed '$d')
    
    echo "Response Code: $http_code"
    echo "Response Body: $body"
    
    if [ "$http_code" = "200" ]; then
        print_result 0 "Health check successful"
        return 0
    else
        print_result 1 "Health check failed"
        return 1
    fi
}

# Test 2: OPTIONS Preflight Request to /sessions/
test_options_sessions() {
    echo ""
    echo -e "${YELLOW}Test 2: OPTIONS Preflight Request to /sessions/${NC}"
    echo "----------------------------------------"
    
    response=$(curl -s -w "\n%{http_code}" -X OPTIONS \
        -H "Origin: ${FRONTEND_ORIGIN}" \
        -H "Access-Control-Request-Method: POST" \
        -H "Access-Control-Request-Headers: Content-Type" \
        -v "${API_BASE_URL}/sessions/" 2>&1)
    
    http_code=$(echo "$response" | grep "< HTTP" | awk '{print $3}')
    
    echo "Response Code: $http_code"
    
    # Check for CORS headers
    if echo "$response" | grep -q "Access-Control-Allow-Origin"; then
        echo -e "${GREEN}✓${NC} Access-Control-Allow-Origin header found"
        cors_origin=$(echo "$response" | grep "Access-Control-Allow-Origin" | head -n1)
        echo "  $cors_origin"
    else
        echo -e "${RED}✗${NC} Access-Control-Allow-Origin header missing"
    fi
    
    if echo "$response" | grep -q "Access-Control-Allow-Methods"; then
        echo -e "${GREEN}✓${NC} Access-Control-Allow-Methods header found"
        cors_methods=$(echo "$response" | grep "Access-Control-Allow-Methods" | head -n1)
        echo "  $cors_methods"
    else
        echo -e "${RED}✗${NC} Access-Control-Allow-Methods header missing"
    fi
    
    if echo "$response" | grep -q "Access-Control-Allow-Headers"; then
        echo -e "${GREEN}✓${NC} Access-Control-Allow-Headers header found"
        cors_headers=$(echo "$response" | grep "Access-Control-Allow-Headers" | head -n1)
        echo "  $cors_headers"
    else
        echo -e "${RED}✗${NC} Access-Control-Allow-Headers header missing"
    fi
    
    if [ "$http_code" = "200" ]; then
        print_result 0 "OPTIONS request successful"
        return 0
    else
        print_result 1 "OPTIONS request failed"
        return 1
    fi
}

# Test 3: POST Request to /sessions/ (Create Session)
test_create_session() {
    echo ""
    echo -e "${YELLOW}Test 3: POST Request to /sessions/ (Create Session)${NC}"
    echo "----------------------------------------"
    
    response=$(curl -s -w "\n%{http_code}" -X POST \
        -H "Origin: ${FRONTEND_ORIGIN}" \
        -H "Content-Type: application/json" \
        -d '{"user_id": "test_user"}' \
        -v "${API_BASE_URL}/sessions/" 2>&1)
    
    http_code=$(echo "$response" | grep "< HTTP" | awk '{print $3}')
    body=$(echo "$response" | tail -n1)
    
    echo "Response Code: $http_code"
    echo "Response Body: $body"
    
    # Check for CORS headers
    if echo "$response" | grep -q "Access-Control-Allow-Origin"; then
        echo -e "${GREEN}✓${NC} Access-Control-Allow-Origin header found"
        cors_origin=$(echo "$response" | grep "Access-Control-Allow-Origin" | head -n1)
        echo "  $cors_origin"
    else
        echo -e "${RED}✗${NC} Access-Control-Allow-Origin header missing"
    fi
    
    if [ "$http_code" = "200" ]; then
        print_result 0 "Session creation successful"
        return 0
    else
        print_result 1 "Session creation failed"
        return 1
    fi
}

# Test 4: OPTIONS Preflight Request to /chat/completions
test_options_chat() {
    echo ""
    echo -e "${YELLOW}Test 4: OPTIONS Preflight Request to /chat/completions${NC}"
    echo "----------------------------------------"
    
    response=$(curl -s -w "\n%{http_code}" -X OPTIONS \
        -H "Origin: ${FRONTEND_ORIGIN}" \
        -H "Access-Control-Request-Method: POST" \
        -H "Access-Control-Request-Headers: Content-Type" \
        -v "${API_BASE_URL}/chat/completions" 2>&1)
    
    http_code=$(echo "$response" | grep "< HTTP" | awk '{print $3}')
    
    echo "Response Code: $http_code"
    
    if [ "$http_code" = "200" ]; then
        print_result 0 "OPTIONS request to /chat/completions successful"
        return 0
    else
        print_result 1 "OPTIONS request to /chat/completions failed"
        return 1
    fi
}

# Test 5: POST Request to /chat/completions (Send Message)
test_send_message() {
    echo ""
    echo -e "${YELLOW}Test 5: POST Request to /chat/completions (Send Message)${NC}"
    echo "----------------------------------------"
    
    response=$(curl -s -w "\n%{http_code}" -X POST \
        -H "Origin: ${FRONTEND_ORIGIN}" \
        -H "Content-Type: application/json" \
        -d '{
            "messages": [{"role": "user", "content": "Hello"}],
            "session_id": "test_session_123",
            "user": "test_user"
        }' \
        -v "${API_BASE_URL}/chat/completions" 2>&1)
    
    http_code=$(echo "$response" | grep "< HTTP" | awk '{print $3}')
    
    echo "Response Code: $http_code"
    
    # Check for CORS headers
    if echo "$response" | grep -q "Access-Control-Allow-Origin"; then
        echo -e "${GREEN}✓${NC} Access-Control-Allow-Origin header found"
        cors_origin=$(echo "$response" | grep "Access-Control-Allow-Origin" | head -n1)
        echo "  $cors_origin"
    else
        echo -e "${RED}✗${NC} Access-Control-Allow-Origin header missing"
    fi
    
    if [ "$http_code" = "200" ]; then
        print_result 0 "Message send successful"
        return 0
    else
        print_result 1 "Message send failed (this is expected if agent is not fully configured)"
        return 1
    fi
}

# Main test execution
main() {
    # Check if server is running
    if ! check_server; then
        exit 1
    fi
    
    # Run all tests
    test_health_check
    test_options_sessions
    test_create_session
    test_options_chat
    test_send_message
    
    echo ""
    echo "=========================================="
    echo "CORS Configuration Test Complete"
    echo "=========================================="
    echo ""
    echo "If all tests passed, CORS is configured correctly!"
    echo "You can now test the frontend at: ${FRONTEND_ORIGIN}"
}

# Run main function
main
