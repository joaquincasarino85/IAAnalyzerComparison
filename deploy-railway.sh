#!/bin/bash

# 🚀 Railway Deployment Script for IAAnalyzerComparator
# This script helps you deploy your application to Railway

set -e

echo "🚀 Starting Railway Deployment..."

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Function to print colored output
print_status() {
    echo -e "${BLUE}[INFO]${NC} $1"
}

print_success() {
    echo -e "${GREEN}[SUCCESS]${NC} $1"
}

print_warning() {
    echo -e "${YELLOW}[WARNING]${NC} $1"
}

print_error() {
    echo -e "${RED}[ERROR]${NC} $1"
}

# Check if Railway CLI is installed
check_railway_cli() {
    if ! command -v railway &> /dev/null; then
        print_warning "Railway CLI not found. Installing..."
        npm install -g @railway/cli
    else
        print_success "Railway CLI is installed"
    fi
}

# Check if user is logged in to Railway
check_railway_login() {
    if ! railway whoami &> /dev/null; then
        print_warning "Not logged in to Railway. Please login..."
        railway login
    else
        print_success "Logged in to Railway"
    fi
}

# Check if project exists
check_project() {
    if [ -z "$RAILWAY_PROJECT_ID" ]; then
        print_warning "RAILWAY_PROJECT_ID not set. Creating new project..."
        railway init
    else
        print_success "Using existing project: $RAILWAY_PROJECT_ID"
    fi
}

# Deploy backend
deploy_backend() {
    print_status "Deploying backend..."
    
    # Set environment variables for backend
    railway variables set \
        ENVIRONMENT=production \
        CORS_ORIGINS="https://your-frontend-domain.railway.app" \
        --service backend
    
    # Deploy
    railway up --service backend
    
    print_success "Backend deployed successfully!"
}

# Deploy frontend
deploy_frontend() {
    print_status "Deploying frontend..."
    
    # Get backend URL
    BACKEND_URL=$(railway domain --service backend)
    
    # Set environment variables for frontend
    railway variables set \
        VITE_API_URL="https://$BACKEND_URL" \
        --service frontend
    
    # Deploy
    railway up --service frontend
    
    print_success "Frontend deployed successfully!"
}

# Setup database
setup_database() {
    print_status "Setting up PostgreSQL database..."
    
    # Create PostgreSQL service if it doesn't exist
    if ! railway service list | grep -q "postgres"; then
        railway service create postgres --type postgresql
    fi
    
    # Get database URL
    DB_URL=$(railway variables get DATABASE_URL --service postgres)
    
    # Set database URL for backend 
    railway variables set DATABASE_URL="postgresql://admin:admin123@ia_db:5432/ianalyzer" --service backend
    
    print_success "Database setup completed!"
}

# Setup API keys
setup_api_keys() {
    print_status "Setting up API keys..."
    
    # Check if .env file exists
    if [ -f ".env" ]; then
        print_warning "Found .env file. Please add your API keys to Railway variables:"
        echo ""
        echo "Required API keys:"
        echo "- OPENAI_API_KEY"
        echo "- ANTHROPIC_API_KEY"
        echo "- GOOGLE_AI_API_KEY"
        echo "- COHERE_API_KEY"
        echo "- PERPLEXITY_API_KEY"
        echo ""
        echo "You can add them using:"
        echo "railway variables set OPENAI_API_KEY=your_key --service backend"
        echo ""
    else
        print_warning "No .env file found. Please create one with your API keys."
    fi
}

# Main deployment function
main() {
    print_status "Starting deployment process..."
    
    # Pre-flight checks
    check_railway_cli
    check_railway_login
    check_project
    
    # Setup services
    setup_database
    setup_api_keys
    
    # Deploy services
    deploy_backend
    deploy_frontend
    
    print_success "🎉 Deployment completed successfully!"
    print_status "Your application should be available at:"
    echo "Frontend: $(railway domain --service frontend)"
    echo "Backend: $(railway domain --service backend)"
    echo ""
    print_status "Don't forget to:"
    echo "1. Add your API keys to Railway variables"
    echo "2. Test the application"
    echo "3. Set up custom domains (optional)"
}

# Run main function
main "$@" 