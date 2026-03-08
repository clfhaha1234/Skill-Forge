# Slide Skill OpenEnv — Docker image
#
# Layer sizes (approximate):
#   python:3.12-slim base:     ~130 MB
#   Node.js 20 + pptxgenjs:   ~200 MB
#   LibreOffice:               ~500 MB  <-- dominant cost; unavoidable for .pptx → .pdf
#   poppler-utils (pdftoppm):  ~30 MB
#   Python deps:               ~80 MB
# Total compressed: ~600-700 MB
#
# LibreOffice is the unavoidable bottleneck. It is required to convert
# .pptx → .pdf. There is no lighter alternative that handles pptxgenjs
# output faithfully.

FROM python:3.12-slim

LABEL description="Slide Skill OpenEnv — McKinsey PPT generation environment"

# System dependencies — installed in one RUN to minimize layers.
RUN apt-get update && apt-get install -y --no-install-recommends \
    # LibreOffice for .pptx → .pdf conversion
    libreoffice \
    # poppler-utils provides pdftoppm (.pdf → .jpg)
    poppler-utils \
    # Node.js 20 LTS via NodeSource
    curl \
    ca-certificates \
    gnupg \
    && curl -fsSL https://deb.nodesource.com/setup_20.x | bash - \
    && apt-get install -y nodejs \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*

# Verify all required tools are available at build time.
RUN node --version && npm --version && soffice --version && pdftoppm -v 2>&1 | head -1

WORKDIR /app

# Install pptxgenjs (Node.js dependency) — copy package.json first for layer caching.
COPY package.json package-lock.json* ./
RUN npm install --production

# Install Python dependencies — copy pyproject.toml first for layer caching.
COPY pyproject.toml ./
RUN pip install --no-cache-dir -e ".[server]"

# Copy application code and data.
COPY pptx/ ./pptx/
COPY skill_files_baseline/ ./skill_files_baseline/
COPY output/TASK_PROMPT.md ./output/TASK_PROMPT.md
COPY output/reference/ ./output/reference/
COPY openenv/ ./openenv/

WORKDIR /app/openenv

# LibreOffice needs a writable user profile directory.
# Setting HOME=/tmp gives each process its own profile path and avoids
# concurrent session conflicts with the LibreOffice lock files.
ENV HOME=/tmp
# Use the headless VCL plugin (no display required).
ENV SAL_USE_VCLPLUGIN=svp

EXPOSE 8000

HEALTHCHECK --interval=30s --timeout=10s --retries=3 \
    CMD python -c "import urllib.request; urllib.request.urlopen('http://localhost:8000/health')"

# Single worker — LibreOffice subprocess calls must be serialized within one
# OS process. Concurrent sessions are handled by per-session /tmp/ directories.
CMD ["uvicorn", "app:app", "--host", "0.0.0.0", "--port", "8000", "--workers", "1"]
