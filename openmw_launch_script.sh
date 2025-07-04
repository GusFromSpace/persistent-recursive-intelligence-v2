#!/bin/bash

# Launch OpenMW with Metrics API Integration
# This script starts the metrics API server and then launches OpenMW

echo "🎮 OpenMW with Metrics Integration Launcher"
echo "=========================================="

# Set up paths
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
METRICS_DIR="$SCRIPT_DIR/metrics_integration"
BUILD_DIR="$SCRIPT_DIR/build"

# Kill any existing metrics API server
echo "🔧 Checking for existing metrics API..."
pkill -f "minimal_metrics_api" 2>/dev/null && echo "   Stopped existing metrics API server"

# Start metrics API server in background
echo "🚀 Starting Metrics API server..."
cd "$SCRIPT_DIR"
python3 minimal_metrics_api.py &
METRICS_PID=$!
echo "   Metrics API PID: $METRICS_PID"

# Wait for API to be ready
echo "⏳ Waiting for Metrics API to start..."
for i in {1..30}; do
    if curl -s http://127.0.0.1:8001/health >/dev/null 2>&1; then
        echo "✅ Metrics API is ready!"
        break
    fi
    sleep 1
done

# Verify API is running
if ! curl -s http://127.0.0.1:8001/health >/dev/null 2>&1; then
    echo "❌ Failed to start Metrics API"
    exit 1
fi

# Show available endpoints
echo ""
echo "📊 Metrics API Endpoints:"
echo "   - Health: http://127.0.0.1:8001/health"
echo "   - Docs: http://127.0.0.1:8001/docs"
echo "   - Consciousness: http://127.0.0.1:8001/metrics/consciousness"
echo "   - Performance: http://127.0.0.1:8001/metrics/performance"
echo ""

# Launch OpenMW
echo "🎮 Launching OpenMW..."
cd "$BUILD_DIR"
./openmw

# Cleanup on exit
echo ""
echo "🛑 OpenMW closed, stopping Metrics API..."
kill $METRICS_PID 2>/dev/null
echo "✅ Cleanup complete"