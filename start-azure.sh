#!/bin/bash

# Online Boutique Azure Migration - Setup Script
# This script helps set up the environment for running Online Boutique with Azure services

echo "🚀 Online Boutique Azure Migration Setup"
echo "========================================"

# Check if required tools are installed
echo "📋 Checking prerequisites..."

# Check Docker
if ! command -v docker &> /dev/null; then
    echo "❌ Docker is not installed. Please install Docker first."
    exit 1
fi

# Check Docker Compose
if ! docker compose version &> /dev/null; then
    echo "❌ Docker Compose is not available. Please install Docker Compose v2+."
    exit 1
fi

echo "✅ Docker and Docker Compose are available"

# Check for environment file
if [ ! -f .env ]; then
    echo "📝 Creating environment file from template..."
    cp .env.example .env
    echo "✅ Created .env file - please update it with your Azure Application Insights connection string"
    echo ""
    echo "To get your Azure Application Insights connection string:"
    echo "1. Login to Azure: az login"
    echo "2. Create Application Insights: az monitor app-insights component create --app online-boutique-dev --location eastus --resource-group your-rg --kind web"
    echo "3. Get connection string: az monitor app-insights component show --app online-boutique-dev --resource-group your-rg --query connectionString -o tsv"
    echo ""
else
    echo "✅ Environment file (.env) already exists"
fi

# Build and run the application
echo ""
echo "🔨 Building and starting Online Boutique..."
echo "This may take a few minutes on first run..."
echo ""

# Build and start all services
docker compose up --build -d

if [ $? -eq 0 ]; then
    echo ""
    echo "🎉 Online Boutique is now running!"
    echo ""
    echo "📱 Access the application:"
    echo "   Web UI: http://localhost:8080"
    echo ""
    echo "🔍 Monitor services:"
    echo "   Check status: docker compose ps"
    echo "   View logs: docker compose logs -f [service-name]"
    echo "   Stop services: docker compose down"
    echo ""
    echo "☁️  Azure Integration:"
    echo "   If you configured Application Insights in .env, telemetry data"
    echo "   will be sent to your Azure Application Insights resource."
    echo ""
else
    echo "❌ Failed to start Online Boutique. Check the logs with: docker compose logs"
    exit 1
fi
