# Clovix Landing Page

This is a code bundle for Generate Code. The original project is available at https://www.figma.com/design/9GfDZrMvwnSjfQPkXblurr/Generate-Code.

## Project Structure

This is a **monorepo** containing both frontend and backend:

```
clovix_landingpage/
├── frontend/          # React + TypeScript + Vite
│   ├── src/
│   ├── package.json
│   └── vite.config.ts
├── backend/          # Python FastAPI
│   ├── main.py
│   ├── routes.py
│   └── requirements.txt
└── docs/             # Documentation
```

## Quick Start

### Frontend Development

Run `npm i` to install the dependencies.

Run `npm run dev` to start the development server.

Run `npm i` to install the dependencies.

Run `npm run dev` to start the development server.

## Building for production

Run `npm run build` to create a production build. The output will be in the `dist` directory.

## Deployment to AWS Amplify

This project is configured for deployment on AWS Amplify with CI/CD pipeline.

### Setup Instructions

1. **Connect your repository to AWS Amplify:**
   - Go to [AWS Amplify Console](https://console.aws.amazon.com/amplify/)
   - Click "New app" → "Host web app"
   - Connect your Git provider (GitHub, GitLab, Bitbucket, etc.)
   - Select your repository and branch

2. **Configure build settings:**
   - Amplify will automatically detect the `amplify.yml` file
   - Build settings:
     - Build command: `npm run build`
     - Output directory: `dist`
     - Node version: 20.x (or latest LTS)

3. **Environment variables (if needed):**
   - Add any required environment variables in the Amplify Console
   - Go to App settings → Environment variables

4. **Deploy:**
   - Amplify will automatically deploy on every push to your main branch
   - You can also trigger manual deployments from the console

### CI/CD Pipeline

The project includes:
- `amplify.yml` - AWS Amplify build configuration
- `.github/workflows/amplify-deploy.yml` - GitHub Actions workflow (optional)

The pipeline will:
- Install dependencies using `npm ci`
- Build the project
- Deploy to AWS Amplify hosting

### Custom Domain (Optional)

1. In Amplify Console, go to "Domain management"
2. Add your custom domain
3. Follow the DNS configuration instructions

## Backend API

The project includes a **production-ready Python FastAPI backend** for storing prospect customer information.

### Why Monorepo?

This project uses a monorepo structure because:
- ✅ Frontend and backend are tightly coupled
- ✅ Easier to coordinate API changes
- ✅ Single source of truth for documentation
- ✅ Simpler local development setup
- ✅ Atomic commits across both codebases

For larger teams or when services need independent scaling, consider splitting into separate repos.

### Backend Setup

1. **Navigate to backend directory:**
   ```bash
   cd backend
   ```

2. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

3. **Run the server:**
   ```bash
   python main.py
   ```

   The API will be available at `http://localhost:8000`

4. **API Documentation:**
   - Swagger UI: `http://localhost:8000/docs`
   - ReDoc: `http://localhost:8000/redoc`

### Backend Features

- RESTful API for prospect registration
- SQLite database for data storage
- Email validation and duplicate prevention
- CORS enabled for frontend integration

### API Endpoints

- `POST /api/prospects` - Register a new prospect
- `GET /api/prospects` - Get all prospects (admin)
- `GET /api/prospects/{id}` - Get specific prospect

### Frontend Integration

The registration form automatically sends data to the backend API. Configure the API URL using environment variables:

1. Create a `.env` file in the root directory:
   ```bash
   VITE_API_URL=http://localhost:8000
   ```

2. For production, set `VITE_API_URL` in AWS Amplify environment variables to your deployed backend URL.

### Backend Deployment

See [DEPLOYMENT.md](./DEPLOYMENT.md) for detailed backend deployment instructions including:
- AWS Lambda + API Gateway
- AWS Elastic Beanstalk
- AWS ECS (Docker)
- Railway / Render / Heroku

### Database

The backend uses SQLite by default (development). For production, consider:
- PostgreSQL (AWS RDS, Railway, Render)
- DynamoDB (AWS serverless)

See `backend/README.md` for more details.