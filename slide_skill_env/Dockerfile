FROM python:3.12-slim

# Node.js 20 for pptxgenjs
RUN apt-get update && \
    apt-get install -y curl && \
    curl -fsSL https://deb.nodesource.com/setup_20.x | bash - && \
    apt-get install -y nodejs && \
    apt-get clean && rm -rf /var/lib/apt/lists/*

# LibreOffice for pptx → pdf conversion
RUN apt-get update && \
    apt-get install -y --no-install-recommends libreoffice-impress && \
    apt-get clean && rm -rf /var/lib/apt/lists/*

# Poppler for pdf → jpg conversion
RUN apt-get update && \
    apt-get install -y --no-install-recommends poppler-utils && \
    apt-get clean && rm -rf /var/lib/apt/lists/*

WORKDIR /app

# Install Python dependencies
COPY pyproject.toml ./
RUN pip install --no-cache-dir .

# Copy project files
COPY package.json package-lock.json ./
RUN npm ci --production

COPY slide_skill_env/ slide_skill_env/
COPY skill_files_baseline/ skill_files_baseline/
COPY pptx/ pptx/

ENV HOME=/tmp
ENV SAL_USE_VCLPLUGIN=svp

EXPOSE 8000
CMD ["uvicorn", "slide_skill_env.app:app", "--host", "0.0.0.0", "--port", "8000", "--workers", "1"]
