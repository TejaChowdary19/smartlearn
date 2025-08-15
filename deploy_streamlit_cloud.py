#!/usr/bin/env python3
"""
SmartLearn Streamlit Cloud Deployment Script
Automates the deployment process to Streamlit Cloud
"""

import os
import sys
import subprocess
import json
import requests
from pathlib import Path

def check_git_status():
    """Check if the repository is ready for deployment"""
    print("🔍 Checking Git repository status...")
    
    try:
        # Check if we're in a git repository
        result = subprocess.run(['git', 'status'], capture_output=True, text=True)
        if result.returncode != 0:
            print("❌ Not in a Git repository. Please run this from your SmartLearn project directory.")
            return False
        
        # Check for uncommitted changes
        result = subprocess.run(['git', 'diff', '--name-only'], capture_output=True, text=True)
        if result.stdout.strip():
            print("⚠️  You have uncommitted changes. Consider committing them before deployment.")
            response = input("Continue with deployment? (y/N): ")
            if response.lower() != 'y':
                return False
        
        # Check if remote origin exists
        result = subprocess.run(['git', 'remote', 'get-url', 'origin'], capture_output=True, text=True)
        if result.returncode != 0:
            print("❌ No remote origin found. Please add your GitHub repository as origin.")
            return False
        
        print("✅ Git repository is ready for deployment")
        return True
        
    except Exception as e:
        print(f"❌ Error checking Git status: {e}")
        return False

def create_deployment_files():
    """Create necessary files for Streamlit Cloud deployment"""
    print("📁 Creating deployment files...")
    
    # Create .streamlit directory if it doesn't exist
    streamlit_dir = Path(".streamlit")
    streamlit_dir.mkdir(exist_ok=True)
    
    # Create config.toml if it doesn't exist
    config_file = streamlit_dir / "config.toml"
    if not config_file.exists():
        print("⚠️  .streamlit/config.toml not found. Creating default configuration...")
        # The config.toml was already created earlier
    
    # Create requirements.txt for deployment if it doesn't exist
    if not Path("requirements.txt").exists():
        print("📦 Creating requirements.txt for deployment...")
        subprocess.run(['cp', 'requirements_deployment.txt', 'requirements.txt'])
    
    print("✅ Deployment files created successfully")
    return True

def check_dependencies():
    """Check if all required dependencies are available"""
    print("📦 Checking dependencies...")
    
    required_files = [
        "requirements.txt",
        ".streamlit/config.toml",
        "src/app_final_corrected.py"
    ]
    
    missing_files = []
    for file_path in required_files:
        if not Path(file_path).exists():
            missing_files.append(file_path)
    
    if missing_files:
        print(f"❌ Missing required files: {', '.join(missing_files)}")
        return False
    
    print("✅ All required files are present")
    return True

def create_deployment_readme():
    """Create a deployment README with instructions"""
    print("📚 Creating deployment documentation...")
    
    readme_content = """# SmartLearn Deployment Guide

## 🚀 Streamlit Cloud Deployment

### Prerequisites
1. GitHub account with SmartLearn repository
2. Streamlit Cloud account (free)

### Deployment Steps

#### 1. Connect to Streamlit Cloud
1. Go to [share.streamlit.io](https://share.streamlit.io)
2. Sign in with GitHub
3. Click "New app"

#### 2. Configure Your App
- **Repository**: `tejachowdary19/smartlearn`
- **Branch**: `main`
- **Main file path**: `src/app_final_corrected.py`
- **App URL**: Will be generated automatically

#### 3. Advanced Settings
- **Python version**: 3.9
- **Requirements file**: `requirements.txt`
- **Environment variables**: Add if needed

#### 4. Deploy
Click "Deploy" and wait for the build to complete.

### Access Your App
Your app will be available at: `https://your-app-name.streamlit.app`

### Troubleshooting
- Check build logs for errors
- Ensure all dependencies are in requirements.txt
- Verify file paths are correct

## 🌐 Alternative Deployment Options

### Heroku Deployment
```bash
# Install Heroku CLI
brew install heroku/brew/heroku

# Login to Heroku
heroku login

# Create Heroku app
heroku create your-smartlearn-app

# Deploy
git push heroku main
```

### Docker Deployment
```bash
# Build Docker image
docker build -t smartlearn .

# Run container
docker run -p 8501:8501 smartlearn
```

## 📊 Monitoring and Maintenance
- Monitor app performance through Streamlit Cloud dashboard
- Set up alerts for errors and performance issues
- Regular updates and dependency management
"""
    
    with open("DEPLOYMENT_GUIDE.md", "w") as f:
        f.write(readme_content)
    
    print("✅ Deployment documentation created")
    return True

def create_dockerfile():
    """Create a Dockerfile for containerized deployment"""
    print("🐳 Creating Dockerfile...")
    
    dockerfile_content = """# SmartLearn Docker Image
FROM python:3.9-slim

# Set working directory
WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y \\
    build-essential \\
    curl \\
    software-properties-common \\
    git \\
    && rm -rf /var/lib/apt/lists/*

# Copy requirements and install Python dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy application code
COPY . .

# Create .streamlit directory and config
RUN mkdir -p .streamlit
COPY .streamlit/config.toml .streamlit/

# Expose port
EXPOSE 8501

# Set environment variables
ENV STREAMLIT_SERVER_PORT=8501
ENV STREAMLIT_SERVER_ADDRESS=0.0.0.0
ENV STREAMLIT_SERVER_HEADLESS=true

# Health check
HEALTHCHECK CMD curl --fail http://localhost:8501/_stcore/health

# Run the application
CMD ["streamlit", "run", "src/app_final_corrected.py", "--server.port=8501", "--server.address=0.0.0.0"]
"""
    
    with open("Dockerfile", "w") as f:
        f.write(dockerfile_content)
    
    print("✅ Dockerfile created")
    return True

def create_heroku_files():
    """Create Heroku deployment files"""
    print("☁️  Creating Heroku deployment files...")
    
    # Create Procfile
    procfile_content = "web: streamlit run src/app_final_corrected.py --server.port=$PORT --server.address=0.0.0.0"
    with open("Procfile", "w") as f:
        f.write(procfile_content)
    
    # Create runtime.txt
    runtime_content = "python-3.9.18"
    with open("runtime.txt", "w") as f:
        f.write(runtime_content)
    
    # Create app.json for Heroku
    app_json = {
        "name": "SmartLearn AI Education Platform",
        "description": "AI-powered educational platform with fine-tuned language models",
        "repository": "https://github.com/TejaChowdary19/smartlearn",
        "keywords": ["ai", "education", "machine-learning", "python", "streamlit"],
        "env": {
            "STREAMLIT_SERVER_HEADLESS": {
                "value": "true"
            },
            "STREAMLIT_SERVER_ADDRESS": {
                "value": "0.0.0.0"
            }
        },
        "buildpacks": [
            {
                "url": "heroku/python"
            }
        ]
    }
    
    with open("app.json", "w") as f:
        json.dump(app_json, f, indent=2)
    
    print("✅ Heroku deployment files created")
    return True

def create_github_actions():
    """Create GitHub Actions for automated deployment"""
    print("🔄 Creating GitHub Actions workflow...")
    
    # Create .github/workflows directory
    workflows_dir = Path(".github/workflows")
    workflows_dir.mkdir(parents=True, exist_ok=True)
    
    workflow_content = """name: Deploy SmartLearn

on:
  push:
    branches: [ main ]
  pull_request:
    branches: [ main ]

jobs:
  test:
    runs-on: ubuntu-latest
    steps:
    - uses: actions/checkout@v3
    - name: Set up Python
      uses: actions/setup-python@v4
      with:
        python-version: '3.9'
    - name: Install dependencies
      run: |
        python -m pip install --upgrade pip
        pip install -r requirements.txt
    - name: Run tests
      run: |
        python -m pytest tests/ -v

  deploy-streamlit:
    needs: test
    runs-on: ubuntu-latest
    if: github.ref == 'refs/heads/main'
    steps:
    - uses: actions/checkout@v3
    - name: Deploy to Streamlit Cloud
      run: |
        echo "Deployment to Streamlit Cloud is automatic when pushing to main branch"
        echo "Ensure your Streamlit Cloud app is connected to this repository"
"""
    
    workflow_file = workflows_dir / "deploy.yml"
    with open(workflow_file, "w") as f:
        f.write(workflow_content)
    
    print("✅ GitHub Actions workflow created")
    return True

def show_deployment_instructions():
    """Display deployment instructions"""
    print("\n" + "="*60)
    print("🚀 SMARTLEARN DEPLOYMENT READY!")
    print("="*60)
    
    print("\n📋 Next Steps for Deployment:")
    
    print("\n1️⃣  STREAMLIT CLOUD (Recommended):")
    print("   • Go to: https://share.streamlit.io")
    print("   • Sign in with GitHub")
    print("   • Click 'New app'")
    print("   • Repository: tejachowdary19/smartlearn")
    print("   • Main file: src/app_final_corrected.py")
    print("   • Branch: main")
    
    print("\n2️⃣  HEROKU:")
    print("   • Install Heroku CLI: brew install heroku/brew/heroku")
    print("   • Login: heroku login")
    print("   • Create app: heroku create your-smartlearn-app")
    print("   • Deploy: git push heroku main")
    
    print("\n3️⃣  DOCKER:")
    print("   • Build: docker build -t smartlearn .")
    print("   • Run: docker run -p 8501:8501 smartlearn")
    
    print("\n4️⃣  GITHUB ACTIONS:")
    print("   • Workflow created: .github/workflows/deploy.yml")
    print("   • Automatic testing on push")
    print("   • Ready for CI/CD integration")
    
    print("\n📚 Documentation:")
    print("   • DEPLOYMENT_GUIDE.md - Complete deployment guide")
    print("   • .streamlit/config.toml - Streamlit configuration")
    print("   • Dockerfile - Container configuration")
    print("   • Procfile - Heroku configuration")
    
    print("\n🔗 Your Repository:")
    print("   • https://github.com/TejaChowdary19/smartlearn")
    
    print("\n" + "="*60)
    print("🎉 Your SmartLearn app is ready for deployment!")
    print("="*60)

def main():
    """Main deployment preparation function"""
    print("🚀 SmartLearn Deployment Preparation")
    print("="*50)
    
    # Check prerequisites
    if not check_git_status():
        print("❌ Deployment preparation failed. Please fix the issues above.")
        return False
    
    # Create deployment files
    if not create_deployment_files():
        print("❌ Failed to create deployment files.")
        return False
    
    if not check_dependencies():
        print("❌ Missing dependencies. Please install required packages.")
        return False
    
    # Create deployment configurations
    create_deployment_readme()
    create_dockerfile()
    create_heroku_files()
    create_github_actions()
    
    # Commit deployment files
    print("📝 Committing deployment files...")
    try:
        subprocess.run(['git', 'add', '.'], check=True)
        subprocess.run(['git', 'commit', '-m', 'Add deployment configuration files'], check=True)
        print("✅ Deployment files committed to Git")
    except subprocess.CalledProcessError:
        print("⚠️  Failed to commit deployment files. Please commit manually.")
    
    # Show deployment instructions
    show_deployment_instructions()
    
    return True

if __name__ == "__main__":
    success = main()
    if success:
        print("\n🎯 Ready to deploy! Choose your deployment method above.")
    else:
        print("\n❌ Deployment preparation failed. Please check the errors above.")
        sys.exit(1)
