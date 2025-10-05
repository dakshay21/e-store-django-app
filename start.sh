#!/bin/bash

# E-commerce Backend Startup Script

echo "🚀 Starting E-commerce Backend with Docker..."

# Check if Docker is running
if ! docker info > /dev/null 2>&1; then
    echo "❌ Docker is not running. Please start Docker first."
    exit 1
fi

# Check if docker-compose is available
if ! command -v docker-compose &> /dev/null; then
    echo "❌ docker-compose is not installed. Please install docker-compose first."
    exit 1
fi

# Function to show help
show_help() {
    echo "Usage: ./start.sh [COMMAND]"
    echo ""
    echo "Commands:"
    echo "  dev       Start development environment (default)"
    echo "  prod      Start production environment"
    echo "  build     Build Docker images"
    echo "  stop      Stop all containers"
    echo "  clean     Remove all containers and volumes"
    echo "  logs      Show container logs"
    echo "  shell     Open shell in web container"
    echo "  help      Show this help message"
    echo ""
}

# Function to start development environment
start_dev() {
    echo "🔧 Starting development environment..."
    docker-compose up --build
}

# Function to start production environment
start_prod() {
    echo "🏭 Starting production environment..."
    docker-compose -f docker-compose.prod.yml up --build -d
}

# Function to build images
build_images() {
    echo "🔨 Building Docker images..."
    docker-compose build
}

# Function to stop containers
stop_containers() {
    echo "🛑 Stopping containers..."
    docker-compose down
}

# Function to clean up
clean_up() {
    echo "🧹 Cleaning up containers and volumes..."
    docker-compose down -v --remove-orphans
    docker system prune -f
}

# Function to show logs
show_logs() {
    echo "📋 Showing container logs..."
    docker-compose logs -f
}

# Function to open shell
open_shell() {
    echo "🐚 Opening shell in web container..."
    docker-compose exec web bash
}

# Main script logic
case "${1:-dev}" in
    "dev")
        start_dev
        ;;
    "prod")
        start_prod
        ;;
    "build")
        build_images
        ;;
    "stop")
        stop_containers
        ;;
    "clean")
        clean_up
        ;;
    "logs")
        show_logs
        ;;
    "shell")
        open_shell
        ;;
    "help"|"-h"|"--help")
        show_help
        ;;
    *)
        echo "❌ Unknown command: $1"
        show_help
        exit 1
        ;;
esac
