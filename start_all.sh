#!/bin/bash

# One-Click Startup Script for Nexus Agent
# This script starts Redis, backend server, and frontend server in the correct order

set -e  # Exit on error

echo "🚀 Starting Nexus Agent Development Environment..."
echo ""

# Color codes for output
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
RED='\033[0;31m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Function to check if a command exists
command_exists() {
    command -v "$1" >/dev/null 2>&1
}

# Function to cleanup on exit
cleanup() {
    echo ""
    echo -e "${YELLOW}🛑 Stopping all services...${NC}"
    
    # Stop frontend if running
    if [ -f .frontend_pid ]; then
        FRONTEND_PID=$(cat .frontend_pid 2>/dev/null)
        if ps -p $FRONTEND_PID > /dev/null 2>&1; then
            echo "Stopping frontend (PID: $FRONTEND_PID)..."
            kill $FRONTEND_PID 2>/dev/null || true
        fi
        rm -f .frontend_pid
    fi
    
    # Stop backend if running
    if [ -f .backend_pid ]; then
        BACKEND_PID=$(cat .backend_pid 2>/dev/null)
        if ps -p $BACKEND_PID > /dev/null 2>&1; then
            echo "Stopping backend (PID: $BACKEND_PID)..."
            kill $BACKEND_PID 2>/dev/null || true
        fi
        rm -f .backend_pid
    fi
    
    echo -e "${GREEN}✅ All services stopped${NC}"
    exit 0
}

# Trap SIGINT and SIGTERM
trap cleanup SIGINT SIGTERM

# Check if Redis is installed
if ! command_exists redis-server; then
    echo -e "${RED}❌ Redis is not installed. Please install Redis first.${NC}"
    echo "   On macOS: brew install redis"
    echo "   On Ubuntu: sudo apt-get install redis-server"
    exit 1
fi

# Check if Node.js is installed
if ! command_exists node; then
    echo -e "${RED}❌ Node.js is not installed. Please install Node.js first.${NC}"
    echo "   On macOS: brew install node"
    echo "   On Ubuntu: sudo apt-get install nodejs npm"
    exit 1
fi

# Check if Python is installed
if ! command_exists python3; then
    echo -e "${RED}❌ Python 3 is not installed. Please install Python 3 first.${NC}"
    exit 1
fi

# Check if npm is installed
if ! command_exists npm; then
    echo -e "${RED}❌ npm is not installed. Please install npm first.${NC}"
    exit 1
fi

# Step 1: Start Redis
echo -e "${BLUE}📦 Step 1/4: Starting Redis server...${NC}"
if lsof -Pi :6379 -sTCP:LISTEN -t >/dev/null 2>&1; then
    echo -e "${YELLOW}⚠️  Redis is already running on port 6379${NC}"
else
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

# Step 2: Check and install frontend dependencies
echo -e "${BLUE}📦 Step 2/4: Checking frontend dependencies...${NC}"
cd frontend
if [ ! -d "node_modules" ]; then
    echo "📥 Installing frontend dependencies..."
    npm install
    if [ $? -ne 0 ]; then
        echo -e "${RED}❌ Failed to install frontend dependencies${NC}"
        exit 1
    fi
    echo -e "${GREEN}✅ Frontend dependencies installed${NC}"
else
    echo -e "${GREEN}✅ Frontend dependencies already installed${NC}"
fi
cd ..
echo ""

# Step 3: Start backend server
echo -e "${BLUE}📦 Step 3/4: Starting backend server...${NC}"
if lsof -Pi :8001 -sTCP:LISTEN -t >/dev/null 2>&1; then
    echo -e "${YELLOW}⚠️  Backend server is already running on port 8001${NC}"
else
    # Start the backend server in background
    uvicorn nexus_agent.api.main:app \
        --host 0.0.0.0 \
        --port 8001 \
        --reload \
        --log-level info > backend.log 2>&1 &
    
    # Store the process ID
    BACKEND_PID=$!
    echo $BACKEND_PID > .backend_pid
    
    # Wait for backend to be ready
    echo "⏳ Waiting for backend server to be ready..."
    sleep 5
    
    # Verify backend is running
    if curl -s http://localhost:8001/v1/health >/dev/null 2>&1; then
        echo -e "${GREEN}✅ Backend server is running successfully${NC}"
    else
        echo -e "${RED}❌ Failed to start backend server${NC}"
        echo "Check backend.log for details"
        exit 1
    fi
fi
echo ""

# Step 4: Start frontend server
echo -e "${BLUE}📦 Step 4/4: Starting frontend server...${NC}"
if lsof -Pi :5173 -sTCP:LISTEN -t >/dev/null 2>&1; then
    echo -e "${YELLOW}⚠️  Frontend server is already running on port 5173${NC}"
else
    # Start the frontend server in background
    cd frontend
    npm run dev > ../frontend.log 2>&1 &
    
    # Store the process ID
    FRONTEND_PID=$!
    echo $FRONTEND_PID > ../.frontend_pid
    cd ..
    
    # Wait for frontend to be ready
    echo "⏳ Waiting for frontend server to be ready..."
    sleep 5
    
    # Verify frontend is running
    if lsof -Pi :5173 -sTCP:LISTEN -t >/dev/null 2>&1; then
        echo -e "${GREEN}✅ Frontend server is running successfully${NC}"
    else
        echo -e "${RED}❌ Failed to start frontend server${NC}"
        echo "Check frontend.log for details"
        exit 1
    fi
fi
echo ""

# Success message
echo -e "${GREEN}🎉 All services are running successfully!${NC}"
echo ""
echo -e "${BLUE}📝 Services:${NC}"
echo "   - Redis:        http://localhost:6379"
echo "   - Backend API:  http://localhost:8001"
echo "   - Frontend:     http://localhost:5173"
echo "   - API Docs:     http://localhost:8001/docs"
echo ""
echo -e "${BLUE}🌐 Open your browser and navigate to:${NC}"
echo -e "   ${GREEN}http://localhost:5173${NC}"
echo ""
echo -e "${BLUE}📊 Logs:${NC}"
echo "   - Backend:  tail -f backend.log"
echo "   - Frontend: tail -f frontend.log"
echo ""
echo -e "${BLUE}🛑 To stop all services, press Ctrl+C${NC}"
echo ""

# Keep the script running
echo -e "${YELLOW}Press Ctrl+C to stop all services...${NC}"
while true; do
    sleep 1
done
