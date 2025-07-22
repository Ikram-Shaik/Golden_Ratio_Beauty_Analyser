FROM python:3.9-slim

# Set working directory
WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y \
    build-essential \
    curl \
    software-properties-common \
    git \
    libgl1 \
    libglib2.0-0 \
    libsm6 \
    libxext6 \
    libxrender-dev \
    ffmpeg \
    && rm -rf /var/lib/apt/lists/*

# Create Streamlit config directory and add config
RUN mkdir -p /app/.streamlit
RUN echo "\
[server]\n\
headless = true\n\
enableCORS = false\n\
enableXsrfProtection = false\n\
port = 8501\n\
\n\
[browser]\n\
gatherUsageStats = false\n\
" > /app/.streamlit/config.toml

# Copy files
COPY requirements.txt ./
COPY main.py ./

# Install Python dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Expose Streamlit default port
EXPOSE 8501

# Health check for Hugging Face Spaces
HEALTHCHECK CMD curl --fail http://localhost:8501/_stcore/health || exit 1

# Start Streamlit app
ENTRYPOINT ["streamlit", "run", "main.py", "--server.port=8501", "--server.address=0.0.0.0"]
