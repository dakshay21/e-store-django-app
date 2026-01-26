# EC2 Deployment Guide

This guide provides step-by-step instructions for deploying your Django REST Framework application to AWS EC2 using Docker and RDS PostgreSQL.

## Architecture Overview

```
Internet → EC2 (Nginx on Port 80) → Django Container (Port 8000) → RDS PostgreSQL
```

## Prerequisites

- AWS Account with appropriate permissions
- Docker Hub account (your image should already be pushed)
- SSH client installed on your local machine
- Basic knowledge of AWS Console

## Step 1: Create RDS PostgreSQL Database

**Note:** Create the database first so you have the connection details ready when setting up EC2.

### 1.1 Navigate to RDS Console

1. Log in to AWS Console
2. Search for "RDS" in the services search bar
3. Click on "RDS" service

### 1.2 Create Database

1. Click **"Create database"** button
2. Choose **"Standard create"** (not Easy create)
3. Select **"PostgreSQL"** as the database engine
4. Choose **PostgreSQL version**: 15.x or 16.x (recommended: 16.x)

### 1.3 Configure Database Settings

**Templates:**
- Select **"Free tier"** (if eligible) or **"Production"** for better performance

**Settings:**
- **DB instance identifier**: `drf-ecommerce-db` (or your preferred name)
- **Master username**: `postgres` (or your preferred username)
- **Master password**: Create a strong password and **save it securely**
  - You'll need this password later

**Instance configuration:**
- **DB instance class**: 
  - `db.t3.micro` (Free tier eligible, 1 vCPU, 1 GB RAM)
  - Or `db.t3.small` (2 vCPU, 2 GB RAM) for better performance

**Storage:**
- **Storage type**: `gp3` (General Purpose SSD)
- **Allocated storage**: `20` GB
- **Enable storage autoscaling**: ✅ Check this box
- **Maximum storage threshold**: `100` GB

**Connectivity:**
- **Virtual Private Cloud (VPC)**: Select your default VPC or create a new one
- **Subnet group**: Use default (or create custom)
- **Public access**: **No** (database should not be publicly accessible)
- **VPC security group**: 
  - Select **"Create new"**
  - Name: `rds-postgres-sg`
  - We'll configure this later to allow EC2 access

**Database authentication:**
- **Password authentication**: Selected by default

**Additional configuration:**
- **Initial database name**: `ecommerce_db` (or your preferred name)
- **DB parameter group**: Use default
- **Backup:**
  - **Enable automated backups**: ✅ Check (recommended)
  - **Backup retention period**: `7` days (free tier allows 7 days)
- **Encryption**: Enable encryption at rest (recommended)
- **Performance Insights**: Disable (optional, costs extra)
- **Enhanced monitoring**: Disable (optional)

### 1.4 Create Database

1. Review all settings
2. Click **"Create database"**
3. Wait 5-10 minutes for the database to be created
4. Note down the following information (you'll need it later):
   - **Endpoint**: e.g., `drf-ecommerce-db.xxxxx.us-east-1.rds.amazonaws.com`
   - **Port**: `5432` (default PostgreSQL port)
   - **Database name**: `ecommerce_db` (or what you set)
   - **Username**: `postgres` (or what you set)
   - **Password**: (the one you created)

### 1.5 Configure RDS Security Group

1. Once the database is created, go to **"Databases"** in RDS console
2. Click on your database instance
3. Scroll down to **"Connectivity & security"** tab
4. Click on the **Security group** link (e.g., `rds-postgres-sg`)
5. In the Security Group page:
   - Click **"Edit inbound rules"**
   - Click **"Add rule"**
   - **Type**: `PostgreSQL`
   - **Port**: `5432`
   - **Source**: 
     - Select **"Custom"**
     - We'll update this after creating EC2 to allow only EC2 security group
     - For now, select **"My IP"** or temporarily use the EC2 security group ID (we'll create it next)
   - Click **"Save rules"**

**Note:** After creating EC2, come back and update the source to the EC2 security group for better security.

---

## Step 2: Create EC2 Instance

### 2.1 Navigate to EC2 Console

1. In AWS Console, search for "EC2"
2. Click on **"EC2"** service

### 2.2 Launch Instance

1. Click **"Launch instance"** button
2. Click **"Launch instance"** from the dropdown

### 2.3 Configure Instance

**Name and tags:**
- **Name**: `drf-ecommerce-server` (or your preferred name)

**Application and OS Images (Amazon Machine Image):**
- Click **"Browse more AMIs"**
- Search for **"Amazon Linux 2023"** or **"Ubuntu Server 22.04 LTS"**
- Select the AMI (Amazon Linux 2023 is recommended for AWS integration)

**Instance type:**
- Select **"t3.small"** (2 vCPU, 2 GB RAM) - recommended
- Or **"t3.micro"** (1 vCPU, 1 GB RAM) - free tier eligible but may be slower
- Click **"Next"** to continue

**Key pair (login):**
- If you have an existing key pair, select it
- If not, click **"Create new key pair"**:
  - **Name**: `drf-ec2-key` (or your preferred name)
  - **Key pair type**: `RSA`
  - **Private key file format**: `.pem` (for OpenSSH)
  - Click **"Create key pair"**
  - **Download the .pem file** and save it securely
  - **Important:** You cannot download this again, so keep it safe!

**Network settings:**
- **VPC**: Select the same VPC where your RDS database is located
- **Subnet**: Select any public subnet
- **Auto-assign Public IP**: **Enable**
- **Firewall (security group):**
  - Click **"Create security group"**
  - **Security group name**: `ec2-web-server-sg`
  - **Description**: `Security group for DRF web server`
  
  **Inbound rules:**
  - Click **"Add security group rule"**
    - **Type**: `SSH`
    - **Source**: `My IP` (for security, only allow your IP)
  - Click **"Add security group rule"** again
    - **Type**: `HTTP`
    - **Source**: `Anywhere-IPv4` (0.0.0.0/0) - allows public access
  - **Outbound rules**: Leave default (All traffic)

**Configure storage:**
- **Volume size**: `20` GB (minimum)
- **Volume type**: `gp3` (General Purpose SSD)
- Click **"Next"** to continue

**Advanced details:**
- Leave defaults for now
- Click **"Launch instance"**

### 2.4 Wait for Instance to Start

1. Click **"View all instances"**
2. Wait for the instance status to change from **"Pending"** to **"Running"**
3. Note down the **Public IPv4 address** (e.g., `65.0.176.196`)
4. Note down the **Security group ID** (e.g., `sg-0b1c91060a79f555f`)

### 2.5 Update RDS Security Group

1. Go back to RDS Console
2. Click on your database instance
3. Click on the Security group link
4. Click **"Edit inbound rules"**
5. Edit the existing PostgreSQL rule:
   - **Source**: Change to **"Custom"**
   - Enter the **EC2 Security Group ID** (from step 2.4)
   - This allows only your EC2 instance to access the database
6. Click **"Save rules"**

---

## Step 3: Connect to EC2 Instance

### 3.1 Set Permissions for SSH Key

On your local machine (Linux/Mac):

```bash
chmod 400 /path/to/your/drf-ec2-key.pem
```

On Windows (using Git Bash or WSL):

```bash
chmod 400 /path/to/your/drf-ec2-key.pem
```

### 3.2 SSH into EC2 Instance

**For Amazon Linux 2023:**

```bash
ssh -i /path/to/your/drf-ec2-key.pem ec2-user@<EC2_PUBLIC_IP>
```

**For Ubuntu 22.04:**

```bash
ssh -i /path/to/your/drf-ec2-key.pem ubuntu@<EC2_PUBLIC_IP>
```

Replace `<EC2_PUBLIC_IP>` with your actual EC2 public IP address.

**First time connection:**
- You may see a message about authenticity of host, type `yes` to continue

---

## Step 4: Install Docker and Docker Compose on EC2

### 4.1 Update System Packages

**For Amazon Linux 2023:**

```bash
sudo yum update -y
```

**For Ubuntu 22.04:**

```bash
sudo apt update && sudo apt upgrade -y
```

### 4.2 Install Docker Engine

**For Amazon Linux 2023:**

```bash
# Install Docker
sudo yum install docker -y

# Start Docker service
sudo systemctl start docker

# Enable Docker to start on boot
sudo systemctl enable docker

# Add ec2-user to docker group (so you can run docker without sudo)
sudo usermod -aG docker ec2-user

# Log out and log back in for group changes to take effect
exit
```

Then SSH back in:

```bash
ssh -i /path/to/your/drf-ec2-key.pem ec2-user@<EC2_PUBLIC_IP>
```

**For Ubuntu 22.04:**

```bash
# Remove old versions if any
sudo apt remove docker docker-engine docker.io containerd runc -y

# Install prerequisites
sudo apt update
sudo apt install ca-certificates curl gnupg lsb-release -y

# Add Docker's official GPG key
sudo mkdir -p /etc/apt/keyrings
curl -fsSL https://download.docker.com/linux/ubuntu/gpg | sudo gpg --dearmor -o /etc/apt/keyrings/docker.gpg

# Set up Docker repository
echo \
  "deb [arch=$(dpkg --print-architecture) signed-by=/etc/apt/keyrings/docker.gpg] https://download.docker.com/linux/ubuntu \
  $(lsb_release -cs) stable" | sudo tee /etc/apt/sources.list.d/docker.list > /dev/null

# Install Docker Engine and Docker Compose plugin
sudo apt update
sudo apt install docker-ce docker-ce-cli containerd.io docker-buildx-plugin docker-compose-plugin -y

# Start Docker service
sudo systemctl start docker

# Enable Docker to start on boot
sudo systemctl enable docker

# Add ubuntu user to docker group
sudo usermod -aG docker ubuntu

# Log out and log back in for group changes to take effect
exit
```

Then SSH back in:

```bash
ssh -i /path/to/your/drf-ec2-key.pem ubuntu@<EC2_PUBLIC_IP>
```

### 4.3 Verify Docker Installation

```bash
docker --version
docker ps
```

You should see Docker version and an empty container list.

### 4.4 Verify Docker Compose Installation

**For Amazon Linux 2023:**

```bash
# Verify Docker Compose plugin is installed
docker compose version
```

**For Ubuntu 22.04:**

```bash
# Verify Docker Compose plugin is installed
docker compose version
```

You should see Docker Compose version (v2.x.x). If you see an error, the plugin was installed as part of Docker Engine installation above.

---

## Step 5: Set Up Deployment Directory

### 5.1 Create Project Directory

```bash
mkdir -p ~/drf-deployment
cd ~/drf-deployment
```

### 5.2 Create docker-compose.prod.yml

Create the file:

```bash
nano docker-compose.prod.yml
```

Copy and paste the following content (adjust the image name if different):

```yaml
services:
  web:
    # Use the image from Docker Hub (built by CI/CD)
    image: ${DOCKERHUB_REPOSITORY:-dakshay111/drf-pipeline-deployment}:latest
    # Pull the latest image
    pull_policy: always
    # No volume mounts - code is in the image
    volumes:
      - static_volume:/app/staticfiles
      - media_volume:/app/media
    expose:
      - "8000"
    environment:
      # Database configuration (RDS)
      - DB_NAME=${DB_NAME}
      - DB_USER=${DB_USER}
      - DB_PASSWORD=${DB_PASSWORD}
      - DB_HOST=${DB_HOST}
      - DB_PORT=${DB_PORT:-5432}
      # Django settings
      - SECRET_KEY=${SECRET_KEY}
      - DEBUG=${DEBUG:-False}
      - ALLOWED_HOSTS=${ALLOWED_HOSTS}
      # Gunicorn settings
      - GUNICORN_WORKERS=${GUNICORN_WORKERS:-4}
      - GUNICORN_TIMEOUT=${GUNICORN_TIMEOUT:-30}
      - GUNICORN_MAX_REQUESTS=${GUNICORN_MAX_REQUESTS:-1000}
      - GUNICORN_MAX_REQUESTS_JITTER=${GUNICORN_MAX_REQUESTS_JITTER:-50}
      # Optional: Set to true to populate initial data on first run
      - POPULATE_DATA=${POPULATE_DATA:-false}
      - LOG_LEVEL=${LOG_LEVEL:-info}
    restart: unless-stopped
    networks:
      - app-network
    # Health check
    healthcheck:
      test: ["CMD", "pg_isready", "-h", "${DB_HOST}", "-p", "${DB_PORT:-5432}", "-U", "${DB_USER}"]
      interval: 30s
      timeout: 10s
      retries: 3
      start_period: 40s

  nginx:
    image: nginx:alpine
    volumes:
      - ./nginx.conf:/etc/nginx/nginx.conf:ro
      - static_volume:/app/staticfiles:ro
      - media_volume:/app/media:ro
    ports:
      - "${NGINX_PORT:-80}:80"
    depends_on:
      web:
        condition: service_healthy
    restart: unless-stopped
    networks:
      - app-network

volumes:
  static_volume:
  media_volume:

networks:
  app-network:
    driver: bridge
```

Save and exit:
- Press `Ctrl + X`
- Press `Y` to confirm
- Press `Enter` to save

### 5.3 Create nginx.conf

```bash
nano nginx.conf
```

Copy and paste the following content:

```nginx
events {
    worker_connections 1024;
}

http {
    include /etc/nginx/mime.types;
    default_type application/octet-stream;

    # Logging
    access_log /var/log/nginx/access.log;
    error_log /var/log/nginx/error.log;

    # Performance optimizations
    sendfile on;
    tcp_nopush on;
    tcp_nodelay on;
    keepalive_timeout 65;
    types_hash_max_size 2048;

    # Gzip compression
    gzip on;
    gzip_vary on;
    gzip_proxied any;
    gzip_comp_level 6;
    gzip_types text/plain text/css text/xml text/javascript application/json application/javascript application/xml+rss application/rss+xml font/truetype font/opentype application/vnd.ms-fontobject image/svg+xml;

    upstream web {
        server web:8000;
    }

    server {
        listen 80;
        server_name localhost;

        client_max_body_size 100M;

        # Security headers
        add_header X-Frame-Options "SAMEORIGIN" always;
        add_header X-Content-Type-Options "nosniff" always;
        add_header X-XSS-Protection "1; mode=block" always;

        location / {
            proxy_pass http://web;
            proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
            proxy_set_header Host $host;
            proxy_set_header X-Real-IP $remote_addr;
            proxy_set_header X-Forwarded-Proto $scheme;
            proxy_redirect off;
            
            # Timeout settings
            proxy_connect_timeout 60s;
            proxy_send_timeout 60s;
            proxy_read_timeout 60s;
        }

        location /static/ {
            alias /app/staticfiles/;
            expires 30d;
            add_header Cache-Control "public, immutable";
        }

        location /media/ {
            alias /app/media/;
            expires 30d;
            add_header Cache-Control "public, immutable";
        }
    }
}
```

Save and exit (Ctrl + X, Y, Enter).

### 5.4 Create .env File

```bash
nano .env
```

Add the following content (replace with your actual values):

```bash
# Docker Hub Repository
DOCKERHUB_REPOSITORY=dakshay111/drf-pipeline-deployment

# Database Configuration (from RDS)
DB_NAME=ecommerce_db
DB_USER=postgres
DB_PASSWORD=your_rds_password_here
DB_HOST=drf-ecommerce-db.xxxxx.us-east-1.rds.amazonaws.com
DB_PORT=5432

# Django Settings
SECRET_KEY=your-django-secret-key-here-generate-a-strong-random-key
DEBUG=False
ALLOWED_HOSTS=your-ec2-public-ip,54.123.45.67

# Gunicorn Settings
GUNICORN_WORKERS=4
GUNICORN_TIMEOUT=30
GUNICORN_MAX_REQUESTS=1000
GUNICORN_MAX_REQUESTS_JITTER=50

# Optional Settings
POPULATE_DATA=false
LOG_LEVEL=info
NGINX_PORT=80
```

**Important values to replace:**
- `DOCKERHUB_REPOSITORY`: Your Docker Hub repository name
- `DB_PASSWORD`: The RDS master password you created
- `DB_HOST`: The RDS endpoint (from Step 1.4)
- `SECRET_KEY`: Generate a strong random key (see below)
- `ALLOWED_HOSTS`: Your EC2 public IP address

**Generate Django Secret Key:**

You can generate a secret key using Python:

```bash
python3 -c "from django.core.management.utils import get_random_secret_key; print(get_random_secret_key())"
```

Or use an online generator, or run this on your local machine if you have Django installed.

Save and exit (Ctrl + X, Y, Enter).

### 5.5 Set Secure Permissions for .env

```bash
chmod 600 .env
```

This restricts access to only the owner (you).

---

## Step 6: Deploy Application

### 6.1 Pull Docker Image

```bash
cd ~/drf-deployment
docker pull dakshay111/drf-pipeline-deployment:latest
```

Replace `dakshay111/drf-pipeline-deployment` with your actual Docker Hub repository name.

### 6.2 Start Services

```bash
docker compose -f docker-compose.prod.yml up -d
```

The `-d` flag runs containers in detached mode (in the background).

### 6.3 Check Container Status

```bash
docker compose -f docker-compose.prod.yml ps
```

You should see both `web` and `nginx` containers running.

### 6.4 View Logs

```bash
# View all logs
docker compose -f docker-compose.prod.yml logs -f

# View only web container logs
docker compose -f docker-compose.prod.yml logs -f web

# View only nginx logs
docker compose -f docker-compose.prod.yml logs -f nginx
```

Press `Ctrl + C` to exit log viewing.

---

## Step 7: Verify Deployment

### 7.1 Check Application Health

From your local machine, open a web browser and visit:

```
http://<EC2_PUBLIC_IP>
```

Or use curl:

```bash
curl http://<EC2_PUBLIC_IP>
```

You should see a response from your Django application.

### 7.2 Test API Endpoints

If you have API endpoints, test them:

```bash
curl http://<EC2_PUBLIC_IP>/api/products/
```

### 7.3 Check Database Connection

SSH into EC2 and check if the web container can connect to the database:

```bash
docker compose -f docker-compose.prod.yml exec web python manage.py dbshell
```

If connected, you'll see a PostgreSQL prompt. Type `\q` to exit.

### 7.4 Verify Static Files

Check if static files are being served:

```bash
curl http://<EC2_PUBLIC_IP>/static/
```

---

## Step 8: Manual Deployment (Updates)

When you need to deploy updates after pushing new code:

### 8.1 Pull Latest Image

```bash
cd ~/drf-deployment
docker pull dakshay111/drf-pipeline-deployment:latest
```

### 8.2 Restart Services

```bash
docker compose -f docker-compose.prod.yml down
docker compose -f docker-compose.prod.yml up -d
```

### 8.3 Verify Update

```bash
docker compose -f docker-compose.prod.yml logs -f web
```

Check the logs to ensure the new version is running.

---

## Troubleshooting

### Issue: Cannot connect to database from local machine

**Symptoms:** Database client (DBeaver, pgAdmin, etc.) cannot connect to RDS, shows connection timeout or host unreachable.

**Root Cause:** RDS instance was created with "Public access: No", which means it's only accessible from within the AWS VPC, not from your local machine.

**Solutions:**

#### Option 1: Enable Public Access (Easiest for Development)

1. Go to AWS RDS Console
2. Select your database instance
3. Click **"Modify"**
4. Under **"Connectivity"**, expand **"Additional connectivity configuration"**
5. Set **"Public access"** to **"Yes"**
6. Click **"Continue"** and **"Modify DB instance"**
7. Wait 5-10 minutes for the change to apply
8. Update RDS Security Group:
   - Go to RDS → Your database → Security group
   - Edit inbound rules
   - Add rule: Type `PostgreSQL`, Port `5432`, Source `My IP` (or `0.0.0.0/0` for any IP - less secure)
   - Save rules
9. Try connecting again from your database client

**Note:** This makes your database publicly accessible. Only use this for development/testing. For production, use Option 2 or 3.

#### Option 2: Use SSH Tunnel Through EC2 (Recommended for Production)

This allows you to connect securely through your EC2 instance without making RDS publicly accessible.

**Step 1: Configure SSH Tunnel in your database client**

In DBeaver or pgAdmin, use the **"SSH Tunnel"** tab:

- **Host**: Your EC2 public IP address
- **Port**: `22`
- **User**: `ec2-user` (Amazon Linux) or `ubuntu` (Ubuntu)
- **Authentication**: Use your EC2 private key file (`.pem` file)

**Step 2: Configure Database Connection**

- **Host**: RDS endpoint (e.g., `drf-ecommerce-db.cl8eq0qosk5o.ap-south-1.rds.amazonaws.com`)
- **Port**: `5432`
- **Database**: `ecommerce_db`
- **Username**: `postgres`
- **Password**: Your RDS master password

**Step 3: Test Connection**

The SSH tunnel will forward your local connection through EC2 to RDS.

#### Option 3: Connect from EC2 Instance

SSH into your EC2 instance and connect from there:

```bash
# SSH into EC2
ssh -i /path/to/your/drf-ec2-key.pem ec2-user@<EC2_IP>

# Install PostgreSQL client (if not already installed)
# Amazon Linux
sudo yum install postgresql15 -y

# Ubuntu
sudo apt install postgresql-client -y

# Connect to RDS
psql -h drf-ecommerce-db.cl8eq0qosk5o.ap-south-1.rds.amazonaws.com \
     -U postgres \
     -d ecommerce_db \
     -p 5432
```

Enter your RDS password when prompted.

#### Option 4: Use AWS Systems Manager Session Manager

If you have Session Manager configured, you can use port forwarding:

```bash
aws ssm start-session \
    --target <EC2_INSTANCE_ID> \
    --document-name AWS-StartPortForwardingSessionToRemoteHost \
    --parameters '{"host":["drf-ecommerce-db.cl8eq0qosk5o.ap-south-1.rds.amazonaws.com"],"portNumber":["5432"],"localPortNumber":["5432"]}'
```

Then connect to `localhost:5432` from your database client.

### Issue: Cannot connect to database (from EC2/Container)

**Symptoms:** Container fails to start, logs show database connection errors.

**Solutions:**
1. Verify RDS security group allows EC2 security group on port 5432
2. Check DB_HOST, DB_USER, DB_PASSWORD in `.env` file
3. Verify RDS instance is running and accessible
4. Test connection from EC2:
   ```bash
   psql -h <DB_HOST> -U <DB_USER> -d <DB_NAME> -p 5432
   ```
5. Verify RDS and EC2 are in the same VPC
6. Check RDS security group inbound rules allow EC2 security group

### Issue: 502 Bad Gateway

**Symptoms:** Browser shows 502 error, nginx can't reach Django.

**Solutions:**
1. Check if web container is running:
   ```bash
   docker compose -f docker-compose.prod.yml ps
   ```
2. Check web container logs:
   ```bash
   docker compose -f docker-compose.prod.yml logs web
   ```
3. Verify database connection (see above)
4. Check if web container is healthy:
   ```bash
   docker compose -f docker-compose.prod.yml ps
   ```
   Look for "healthy" status

### Issue: Static files not loading

**Symptoms:** CSS/JS files return 404.

**Solutions:**
1. Ensure static files are collected:
   ```bash
   docker compose -f docker-compose.prod.yml exec web python manage.py collectstatic --noinput
   ```
2. Check nginx.conf volume mount is correct
3. Verify static_volume exists:
   ```bash
   docker volume ls
   ```

### Issue: Permission denied errors

**Symptoms:** Container can't write to volumes.

**Solutions:**
1. Check volume permissions:
   ```bash
   docker compose -f docker-compose.prod.yml exec web ls -la /app/staticfiles
   ```
2. Recreate volumes if needed:
   ```bash
   docker compose -f docker-compose.prod.yml down -v
   docker compose -f docker-compose.prod.yml up -d
   ```

### Issue: Container keeps restarting

**Symptoms:** Container status shows "Restarting" repeatedly.

**Solutions:**
1. Check logs for errors:
   ```bash
   docker compose -f docker-compose.prod.yml logs web
   ```
2. Verify all environment variables are set correctly in `.env`
3. Check database connectivity
4. Verify SECRET_KEY is set and valid

### Issue: Cannot SSH into EC2

**Symptoms:** SSH connection times out or is refused.

**Solutions:**
1. Verify EC2 security group allows SSH from your IP
2. Check if EC2 instance is running
3. Verify you're using the correct key file:
   ```bash
   ssh -i /path/to/key.pem ec2-user@<EC2_IP>
   ```
4. Check EC2 instance status in AWS Console

### Issue: Port 80 not accessible

**Symptoms:** Cannot access application via HTTP.

**Solutions:**
1. Verify security group allows inbound traffic on port 80
2. Check if nginx container is running:
   ```bash
   docker compose -f docker-compose.prod.yml ps nginx
   ```
3. Check nginx logs:
   ```bash
   docker compose -f docker-compose.prod.yml logs nginx
   ```
4. Test from within EC2:
   ```bash
   curl http://localhost
   ```

---

## Useful Commands Reference

### Docker Compose Commands

```bash
# Start services
docker compose -f docker-compose.prod.yml up -d

# Stop services
docker compose -f docker-compose.prod.yml down

# View logs
docker compose -f docker-compose.prod.yml logs -f

# Restart services
docker compose -f docker-compose.prod.yml restart

# View container status
docker compose -f docker-compose.prod.yml ps

# Execute command in container
docker compose -f docker-compose.prod.yml exec web <command>

# Pull latest images
docker compose -f docker-compose.prod.yml pull
```

### Django Management Commands

```bash
# Run migrations
docker compose -f docker-compose.prod.yml exec web python manage.py migrate

# Collect static files
docker compose -f docker-compose.prod.yml exec web python manage.py collectstatic --noinput

# Create superuser
docker compose -f docker-compose.prod.yml exec web python manage.py createsuperuser

# Access Django shell
docker compose -f docker-compose.prod.yml exec web python manage.py shell

# Access database shell
docker compose -f docker-compose.prod.yml exec web python manage.py dbshell
```

### System Commands

```bash
# Check disk space
df -h

# Check memory usage
free -h

# Check Docker disk usage
docker system df

# Clean up unused Docker resources
docker system prune -a

# View system logs
sudo journalctl -u docker
```

---

## Security Best Practices

1. **Keep .env file secure:**
   - Never commit `.env` to version control
   - Use `chmod 600 .env` to restrict access
   - Consider using AWS Secrets Manager for production

2. **Update system regularly:**
   ```bash
   # Amazon Linux
   sudo yum update -y
   
   # Ubuntu
   sudo apt update && sudo apt upgrade -y
   ```

3. **Restrict SSH access:**
   - Only allow your IP in EC2 security group for SSH
   - Use key-based authentication (already configured)

4. **Monitor logs:**
   - Regularly check application and nginx logs
   - Set up CloudWatch alarms for critical errors

5. **Backup database:**
   - RDS automated backups are enabled
   - Consider manual snapshots before major updates

6. **Use HTTPS (Future):**
   - Set up SSL certificate using Let's Encrypt
   - Configure nginx for HTTPS
   - Update security group for port 443

---

## Step 9: Set Up Automated Deployment with GitHub Actions

After completing the manual deployment, you can set up automated deployment that triggers whenever you push code to the main branch.

### 9.1 Generate SSH Key Pair for GitHub Actions

On your local machine, generate a new SSH key pair specifically for GitHub Actions:

```bash
ssh-keygen -t rsa -b 4096 -C "github-actions-deploy" -f ~/.ssh/github-actions-ec2-key
```

This creates two files:
- `~/.ssh/github-actions-ec2-key` (private key - add to GitHub Secrets)
- `~/.ssh/github-actions-ec2-key.pub` (public key - add to EC2)

### 9.2 Add Public Key to EC2

Copy the public key to your EC2 instance:

```bash
# Copy public key to EC2
cat ~/.ssh/github-actions-ec2-key.pub | ssh -i /path/to/your/drf-ec2-key.pem ec2-user@<EC2_IP> "cat >> ~/.ssh/authorized_keys"
```

Or manually:
1. SSH into EC2
2. Edit `~/.ssh/authorized_keys`:
   ```bash
   nano ~/.ssh/authorized_keys
   ```
3. Paste the public key content
4. Save and exit

### 9.3 Configure GitHub Secrets

1. Go to your GitHub repository
2. Navigate to **Settings** → **Secrets and variables** → **Actions**
3. Click **"New repository secret"** and add the following secrets:

   **EC2_HOST:**
   - Name: `EC2_HOST`
   - Value: Your EC2 public IP address (e.g., `54.123.45.67`)

   **EC2_USER:**
   - Name: `EC2_USER`
   - Value: `ec2-user` (for Amazon Linux) or `ubuntu` (for Ubuntu)

   **EC2_SSH_KEY:**
   - Name: `EC2_SSH_KEY`
   - Value: The **private key** content from `~/.ssh/github-actions-ec2-key`
     ```bash
     cat ~/.ssh/github-actions-ec2-key
     ```
     Copy the entire output including `-----BEGIN OPENSSH PRIVATE KEY-----` and `-----END OPENSSH PRIVATE KEY-----`

   **DOCKERHUB_REPOSITORY:**
   - Name: `DOCKERHUB_REPOSITORY`
   - Value: Your Docker Hub repository name (e.g., `dakshay111/drf-pipeline-deployment`)
   - Note: This should already exist if you set up the Docker Hub push workflow

### 9.4 How It Works

The automated deployment workflow (`.github/workflows/deploy-ec2.yml`) will:

1. **Trigger automatically** after the "Build and Push to Docker Hub" workflow completes successfully
2. **SSH into your EC2 instance** using the configured credentials
3. **Pull the latest Docker image** from Docker Hub
4. **Restart the containers** with the new image
5. **Perform health checks** to verify the deployment
6. **Clean up old Docker images** to save space

### 9.5 Manual Trigger

You can also manually trigger the deployment:

1. Go to **Actions** tab in your GitHub repository
2. Select **"Deploy to EC2"** workflow
3. Click **"Run workflow"** button
4. Select the branch (usually `main`)
5. Click **"Run workflow"**

### 9.6 Verify Automated Deployment

After pushing code to the main branch:

1. Go to **Actions** tab in GitHub
2. You should see two workflows:
   - "Build and Push to Docker Hub" (builds and pushes image)
   - "Deploy to EC2" (deploys to your server)
3. Click on the "Deploy to EC2" workflow to see the deployment progress
4. Check the logs to ensure deployment succeeded

### 9.7 Troubleshooting GitHub Actions Deployment

**Issue: SSH connection fails**

- Verify `EC2_HOST` secret is correct (use IP address, not domain)
- Verify `EC2_USER` matches your AMI (ec2-user for Amazon Linux, ubuntu for Ubuntu)
- Check that public key is in `~/.ssh/authorized_keys` on EC2
- Verify EC2 security group allows SSH from GitHub Actions IPs (or use 0.0.0.0/0 temporarily for testing)

**Issue: Deployment directory not found**

- Ensure you created `~/drf-deployment` directory on EC2
- Verify the directory contains `docker-compose.prod.yml` and `nginx.conf`

**Issue: Docker pull fails**

- Verify `DOCKERHUB_REPOSITORY` secret is correct
- Check that the Docker image exists in Docker Hub
- Ensure EC2 instance has internet access

**Issue: Health check fails**

- Check application logs on EC2: `docker compose -f docker-compose.prod.yml logs`
- Verify database connection is working
- Check if port 80 is accessible from EC2 itself: `curl http://localhost`

---

## Next Steps

1. ✅ **Set up automated deployment** using GitHub Actions (completed above)
2. **Configure domain name** and set up SSL/HTTPS
3. **Set up monitoring** with CloudWatch
4. **Configure backups** and disaster recovery plan
5. **Set up CI/CD pipeline** for automated testing and deployment

---

## Cost Optimization Tips

1. **Use t3.micro for EC2** if free tier eligible
2. **Use db.t3.micro for RDS** if free tier eligible
3. **Stop EC2 instance** when not in use (development/testing)
4. **Enable RDS automated backups** but set appropriate retention
5. **Monitor data transfer** costs
6. **Use Reserved Instances** for long-term deployments (saves up to 75%)

---

## Support

If you encounter issues not covered in this guide:

1. Check Docker logs: `docker compose -f docker-compose.prod.yml logs`
2. Check AWS CloudWatch logs
3. Review Django application logs
4. Verify all environment variables are correct
5. Check AWS service health dashboard

---

**Last Updated:** January 2026
