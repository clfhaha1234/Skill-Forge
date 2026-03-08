# Slide Skill OpenEnv — HuggingFace Spaces Docker image
#
# HF Spaces requirements:
#   - app_port: 7860  (set in README.md YAML header)
#   - Non-root user with UID 1000
#   - SLIDE_SKILL_SESSION_ROOT=/tmp (Spaces app dir is read-only)
#
# Layer sizes (approximate):
#   python:3.12-slim base:     ~130 MB
#   Node.js 20 + pptxgenjs:   ~200 MB
#   LibreOffice:               ~500 MB
#   poppler-utils (pdftoppm):  ~30 MB
#   Python deps:               ~80 MB
# Total compressed: ~600-700 MB

FROM python:3.12-slim

LABEL description="Slide Skill OpenEnv — McKinsey PPT generation environment"

# System dependencies — installed in one RUN to minimize layers.
RUN apt-get update && apt-get install -y --no-install-recommends \
    libreoffice \
    poppler-utils \
    curl \
    ca-certificates \
    gnupg \
    && curl -fsSL https://deb.nodesource.com/setup_20.x | bash - \
    && apt-get install -y nodejs \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*

# Verify all required tools are available at build time.
RUN node --version && npm --version && soffice --version && pdftoppm -v 2>&1 | head -1

# HuggingFace Spaces requires a non-root user with UID 1000.
RUN useradd -m -u 1000 appuser

WORKDIR /app

# Install pptxgenjs (Node.js dependency).
COPY package.json package-lock.json* ./
RUN npm install --production

# Install Python dependencies.
COPY pyproject.toml ./
RUN pip install --no-cache-dir -e ".[server]"

# Copy application code and data.
COPY pptx/ ./pptx/
COPY skill_files_baseline/ ./skill_files_baseline/
COPY slide_skill_env/ ./slide_skill_env/

# Embed the fixed task prompt directly (output/reference/ images are not
# included — the evaluator runs without them using rubric-only scoring).
RUN mkdir -p /app/output/reference && \
    printf '%s\n' \
      '# Task Prompt' \
      '' \
      'Generate a 1-slide PowerPoint comparing three hydrogen production methods (Grey, Blue, Green) in McKinsey & Company consulting style.' \
      '' \
      'The slide should include:' \
      '- An insight-driven title (a "so-what" conclusion, not a topic label)' \
      '- A structured comparison table with columns for Grey H2, Blue H2, and Green H2' \
      '- Row categories: Production process, CO2 emissions (kg CO2/kgH2), Investment scale, EPC duration, Link to power sector' \
      '- Footnotes with source citations' \
      '- A "McKinsey & Company" footer with page number' \
      '' \
      'Use the rubric in your evaluation to score against McKinsey visual standards.' \
    > /app/output/TASK_PROMPT.md

# Give the non-root user ownership of the app directory.
RUN chown -R appuser:appuser /app

USER appuser

WORKDIR /app

# LibreOffice needs a writable HOME for its user profile.
ENV HOME=/tmp
ENV SAL_USE_VCLPLUGIN=svp

# Sessions are written to /tmp (writable on HF Spaces).
ENV SLIDE_SKILL_SESSION_ROOT=/tmp

EXPOSE 7860

HEALTHCHECK --interval=30s --timeout=10s --retries=3 \
    CMD python -c "import urllib.request; urllib.request.urlopen('http://localhost:7860/health')"

CMD ["sh", "slide_skill_env/start.sh"]
