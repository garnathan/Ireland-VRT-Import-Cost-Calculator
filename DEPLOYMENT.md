# VRT Calculator Deployment Guide

## Local Development

### Quick Start
```bash
# Install dependencies
pip3 install -r requirements.txt

# Run development server
python3 app.py

# Access at: http://localhost:5000
```

### Production Mode
```bash
# Run with production settings
python3 run.py

# Or with custom settings
HOST=0.0.0.0 PORT=8080 DEBUG=false python3 run.py
```

## Production Deployment

### Using Gunicorn (Recommended)
```bash
# Install gunicorn (included in requirements.txt)
pip3 install gunicorn

# Run with gunicorn
gunicorn --bind 0.0.0.0:8000 --workers 4 app:app

# With configuration file
gunicorn --config gunicorn.conf.py app:app
```

### Docker Deployment
Create a `Dockerfile`:
```dockerfile
FROM python:3.9-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

EXPOSE 5000

CMD ["gunicorn", "--bind", "0.0.0.0:5000", "--workers", "4", "app:app"]
```

Build and run:
```bash
docker build -t vrt-calculator .
docker run -p 5000:5000 vrt-calculator
```

### Environment Variables

| Variable | Default | Description |
|----------|---------|-------------|
| `HOST` | `0.0.0.0` | Host to bind to |
| `PORT` | `5000` | Port to listen on |
| `DEBUG` | `False` | Enable debug mode |
| `SECRET_KEY` | `your-secret-key-change-this` | Flask secret key |
| `EXCHANGE_API_KEY` | None | API key for exchange rate service |

### Nginx Configuration
```nginx
server {
    listen 80;
    server_name your-domain.com;

    location / {
        proxy_pass http://127.0.0.1:5000;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
    }

    location /static {
        alias /path/to/your/app/static;
        expires 1y;
        add_header Cache-Control "public, immutable";
    }
}
```

### SSL/HTTPS Setup
```bash
# Using Let's Encrypt with Certbot
sudo certbot --nginx -d your-domain.com
```

## Cloud Deployment

### Heroku
1. Create `Procfile`:
```
web: gunicorn app:app
```

2. Deploy:
```bash
heroku create your-vrt-calculator
git push heroku main
```

### AWS EC2
1. Launch EC2 instance
2. Install Python and dependencies
3. Use systemd service for auto-start
4. Configure security groups for port 80/443

### DigitalOcean App Platform
1. Connect GitHub repository
2. Configure build settings:
   - Build command: `pip install -r requirements.txt`
   - Run command: `gunicorn --worker-tmp-dir /dev/shm app:app`

## Monitoring & Logging

### Application Logging
```python
import logging
logging.basicConfig(level=logging.INFO)
```

### Health Check Endpoint
The app includes a basic health check at `/api/exchange-rate`

### Performance Monitoring
Consider adding:
- New Relic
- DataDog
- Sentry for error tracking

## Security Considerations

1. **Change the secret key** in production
2. **Use HTTPS** for all traffic
3. **Rate limiting** for API endpoints
4. **Input validation** (already implemented)
5. **CORS configuration** if needed for API access

## Backup & Maintenance

- No database required (stateless application)
- Monitor exchange rate API limits
- Update VRT rates regularly
- Keep dependencies updated

## Troubleshooting

### Common Issues

1. **Port already in use**
   ```bash
   lsof -ti:5000 | xargs kill -9
   ```

2. **Permission denied**
   ```bash
   sudo chown -R $USER:$USER /path/to/app
   ```

3. **Module not found**
   ```bash
   pip3 install -r requirements.txt --user
   ```

### Logs Location
- Development: Console output
- Production: `/var/log/your-app/`
- Docker: `docker logs container-name`

## Performance Optimization

1. **Enable gzip compression**
2. **Use CDN for static files**
3. **Cache exchange rates** (implement Redis)
4. **Optimize images** in static folder
5. **Use HTTP/2** with proper server configuration
