# Deployment Workflow Checklist

This checklist ensures everything is ready for the self-hosted runner deployment workflow.

## ✅ Pre-Deployment Requirements

### 1. EC2 Instance Setup

- [ ] EC2 instance is running
- [ ] Docker is installed and working (`docker --version`)
- [ ] Docker Compose is installed and working (`docker compose version`)
- [ ] Runner user can run docker without sudo (user in docker group)
- [ ] `curl` is installed (for health checks)

**To check docker permissions:**
```bash
docker ps
# If it fails with permission error, run:
sudo usermod -aG docker $USER
# Then restart the runner service
sudo systemctl restart actions.runner.*
```

### 2. Deployment Directory Structure

On EC2, ensure `~/drf-deployment` exists with:

- [ ] `docker-compose.prod.yml` file
- [ ] `nginx.conf` file  
- [ ] `.env` file with all required variables

**Verify:**
```bash
ls -la ~/drf-deployment/
# Should show:
# - docker-compose.prod.yml
# - nginx.conf
# - .env
```

### 3. .env File Configuration

The `.env` file must contain:

- [ ] `DOCKERHUB_REPOSITORY` - Your Docker Hub repo name
- [ ] `DB_NAME` - RDS database name
- [ ] `DB_USER` - RDS username
- [ ] `DB_PASSWORD` - RDS password
- [ ] `DB_HOST` - RDS endpoint
- [ ] `DB_PORT` - RDS port (usually 5432)
- [ ] `SECRET_KEY` - Django secret key
- [ ] `DEBUG=False`
- [ ] `ALLOWED_HOSTS` - EC2 public IP or domain

**Verify .env file:**
```bash
cd ~/drf-deployment
cat .env | grep -v PASSWORD  # Shows all vars except password
```

### 4. GitHub Secrets

In GitHub repository: **Settings** → **Secrets and variables** → **Actions**

- [ ] `DOCKERHUB_REPOSITORY` - Your Docker Hub repository name (e.g., `dakshay111/drf-pipeline-deployment`)

**That's the only secret needed!** No AWS credentials, no SSH keys, no EC2 instance IDs.

### 5. GitHub Runner

- [ ] Runner is installed on EC2
- [ ] Runner service is running (`sudo systemctl status actions.runner.*`)
- [ ] Runner appears as "Online" in GitHub (Settings → Actions → Runners)

**Check runner status:**
```bash
cd ~/actions-runner
sudo ./svc.sh status
```

### 6. Network & Security

- [ ] EC2 security group allows HTTP (port 80) from `0.0.0.0/0`
- [ ] RDS security group allows PostgreSQL (port 5432) from EC2 security group
- [ ] EC2 can reach Docker Hub (test: `docker pull hello-world`)

## ✅ Workflow File

The workflow file `.github/workflows/deploy-ec2-runner.yml` includes:

- [x] Prerequisites verification (Docker, Docker Compose)
- [x] File existence checks (docker-compose.prod.yml, nginx.conf, .env)
- [x] Environment variable validation
- [x] Error handling and logging
- [x] Health checks
- [x] Automatic cleanup of old Docker images

## 🧪 Testing the Setup

### Test 1: Manual Deployment

1. Go to **Actions** → **Deploy to EC2 (Self-Hosted Runner)**
2. Click **"Run workflow"**
3. Select branch: `main`
4. Click **"Run workflow"**
5. Watch the workflow execute on your self-hosted runner

### Test 2: Automatic Deployment

1. Make a small change to your code
2. Commit and push to `main` branch
3. Watch "Build and Push to Docker Hub" workflow
4. After it completes, "Deploy to EC2" should automatically start
5. Verify deployment succeeded

### Test 3: Verify Application

After deployment:

```bash
# SSH into EC2
ssh -i /path/to/key.pem ubuntu@<EC2_IP>

# Check containers are running
cd ~/drf-deployment
docker compose -f docker-compose.prod.yml ps

# Check logs
docker compose -f docker-compose.prod.yml logs -f

# Test from browser
curl http://localhost
```

## 🔍 Troubleshooting

### Issue: Workflow doesn't trigger

**Check:**
- Runner is online in GitHub
- Workflow file is in `.github/workflows/` directory
- Workflow file has correct name: `deploy-ec2-runner.yml`
- "Build and Push to Docker Hub" workflow completed successfully

### Issue: "Deployment directory not found"

**Solution:**
```bash
mkdir -p ~/drf-deployment
# Copy files from your repo or create them manually
```

### Issue: "docker-compose.prod.yml not found"

**Solution:**
```bash
cd ~/drf-deployment
# Copy docker-compose.prod.yml from your repository
```

### Issue: ".env file not found"

**Solution:**
```bash
cd ~/drf-deployment
nano .env
# Add all required environment variables
chmod 600 .env
```

### Issue: "Cannot run docker commands"

**Solution:**
```bash
# Add user to docker group
sudo usermod -aG docker $USER

# Restart runner service
cd ~/actions-runner
sudo ./svc.sh restart

# Or log out and back in
```

### Issue: "Failed to pull image"

**Check:**
- `DOCKERHUB_REPOSITORY` secret is correct
- Image exists in Docker Hub
- EC2 has internet connectivity
- Docker Hub is accessible

### Issue: "Failed to start containers"

**Check logs:**
```bash
cd ~/drf-deployment
docker compose -f docker-compose.prod.yml logs
```

**Common causes:**
- Missing environment variables in `.env`
- Database connection issues
- Port conflicts
- Invalid docker-compose.prod.yml syntax

### Issue: "Health check failed"

**Check:**
- Containers are running: `docker compose -f docker-compose.prod.yml ps`
- Application logs: `docker compose -f docker-compose.prod.yml logs web`
- Nginx logs: `docker compose -f docker-compose.prod.yml logs nginx`
- Port 80 is accessible: `curl http://localhost`

## 📋 Quick Verification Commands

Run these on EC2 to verify everything is ready:

```bash
# 1. Check Docker
docker --version && docker compose version

# 2. Check Docker permissions
docker ps

# 3. Check deployment directory
ls -la ~/drf-deployment/

# 4. Check .env file exists
test -f ~/drf-deployment/.env && echo "✅ .env exists" || echo "❌ .env missing"

# 5. Check runner status
cd ~/actions-runner && sudo ./svc.sh status

# 6. Test Docker Hub connectivity
docker pull hello-world
```

## ✅ Ready to Deploy!

Once all items are checked, your workflow is ready to use. The workflow will:

1. ✅ Verify prerequisites automatically
2. ✅ Check all required files exist
3. ✅ Pull latest Docker image
4. ✅ Stop old containers
5. ✅ Start new containers
6. ✅ Perform health checks
7. ✅ Clean up old images

---

**Last Updated:** January 2026
