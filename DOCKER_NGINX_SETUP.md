# Docker + Nginx Setup Guide

## Overview
Your Django REST Framework application is now configured to run behind Nginx as a reverse proxy.

## Architecture
```
Internet → Nginx (Port 80) → Django (Port 8000)
```

## What's Configured

### Services
1. **web**: Django/DRF application running on port 8000 (internal)
2. **nginx**: Nginx reverse proxy exposed on port 80 (external)

### Networks
- Custom bridge network `app-network` for service communication

### Volumes
- `static_volume`: Shared volume for Django static files
- `media_volume`: Shared volume for user-uploaded media files

### Features
- ✅ Reverse proxy to Django backend
- ✅ Static file serving with caching (30 days)
- ✅ Media file serving with caching
- ✅ Gzip compression
- ✅ Security headers
- ✅ 100MB client upload limit
- ✅ Connection timeouts configured

## Usage

### Start Services
```bash
# Build and start all services
docker-compose up -d

# View logs
docker-compose logs -f

# View nginx logs only
docker-compose logs -f nginx

# View web logs only
docker-compose logs -f web
```

### Stop Services
```bash
# Stop all services
docker-compose down

# Stop and remove volumes
docker-compose down -v
```

### Rebuild After Changes
```bash
# Rebuild and restart
docker-compose up -d --build
```

### Collect Static Files
Before running the application, collect static files:
```bash
# Run inside the web container
docker-compose exec web python manage.py collectstatic --noinput
```

## Access Points

- **Application**: http://localhost (Port 80)
- **API Endpoints**: http://localhost/api/...
- **Admin Panel**: http://localhost/admin/
- **Static Files**: http://localhost/static/...
- **Media Files**: http://localhost/media/...

## Testing Nginx Configuration

Test nginx configuration without restarting:
```bash
docker-compose exec nginx nginx -t
```

Reload nginx configuration:
```bash
docker-compose exec nginx nginx -s reload
```

## Troubleshooting

### Check Service Status
```bash
docker-compose ps
```

### Check Nginx Errors
```bash
docker-compose exec nginx cat /var/log/nginx/error.log
```

### Check if Services Can Communicate
```bash
# From nginx container, check if web is reachable
docker-compose exec nginx wget -qO- http://web:8000
```

### Common Issues

1. **502 Bad Gateway**
   - Django app is not running
   - Check: `docker-compose logs web`

2. **Static files not loading**
   - Run collectstatic: `docker-compose exec web python manage.py collectstatic --noinput`

3. **Permission denied errors**
   - Check volume permissions
   - May need to adjust file ownership in Dockerfile

## Configuration Files

- `docker-compose.yml`: Service orchestration
- `nginx.conf`: Nginx reverse proxy configuration
- `Dockerfile`: Django application container build
- `docker.env`: Environment variables for Django

## Production Considerations

For production deployment, consider:
1. Use environment-specific settings (DEBUG=False)
2. Add SSL/TLS certificates
3. Update server_name in nginx.conf
4. Use external database instead of SQLite
5. Set proper SECRET_KEY
6. Configure ALLOWED_HOSTS in Django settings
7. Use docker-compose.prod.yml with production optimizations


