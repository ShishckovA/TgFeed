# Base Python image
FROM python:3.10-buster

# Set working directory
WORKDIR /tg_feed

# Do not buffer stdout & stderr
ENV PYTHONUNBUFFERED 1

# Help Python with imports
ENV PYTHONPATH "src:${PYTHONPATH}"

# Copy reqirements manifests
COPY tg_feed/requirements.txt .

# Install pipenv & dependencies
RUN pip install --upgrade pip && pip install -r requirements.txt

# Copy everything else
COPY tg_feed .

# Copy session data
COPY tg_feed.session .

# Run bot
ENTRYPOINT ["python", "src/main.py"]