# 🚀 Deployment Guide for Gas Utility Service

This guide covers deploying the Gas Utility Service application to various hosting platforms, with a focus on Render.

## 🔧 Preparing for Deployment

Before deploying the application, ensure:

1. **Configuration**: Update `settings.py`:
   - Set `DEBUG = False`
   - Configure `ALLOWED_HOSTS`
   - Use a secure `SECRET_KEY`

2. **Static Files**: Run `python manage.py collectstatic` to collect all static files.

3. **Database**: For production, use PostgreSQL instead of SQLite.

4. **Environment Variables**: Set up environment variables based on `.env.example`.

## 📋 Deployment on Render (Recommended)

Render offers a straightforward deployment process for Django applications with a generous free tier.

### Prerequisites
- A [Render account](https://render.com/)
- Your code pushed to GitHub

### Step-by-Step Deployment

1. **Create a New Web Service**:
   - Log in to Render and click "New +"
   - Select "Web Service"
   - Connect your GitHub repository

2. **Configure the Service**:
   - **Name**: `gas-utility-service` (or choose your own)
   - **Environment**: Python 3
   - **Region**: Choose closest to your users
   - **Branch**: master
   - **Build Command**: `chmod +x build_files/build.sh && ./build_files/build.sh`
   - **Start Command**: `gunicorn gas_utility_service.wsgi:application`
   - **Plan**: Free

3. **Set Environment Variables**:
   - Click on "Environment" tab
   - Add these variables:
     ```
     SECRET_KEY=<generate-a-secure-random-key>
     DEBUG=False
     ALLOWED_HOSTS=gas-utility-service.onrender.com,*.onrender.com
     ```

4. **Add a PostgreSQL Database**:
   - Click "New +" again and select "PostgreSQL"
   - Use Free plan
   - Name it `gas-utility-db`
   - Render will automatically link the database to your web service

5. **Deploy Your Application**:
   - Click "Create Web Service"
   - Wait for the build and deployment to complete (5-10 minutes)

6. **Create a Support User**:
   - Visit your application URL at `https://gas-utility-service.onrender.com/support/create-default-user/`
   - This will create a default support user with username `support_admin` and password `support_password123`

7. **Access Your Application**:
   - Your app will be available at `https://gas-utility-service.onrender.com`

### 📝 Notes on Render Free Tier
- The app will "sleep" after 15 minutes of inactivity
- The first request after inactivity will take longer to respond
- You get 750 hours of free usage per month
- PostgreSQL databases on the free tier are limited to 1GB storage

## 🌐 Alternative Deployment Options

### 1. VPS Deployment (Digital Ocean, AWS EC2, etc.)

#### Prerequisites
- A VPS running Ubuntu/Debian
- Domain name (optional but recommended)

#### Steps
1. **Set up your server**:
   ```bash
   sudo apt update
   sudo apt install python3-pip python3-dev libpq-dev postgresql postgresql-contrib nginx
   ```

2. Create a PostgreSQL database and user.

3. **Set up a Python virtual environment**:
   ```bash
   python3 -m venv env
   source env/bin/activate
   pip install -r requirements.txt
   ```

4. **Configure environment variables** in a `.env` file.

5. **Collect static files and run migrations**:
   ```bash
   python manage.py collectstatic
   python manage.py migrate
   ```

6. **Configure Nginx and Gunicorn**:
   - Create a systemd service for Gunicorn
   - Set up Nginx as a reverse proxy

7. **Set up SSL with Let's Encrypt**:
   ```bash
   sudo apt install certbot python3-certbot-nginx
   sudo certbot --nginx -d your-domain.com
   ```

### 2. Docker Deployment

For containerized deployment:

1. **Build and run with Docker Compose**:
   ```bash
   docker-compose up -d
   ```

2. **Create a support user**:
   ```bash
   docker-compose exec web python manage.py create_support_user
   ```

3. **Access the application** at `http://localhost:8000` or your domain.

## 🔒 Security Considerations

For production deployments:

1. **Always use HTTPS** in production
2. **Secure environment variables** and never expose sensitive information
3. **Keep dependencies updated** to avoid security vulnerabilities
4. **Configure database backups** for data protection
5. **Set up proper logging** for monitoring

## 🔍 Troubleshooting

- **Check logs**: Render provides logs for debugging
- **Verify environment variables**: Misconfigured variables often cause issues
- **Confirm database connection**: Test database connectivity
- **Check allowed hosts**: Ensure your domain is in the ALLOWED_HOSTS setting

For additional assistance, refer to the [Render documentation](https://render.com/docs) or open an issue on GitHub. 