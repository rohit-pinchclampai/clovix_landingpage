# Clovix Landing Page

This is a code bundle for Generate Code. The original project is available at https://www.figma.com/design/9GfDZrMvwnSjfQPkXblurr/Generate-Code.

## Running the code

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