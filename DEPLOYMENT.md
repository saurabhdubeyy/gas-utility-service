# Deployment Guide for Gas Utility Service

This guide covers deploying the Gas Utility Service application to various hosting platforms.

## Preparing for Deployment

1. **Update Settings**: Ensure your `settings.py` is configured correctly:
   - Set `DEBUG = False`
   - Configure `ALLOWED_HOSTS`
   - Set up a secure `SECRET_KEY`

2. **Static Files**: Run `python manage.py collectstatic` to collect all static files.

3. **Database**: Consider migrating to PostgreSQL for production use.

4. **Environment Variables**: Set up environment variables based on `.env.example`.

## Deployment Options

### 1. Heroku Deployment

Heroku offers simple deployment for Django applications.

#### Requirements
- Heroku CLI installed
- Git repository initialized
- Procfile (already provided)
- requirements.txt (already updated)
- runtime.txt (already provided)

#### Steps
1. Create a Heroku app:
   ```
   heroku create your-app-name
   ```

2. Set environment variables:
   ```
   heroku config:set SECRET_KEY=your-secret-key-here
   heroku config:set DEBUG=False
   heroku config:set ALLOWED_HOSTS=your-app-name.herokuapp.com
   ```

3. Add PostgreSQL:
   ```
   heroku addons:create heroku-postgresql:mini
   ```

4. Deploy your application:
   ```
   git push heroku master
   ```

5. Run migrations:
   ```
   heroku run python manage.py migrate
   ```

6. Create a superuser:
   ```
   heroku run python manage.py createsuperuser
   ```

### 2. VPS Deployment (Digital Ocean, AWS EC2, etc.)

#### Prerequisites
- A VPS running Ubuntu/Debian
- Domain name (optional but recommended)

#### Steps
1. Set up your server:
   ```bash
   sudo apt update
   sudo apt install python3-pip python3-dev libpq-dev postgresql postgresql-contrib nginx
   ```

2. Create a PostgreSQL database and user.

3. Set up a Python virtual environment:
   ```bash
   python3 -m venv env
   source env/bin/activate
   pip install -r requirements.txt
   ```

4. Configure Gunicorn and Nginx (sample configs below).

5. Set up environment variables in a `.env` file based on `.env.example`.

6. Collect static files and run migrations:
   ```bash
   python manage.py collectstatic
   python manage.py migrate
   ```

7. Configure Nginx:
   ```
   server {
       listen 80;
       server_name your-domain.com;
   
       location = /favicon.ico { access_log off; log_not_found off; }
       location /static/ {
           root /path/to/your/project;
       }
       
       location /media/ {
           root /path/to/your/project;
       }
   
       location / {
           include proxy_params;
           proxy_pass http://unix:/path/to/your/project/your-project.sock;
       }
   }
   ```

8. Configure Gunicorn service file.

### 3. Docker Deployment

For Docker deployment, create a Dockerfile and docker-compose.yml file in your project root:

#### Dockerfile
```dockerfile
FROM python:3.11-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

RUN python manage.py collectstatic --noinput

EXPOSE 8000

CMD ["gunicorn", "gas_utility_service.wsgi:application", "--bind", "0.0.0.0:8000"]
```

#### docker-compose.yml
```yaml
version: '3'

services:
  db:
    image: postgres:16
    volumes:
      - postgres_data:/var/lib/postgresql/data/
    env_file:
      - ./.env
    environment:
      - POSTGRES_PASSWORD=postgres
      - POSTGRES_USER=postgres
      - POSTGRES_DB=gas_utility_service

  web:
    build: .
    restart: always
    depends_on:
      - db
    env_file:
      - ./.env
    volumes:
      - .:/app
      - static_volume:/app/staticfiles
      - media_volume:/app/media
    ports:
      - "8000:8000"

volumes:
  postgres_data:
  static_volume:
  media_volume:
```

Run with:
```
docker-compose up -d
```

## SSL Configuration

For secure deployment, enable HTTPS using Let's Encrypt:

1. Install Certbot:
   ```
   sudo apt install certbot python3-certbot-nginx
   ```

2. Get certificates:
   ```
   sudo certbot --nginx -d your-domain.com
   ```

## Monitoring and Maintenance

1. Set up regular database backups
2. Configure logging
3. Consider implementing a monitoring solution (e.g., Sentry for error tracking)

## Troubleshooting

- Check Nginx and Gunicorn logs for errors
- Ensure database connections are properly configured
- Verify static files are being served correctly 