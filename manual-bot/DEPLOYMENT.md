# Deployment Guide

This guide covers deploying the Automotive Manual ChatBot in various environments.

## Local Development

See [README.md](README.md) for development setup.

## Docker Deployment

### Build Docker Image

```dockerfile
FROM python:3.11-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

EXPOSE 8000

CMD ["python", "-m", "uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
```

Build:
```bash
docker build -t automotive-chatbot:latest .
```

Run:
```bash
docker run -p 8000:8000 \
  -e OPENAI_API_KEY=your_key_here \
  -v $(pwd)/data:/app/data \
  automotive-chatbot:latest
```

## Cloud Deployment Options

### Heroku

1. Create `Procfile`:
```
web: python -m uvicorn app.main:app --host 0.0.0.0 --port $PORT
```

2. Set environment variables:
```bash
heroku config:set OPENAI_API_KEY=your_key_here
```

3. Deploy:
```bash
git push heroku main
```

### AWS (Lambda + API Gateway)

Use AWS SAM or similar for serverless deployment.

### Google Cloud Run

```bash
gcloud run deploy automotive-chatbot \
  --source . \
  --platform managed \
  --region us-central1 \
  --set-env-vars OPENAI_API_KEY=your_key_here
```

### DigitalOcean App Platform

1. Push to GitHub
2. Connect repository
3. Set build command: `pip install -r requirements.txt`
4. Set run command: `python -m uvicorn app.main:app --host 0.0.0.0 --port 8080`
5. Set environment variables

## Production Considerations

### Security
- Use HTTPS only
- Implement API authentication
- Rate limiting
- Input validation

### Performance
- Use production WSGI server: Gunicorn
```bash
gunicorn -w 4 -b 0.0.0.0:8000 app.main:app
```

- Enable caching
- Use CDN for static files
- Database optimization

### Monitoring
- Set up logging
- Monitor API usage
- Track errors with Sentry
- Performance monitoring

### Scaling
- Horizontal scaling: Multiple instances
- Load balancing
- Database replication
- CDN for frontend

## Environment Variables (Production)

```env
OPENAI_API_KEY=production_key
OPENAI_MODEL=gpt-4
APP_HOST=0.0.0.0
APP_PORT=8000
DEBUG=False
CHROMA_DB_PATH=/persistent/storage/chroma_db
```

## Database Persistence

Ensure Chroma database is on persistent storage:
- Docker volumes
- Managed databases
- Cloud storage (S3, GCS)

## CI/CD Pipeline

### GitHub Actions Example

```yaml
name: Deploy

on:
  push:
    branches: [main]

jobs:
  test:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v2
      - uses: actions/setup-python@v2
        with:
          python-version: '3.11'
      - run: pip install -r requirements.txt
      - run: pytest

  deploy:
    needs: test
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v2
      - name: Deploy to production
        run: |
          # Add deployment commands
```

## Troubleshooting Deployment

1. **Memory issues**: Increase container memory limit
2. **Slow startup**: Pre-load models, use persistent storage
3. **API timeouts**: Increase request timeout, optimize queries
4. **Storage**: Ensure sufficient space for vector database
