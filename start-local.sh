#!/bin/bash

# Start Online Boutique with Open Source Observability
# This script uses Jaeger for distributed tracing instead of Azure Application Insights

set -e

echo "🚀 Starting Online Boutique with Open Source Observability"
echo ""

# Check if Docker is running
if ! docker info > /dev/null 2>&1; then
    echo "❌ Docker is not running. Please start Docker and try again."
    exit 1
fi

echo "📦 Starting services with Jaeger for distributed tracing..."
echo ""

# Start all services
docker-compose up --build -d

echo ""
echo "✅ All services are starting up! This may take a few minutes..."
echo ""
echo "🎯 Access Points:"
echo "   • Frontend:    http://localhost:8080"
echo "   • Jaeger UI:   http://localhost:16686"
echo "   • Redis:       localhost:6379"
echo ""
echo "📊 Observability:"
echo "   • Jaeger provides distributed tracing"
echo "   • View request flows and performance metrics"
echo "   • No Azure account or configuration needed!"
echo ""
echo "🔍 To view logs:"
echo "   docker-compose logs -f [service-name]"
echo ""
echo "🛑 To stop all services:"
echo "   docker-compose down"
echo ""
echo "📚 For more information, see OBSERVABILITY.md"
echo ""
echo "🎉 Enjoy your open-source observability stack!"
