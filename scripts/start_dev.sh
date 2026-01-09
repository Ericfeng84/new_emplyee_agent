#!/bin/bash

# Development Server Startup Script
# This script starts Redis and the backend server in the correct order

set -e  # Exit on error

echo "🚀 Starting Development Environment..."
echo ""

# Color codes for output
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
RED='\033[0;31m'
NC='\033[0m' # No Color

# Function to check if a command exists
command_exists() {
    command -v "$1" >/dev/null 2>&1
}

# Check if Redis is installed
if ! command_exists redis-server; then
    echo -e "${RED}❌ Redis is not installed. Please install Redis first.${NC}"
    echo "   On macOS: brew install redis"
    echo "   On Ubuntu: sudo apt-get install redis-server"
    exit 1
fi

# Check if Redis is already running
if lsof -Pi :6379 -sTCP:LISTEN -t >/dev/null 2>&1; then
    echo -e "${YELLOW}⚠️  Redis is already running on port 6379${NC}"
else
    echo "📦 Starting Redis server..."
    redis-server --daemonize yes
    
    # Wait for Redis to be ready
    echo "⏳ Waiting for Redis to be ready..."
    sleep 2
    
    # Verify Redis is running
    if redis-cli ping >/dev/null 2>&1; then
        echo -e "${GREEN}✅ Redis is running successfully${NC}"
    else
        echo -e "${RED}❌ Failed to start Redis${NC}"
        exit 1
    fi
fi

echo ""

# Check if backend server is already running
if lsof -Pi :8001 -sTCP:LISTEN -t >/dev/null 2>&1; then
    echo -e "${YELLOW}⚠️  Backend server is already running on port 8001${NC}"
    echo "   To restart it, kill the process first:"
    echo "   kill \$(lsof -t -i:8001)"
else
    echo "🔧 Starting backend server..."
    
    # Start the backend server
    # Using uvicorn directly for better control
    uvicorn nexus_agent.api.main:app \
        --host 0.0.0.0 \
        --port 8001 \
        --reload \
        --log-level info &
    
    # Store the process ID
    BACKEND_PID=$!
    echo $BACKEND_PID > .backend_pid
    
    # Wait for backend to be ready
    echo "⏳ Waiting for backend server to be ready..."
    sleep 3
    
    # Verify backend is running
    if curl -s http://localhost:8001/v1/health >/dev/null 2>&1; then
        echo -e "${GREEN}✅ Backend server is running successfully${NC}"
    else
        echo -e "${RED}❌ Failed to start backend server${NC}"
        exit 1
    fi
fi

echo ""
echo -e "${GREEN}🎉 Development environment is ready!${NC}"
echo ""
echo "📝 Services running:"
echo "   - Redis:        http://localhost:6379"
echo "   - Backend API:  http://localhost:8001"
echo "   - API Docs:     http://localhost:8001/docs"
echo ""
echo "🌐 To start the frontend, run:"
echo "   cd frontend && npm run dev"
echo ""
echo "🛑 To stop the backend server:"
echo "   kill \$(cat .backend_pid) 2>/dev/null || kill \$(lsof -t -i:8001)"
echo ""
echo "📊 To check logs:"
echo "   - Backend logs are shown in this terminal"
echo "   - Redis logs: tail -f /usr/local/var/log/redis.log (macOS)"
echo ""
