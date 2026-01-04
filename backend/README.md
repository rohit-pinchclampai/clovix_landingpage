# Clovix Backend API

Production-ready Python FastAPI backend for storing prospect customer information from the landing page.

## Features

- ✅ RESTful API for prospect registration
- ✅ SQLite database for data storage (with PostgreSQL support ready)
- ✅ CORS enabled for frontend integration
- ✅ Email validation with Pydantic
- ✅ Duplicate email prevention
- ✅ **Rate limiting** to prevent abuse
- ✅ **API key authentication** for admin endpoints
- ✅ **Structured logging** with configurable levels
- ✅ **Proper error handling** and validation
- ✅ **Statistics endpoint** for prospect analytics
- ✅ **Environment-based configuration**
- ✅ **Production-ready architecture** with separation of concerns

## Setup

### 1. Install Dependencies

```bash
cd backend
pip install -r requirements.txt
```

Or using a virtual environment (recommended):

```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
pip install -r requirements.txt
```

### 2. Configure Environment Variables

Copy the example environment file:

```bash
cp env.example .env
```

Edit `.env` with your configuration. For development, the defaults are fine, but for production you should:
- Set `ENVIRONMENT=production`
- Set a strong `API_KEY` for admin endpoints
- Configure `FRONTEND_URL` with your actual frontend domain
- Adjust `RATE_LIMIT_PER_MINUTE` as needed

### 3. Run the Server

```bash
python main.py
```

Or using uvicorn directly:

```bash
uvicorn main:app --reload --host 0.0.0.0 --port 8000
```

The API will be available at `http://localhost:8000`

## API Endpoints

### Health Check
- `GET /health` - Check if the API is running

### Create Prospect
- `POST /api/prospects`
  - Body: `{ "name": "John Doe", "companyName": "Acme Corp", "email": "john@example.com" }`
  - Returns: Created prospect with ID and timestamp

### Get All Prospects
- `GET /api/prospects?skip=0&limit=100`
  - Returns: List of all prospects

### Get Prospect by ID
- `GET /api/prospects/{id}`
  - Headers: `X-API-Key: your-api-key` (required)
  - Returns: Specific prospect details

### Get Prospect Statistics
- `GET /api/prospects/stats/summary`
  - Headers: `X-API-Key: your-api-key` (required)
  - Returns: Statistics including total, today, this week, and this month

## API Documentation

FastAPI automatically generates interactive API documentation:

- Swagger UI: `http://localhost:8000/docs`
- ReDoc: `http://localhost:8000/redoc`

## Database

The database is stored in `prospects.db` (SQLite) by default. The database is automatically created on first run.

### Database Schema

```sql
prospects (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL,
    company_name TEXT NOT NULL,
    email TEXT NOT NULL UNIQUE,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
)
```

## Deployment

### Option 1: AWS Lambda + API Gateway

Use AWS SAM or Serverless Framework to deploy as a serverless function.

### Option 2: AWS EC2 / ECS

Deploy as a containerized application.

### Option 3: AWS Elastic Beanstalk

Simple deployment option for Python applications.

### Option 4: Railway / Render / Heroku

Platform-as-a-Service options for quick deployment.

## Project Structure

```
backend/
├── main.py           # FastAPI application entry point
├── config.py         # Configuration management
├── database.py       # Database connection and initialization
├── models.py         # Pydantic models for validation
├── routes.py         # API route handlers
├── middleware.py     # Authentication and security middleware
├── limiter.py        # Rate limiting configuration
├── requirements.txt  # Python dependencies
├── env.example       # Environment variables template
└── README.md         # This file
```

## Environment Variables

| Variable | Description | Default |
|----------|-------------|---------|
| `ENVIRONMENT` | Application environment (development/production) | `development` |
| `DEBUG` | Enable debug mode | `false` |
| `LOG_LEVEL` | Logging level (DEBUG/INFO/WARNING/ERROR) | `INFO` |
| `HOST` | Server host | `0.0.0.0` |
| `PORT` | Server port | `8000` |
| `DATABASE_PATH` | Path to SQLite database file | `prospects.db` |
| `DATABASE_URL` | PostgreSQL connection URL (optional) | - |
| `FRONTEND_URL` | Comma-separated list of allowed frontend URLs | `http://localhost:5173,http://localhost:3000` |
| `API_KEY` | API key for admin endpoints | - |
| `RATE_LIMIT_PER_MINUTE` | Rate limit for prospect creation | `10` |

## Security Features

### Rate Limiting
- Prospect creation endpoint is rate-limited (default: 10 requests/minute per IP)
- Prevents abuse and spam registrations
- Configurable via `RATE_LIMIT_PER_MINUTE` environment variable

### API Key Authentication
- Admin endpoints require `X-API-Key` header
- Set `API_KEY` environment variable to enable
- If not set, admin endpoints are open (development mode only)

### Input Validation
- All inputs validated using Pydantic models
- Email format validation
- String length limits
- SQL injection protection via parameterized queries

## Production Considerations

1. ✅ **Database**: SQLite is fine for small scale. For production, migrate to PostgreSQL:
   - Set `DATABASE_URL=postgresql://user:password@host:port/dbname`
   - Update `database.py` to use PostgreSQL adapter (psycopg2)

2. ✅ **CORS**: Already configured - set `FRONTEND_URL` to your actual domain in production

3. ✅ **Authentication**: API key authentication is implemented - set `API_KEY` in production

4. ✅ **Rate Limiting**: Implemented and configurable

5. ✅ **Logging**: Structured logging with configurable levels

6. **Backup**: Set up regular database backups (automated scripts or cloud backup service)

7. **Monitoring**: Consider adding:
   - Application performance monitoring (APM)
   - Error tracking (Sentry)
   - Health check monitoring
   - Database monitoring

## Testing the API

### Create a Prospect
```bash
curl -X POST http://localhost:8000/api/prospects \
  -H "Content-Type: application/json" \
  -d '{"name":"John Doe","companyName":"Acme Corp","email":"john@example.com"}'
```

### Get All Prospects (Admin)
```bash
curl -X GET http://localhost:8000/api/prospects \
  -H "X-API-Key: your-api-key"
```

### Get Statistics (Admin)
```bash
curl -X GET http://localhost:8000/api/prospects/stats/summary \
  -H "X-API-Key: your-api-key"
```

